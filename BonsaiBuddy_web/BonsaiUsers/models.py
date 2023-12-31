import mongoengine

# Create your models here.
from django.contrib.auth.models import AbstractUser
import bcrypt
from django.utils import timezone
import pycountry
from TreeInfo.models import TreeInfo
from BonsaiAdvice.models import BonsaiObjective
from bson import ObjectId
from rest_framework import permissions


class User(AbstractUser):
    pass


class OwnProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


def build_country_list():
    countries = [(country.name.lower(), country.name)
                 for country in sorted(pycountry.countries, key=lambda x: x.name)]
    countries.insert(0, ("unknown", "Unknown"))
    return countries


class TreeCollection(mongoengine.EmbeddedDocument):
    oid = mongoengine.ObjectIdField(
        required=True, default=ObjectId, primary_key=True)
    treeReference = mongoengine.ReferenceField(TreeInfo)
    objective = mongoengine.ReferenceField(BonsaiObjective)


class UserProfile(mongoengine.Document):
    username = mongoengine.StringField()
    password = mongoengine.BinaryField(max_length=128)
    last_pwd_update = mongoengine.DateTimeField(null=True)
    last_login = mongoengine.DateTimeField(null=True)
    country = mongoengine.StringField(default="Undefined")
    my_trees = mongoengine.EmbeddedDocumentListField(TreeCollection)

    meta = {'db_alias': 'mongo', "indexes": ["$username"]}

    def create_user(self, password):
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt())
        self.save()

    def update_password(self, password):
        self.password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt())
        self.last_pwd_update = timezone.now()
        self.save()

    def get_my_tree(self, oid):
        if isinstance(oid, str):
            oid = ObjectId(oid)
        for tree in self.my_trees:
            if tree.oid == oid:
                return tree
        return None

    @staticmethod
    def get_user(username):
        return UserProfile.objects.get(username=username)

    def __str__(self):
        return self.username
