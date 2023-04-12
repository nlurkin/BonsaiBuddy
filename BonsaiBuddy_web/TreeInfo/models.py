import mongoengine
import datetime
from django.utils import timezone
from django.urls import reverse
from django.db import models

class Question(mongoengine.Document):
    question_text = mongoengine.StringField(max_length=200)
    pub_date = mongoengine.DateTimeField("date published")
    meta = {'db_alias': 'mongo'}

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    @property
    def choices(self):
        return Choice.objects(question=self).all()

    def get_absolute_url(self):
        return reverse('TreeInfo:detail', kwargs={'pk': self.pk})



class Choice(mongoengine.Document):
    question = mongoengine.ReferenceField(Question, reverse_delete_rule=mongoengine.CASCADE)
    choice_text = mongoengine.StringField(max_length=200)
    votes = mongoengine.IntField(default=0)
    meta = {'db_alias': 'mongo'}

    def __str__(self):
        return self.choice_text

class MyModel(models.Model):
    class Meta:
        permissions = (
            ('change_content', 'Content administrators'),
        )

