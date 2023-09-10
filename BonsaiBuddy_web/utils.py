from django.http import Http404
from django.test import TestCase
import mongoengine
import os
import importlib
from django.contrib.auth.models import Permission
from TreeInfo.models import TreeInfo
from BonsaiAdvice.models import BonsaiObjective, BonsaiTechnique, BonsaiWhen, get_periods, get_technique_categories

def get_object_or_404(klass, **kwargs):
    try:
        obj = klass.objects.get(**kwargs)
    except klass.DoesNotExist:
        raise Http404(f"{klass.__name__} does not exist")
    return obj


class MongoDBTestCase(TestCase):
    database_name = "test_database"
    def setUp(self):
        settings = importlib.import_module(os.environ["DJANGO_SETTINGS_MODULE"])
        MONGO_DATABASE_HOST = 'mongodb+srv://%s:%s@%s/%s?ssl=true' % (
            settings.MONGO_USER, settings.MONGO_PASS, settings.MONGO_HOST, MongoDBTestCase.database_name)
        mongoengine.disconnect(alias="mongo")
        self.db = mongoengine.connect(host=MONGO_DATABASE_HOST, alias="mongo")

    def tearDown(self):
        self.db.drop_database(MongoDBTestCase.database_name)
        self.db.close()

def user_has_any_perms(user, perms):
    return any([user.has_perm(_) for _ in perms])

def build_choices(queryset, id_field, name_field):
    return [(getattr(_, id_field).lower(), getattr(_, name_field)) for _ in queryset]

def build_tree_list(published_only = True):
    return build_choices(TreeInfo.get_all(published_only), "name", "display_name")

def build_objectives(published_only = True):
    return build_choices(BonsaiObjective.get_all(published_only), "short_name", "display_name")

def build_techniques(published_only = True):
    return build_choices(BonsaiTechnique.get_all(published_only), "short_name", "display_name")

def build_when(published_only = True):
    return build_choices(BonsaiWhen.get_all(published_only), "short_name", "display_name")

def build_periods():
    return [(None, "Undefined")] + [(f"{periodid[0]}_{periodid[1]}", f"{periodname[0]} {periodname[1]}") for periodid, periodname in get_periods()]

def build_technique_categories():
    return [(_.lower(), _) for _ in get_technique_categories()]
