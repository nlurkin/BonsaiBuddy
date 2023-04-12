from django.http import Http404
from django.test import TestCase
import mongoengine
from BonsaiBuddy import settings

def get_object_or_404(klass, pk):
    try:
        obj = klass.objects.get(pk=pk)
    except klass.DoesNotExist:
        raise Http404(f"{klass.__name__} does not exist")
    return obj


class MongoDBTestCase(TestCase):
    database_name = "test_database"
    def setUp(self):
        MONGO_DATABASE_HOST = 'mongodb+srv://%s:%s@%s/%s?ssl=true' % (
            settings.MONGO_USER, settings.MONGO_PASS, settings.MONGO_HOST, MongoDBTestCase.database_name)
        mongoengine.disconnect(alias="mongo")
        self.db = mongoengine.connect(host=MONGO_DATABASE_HOST, alias="mongo")

    def tearDown(self):
        self.db.drop_database(MongoDBTestCase.database_name)
        self.db.close()
