import mongoengine
from django.db import models
from django.urls import reverse
from BonsaiAdvice.models import BonsaiTechnique, BonsaiObjective, BonsaiStage, get_periods, periodid_to_name
from bson import ObjectId
from rest_framework import permissions


class TreeInfoPermissionModel(models.Model):
    class Meta:
        permissions = (
            ('change_content', 'Content administrators'),
        )


class TreeInfoPermissionModelAPI(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.has_perm('TreeInfo.change_content')


class TechniqueMapper(mongoengine.EmbeddedDocument):
    oid = mongoengine.ObjectIdField(
        required=True, default=ObjectId, primary_key=True)
    technique = mongoengine.LazyReferenceField(BonsaiTechnique)
    objective = mongoengine.LazyReferenceField(BonsaiObjective)
    stage = mongoengine.ListField(mongoengine.LazyReferenceField(BonsaiStage))
    period = mongoengine.ListField(
        choices=[f"{_[0][0]}_{_[0][1]}" for _ in get_periods()])
    comment = mongoengine.StringField()

    def __str__(self):
        return f"Mapper({self.oid}): technique={self.technique}, objective={self.objective}, stage={self.stage}, period={self.period}"

    def fetch(self):
        self.technique_f = self.technique.fetch()
        self.objective_f = self.objective.fetch()
        self.stage_f = [_.fetch().display_name for _ in self.stage]

    def link(self, tree):
        return f"<a href='{reverse('BonsaiAdvice:which_technique')}?oid={self.oid!s}&tree={tree}'>more</a>"


class TreeInfo(mongoengine.Document):
    name = mongoengine.StringField(
        max_length=200, required=True, index=True, unique=True)
    display_name = mongoengine.StringField(max_length=200, required=True)
    latin_name = mongoengine.StringField(max_length=200)
    description = mongoengine.StringField()
    placement = mongoengine.StringField()
    watering = mongoengine.StringField()
    fertilizing = mongoengine.StringField()
    pruning_wiring = mongoengine.StringField()
    repotting = mongoengine.StringField()
    propagation = mongoengine.StringField()
    pests = mongoengine.StringField()
    published = mongoengine.BooleanField(default=False)
    techniques = mongoengine.EmbeddedDocumentListField(TechniqueMapper)

    meta = {'db_alias': 'mongo', "indexes": ["$name"]}

    def __str__(self):
        return self.display_name

    @staticmethod
    def get_all(published_only=True, order_by="name"):
        objects = TreeInfo.objects
        if published_only:
            objects = objects.filter(published=True)
        return objects.order_by(order_by)

    @staticmethod
    def get(name):
        return TreeInfo.objects.get(name=name)

    def get_techniques_list(self, sort=None):
        sort = sort if sort else "technique"
        techniques = [{"oid": item.oid,
                       "technique_name": item.technique.fetch().display_name if item.technique else None,
                       "technique": item.technique.fetch().short_name if item.technique else None,
                       "objective": item.objective.fetch().short_name if item.objective else None,
                       "stage": [stage.fetch().short_name if stage else None for stage in item.stage],
                       "period": item.period,
                       "comment": item.comment
                       } for item in self.techniques]
        techniques = sorted(techniques, key=lambda technique: technique[sort])
        if len(techniques) == 0:
            techniques.append({})
        return techniques
