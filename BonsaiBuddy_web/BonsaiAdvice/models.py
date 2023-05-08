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

    @staticmethod
    def get_all(published_only=True):
        objects = BonsaiTechnique.objects
        if published_only:
            objects = objects.filter(published=True)
        return objects.order_by("short_name")

    @staticmethod
    def get(short_name):
        return BonsaiTechnique.objects.get(short_name=short_name)

class BonsaiObjective(mongoengine.Document):
    short_name = mongoengine.StringField(max_length=200, required=True, index=True, unique=True)
    display_name = mongoengine.StringField(max_length=200)
    description = mongoengine.StringField()
    published = mongoengine.BooleanField(default=False)

    meta = {'db_alias': 'mongo', "indexes": ["$short_name"]}

    def __str__(self):
        return self.name

    @staticmethod
    def get_all(published_only=True):
        objects = BonsaiObjective.objects
        if published_only:
            objects = objects.filter(published=True)
        return objects.order_by("short_name")

    @staticmethod
    def get(short_name):
        return BonsaiObjective.objects.get(short_name=short_name)


class BonsaiWhen(mongoengine.Document):
    short_name = mongoengine.StringField(max_length=200, required=True, index=True, unique=True)
    display_name = mongoengine.StringField(max_length=200)
    description = mongoengine.StringField()
    published = mongoengine.BooleanField(default=False)

    meta = {'db_alias': 'mongo', "indexes": ["$short_name"]}

    def __str__(self):
        return self.name

    @staticmethod
    def get_all(published_only=True):
        objects = BonsaiWhen.objects
        if published_only:
            objects = objects.filter(published=True)
        return objects.order_by("short_name")

    @staticmethod
    def get(short_name):
        return BonsaiWhen.objects.get(short_name=short_name)
