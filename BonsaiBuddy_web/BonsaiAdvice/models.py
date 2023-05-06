from django.db import models
import mongoengine

class AdvicePermissionModel(models.Model):
    class Meta:
        permissions = (
            ('change_content', 'Content administrators'),
        )


class BonsaiTechnique(mongoengine.Document):
    short_name = mongoengine.StringField(max_length=200, required=True, index=True, unique=True)
    display_name = mongoengine.StringField(max_length=200)
    description = mongoengine.StringField()
    category = mongoengine.StringField(max_length=200)
    published = mongoengine.BooleanField(default=False)

    meta = {'db_alias': 'mongo', "indexes": ["$short_name"]}

    def __str__(self):
        return self.name

class BonsaiObjective(mongoengine.Document):
    short_name = mongoengine.StringField(max_length=200, required=True, index=True, unique=True)
    display_name = mongoengine.StringField(max_length=200)
    description = mongoengine.StringField()
    published = mongoengine.BooleanField(default=False)

    meta = {'db_alias': 'mongo', "indexes": ["$short_name"]}

    def __str__(self):
        return self.name

class BonsaiWhen(mongoengine.Document):
    short_name = mongoengine.StringField(max_length=200, required=True, index=True, unique=True)
    display_name = mongoengine.StringField(max_length=200)
    description = mongoengine.StringField()
    published = mongoengine.BooleanField(default=False)

    meta = {'db_alias': 'mongo', "indexes": ["$short_name"]}

    def __str__(self):
        return self.name