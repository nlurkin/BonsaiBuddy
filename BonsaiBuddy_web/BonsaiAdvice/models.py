from django.db import models
import mongoengine

class AdvicePermissionModel(models.Model):
    class Meta:
        permissions = (
            ('change_content', 'Content administrators'),
        )


def get_periods():
    seasons = ["Spring", "Summer", "Autumn", "Winter"]
    subsection = ["Early", "Late"]
    return [((isub, iseason), (sub, season)) for isub, sub in enumerate(subsection) for iseason, season in enumerate(seasons)]

def periodid_to_name(periodid):
    if isinstance(periodid, str):
        periodid = tuple([int(_) for _ in periodid.split("_")])
    if len(periodid) != 2:
        return None
    d = {pid: " ".join(pname) for pid, pname in get_periods()}
    if periodid in d:
        return d[periodid]
    return None

def get_technique_categories():
    return ["Pruning", "Defoliation", "Deadwood"]

def timing_matches(when, period, available_when, available_period):
    # Returns true if both when and period are in the available lists, uniless the corresponding list is empty
    # This is considered as "doesn't matter"
    # Same think in the opposite direction, if either of when or period is None, it is considered as "doesn't matter"
    when_cond = (len(available_when)==0 or when in available_when)
    period_cond = (len(available_period)==0 or period in available_period)
    if when and period:
        return when_cond and period_cond
    elif when and not period:
        return when_cond
    elif not when and period:
        return period_cond

def make_timing(whens, periods):
    return {"when": [_.display_name for _ in whens], "period": [periodid_to_name(_) for _ in periods]}

class BonsaiTechnique(mongoengine.Document):
    short_name = mongoengine.StringField(max_length=200, required=True, index=True, unique=True)
    display_name = mongoengine.StringField(max_length=200)
    description = mongoengine.StringField()
    category = mongoengine.StringField(max_length=200)
    published = mongoengine.BooleanField(default=False)

    meta = {'db_alias': 'mongo', "indexes": ["$short_name"]}

    def __str__(self):
        return self.short_name

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
        return self.short_name

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
    global_period = mongoengine.ListField(choices=[f"{_[0][0]}_{_[0][1]}" for _ in get_periods()])
    published = mongoengine.BooleanField(default=False)

    meta = {'db_alias': 'mongo', "indexes": ["$short_name"]}

    def global_period_name(self):
        return periodid_to_name(self.global_period)

    def __str__(self):
        return self.short_name

    @staticmethod
    def get_all(published_only=True):
        objects = BonsaiWhen.objects
        if published_only:
            objects = objects.filter(published=True)
        return objects.order_by("short_name")

    @staticmethod
    def get(short_name):
        return BonsaiWhen.objects.get(short_name=short_name)
