import mongoengine
from django.db import models


class MyModel(models.Model):
    class Meta:
        permissions = (
            ('change_content', 'Content administrators'),
        )

class TreeInfo(mongoengine.Document):
    name = mongoengine.StringField(max_length=200, required=True, index=True)
    latin_name = mongoengine.StringField(max_length=200)
    description = mongoengine.StringField()
    published = mongoengine.BooleanField(default=False)

    meta = {'db_alias': 'mongo', "indexes": ["$name"]}