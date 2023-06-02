import mongoengine
from django.db import models
from BonsaiAdvice.models import BonsaiTechnique, BonsaiObjective, BonsaiWhen, get_periods
from bson import ObjectId


class TreeInfoPermissionModel(models.Model):
    class Meta:
        permissions = (
            ('change_content', 'Content administrators'),
        )

class TechniqueMapper(mongoengine.EmbeddedDocument):
    oid = mongoengine.ObjectIdField(required=True, default=ObjectId, primary_key=True)
    technique = mongoengine.LazyReferenceField(BonsaiTechnique)
    objective = mongoengine.LazyReferenceField(BonsaiObjective)
    when = mongoengine.ListField(mongoengine.LazyReferenceField(BonsaiWhen))
    period = mongoengine.ListField(choices=[f"{_[0][0]}_{_[0][1]}" for _ in get_periods()])
    comment = mongoengine.StringField()

    def __str__(self):
        return f"Mapper({self.oid}): technique={self.technique}, objective={self.objective}, when={self.when}, period={self.period}"


class TreeInfo(mongoengine.Document):
    name = mongoengine.StringField(max_length=200, required=True, index=True, unique=True)
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

    def get_techniques_list(self):
        techniques = [{"oid": item.oid,
                       "technique": item.technique.fetch().short_name if item.technique else None,
                       "objective": item.objective.fetch().short_name if item.objective else None,
                       "when": [when.fetch().short_name if when else None for when in item.when],
                       "period": item.period,
                       "comment": item.comment
                       } for item in self.techniques]
        if len(techniques) == 0:
            techniques.append({})
        return techniques