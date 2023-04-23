import mongoengine

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

COUNTRY_ENUM = ["Undefined", "Belgium"]

class UserProfile(mongoengine.Document):
    username = mongoengine.StringField()
    password = mongoengine.StringField(max_length=128)
    salt = mongoengine.StringField(max_length=16)
    last_pwd_update = mongoengine.DateTimeField(null=True)
    last_login = mongoengine.DateTimeField(null=True)
    country = mongoengine.EnumField(enum=COUNTRY_ENUM, default="Undefined")

    meta = {'db_alias': 'mongo', "indexes": ["$username"]}