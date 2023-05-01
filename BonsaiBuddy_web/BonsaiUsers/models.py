import mongoengine

# Create your models here.
from django.contrib.auth.models import AbstractUser
import bcrypt
from django.utils import timezone


class User(AbstractUser):
    pass

COUNTRY_ENUM = ["Undefined", "Belgium"]

class UserProfile(mongoengine.Document):
    username = mongoengine.StringField()
    password = mongoengine.BinaryField(max_length=128)
    last_pwd_update = mongoengine.DateTimeField(null=True)
    last_login = mongoengine.DateTimeField(null=True)
    country = mongoengine.StringField(default="Undefined")

    meta = {'db_alias': 'mongo', "indexes": ["$username"]}

    def create_user(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.save()

    def update_password(self, password):
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        self.last_pwd_update = timezone.now()
        self.save()

    def __str__(self):
        return self.username