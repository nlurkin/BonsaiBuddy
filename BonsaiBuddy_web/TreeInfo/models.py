import mongoengine
from django.db import models


class TreeInfoPermissionModel(models.Model):
    class Meta:
        permissions = (
            ('change_content', 'Content administrators'),
        )

class TreeInfo(mongoengine.Document):
    name = mongoengine.StringField(max_length=200, required=True, index=True, unique=True)
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

    meta = {'db_alias': 'mongo', "indexes": ["$name"]}

    def __str__(self):
        return self.name