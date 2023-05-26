from django.db import models
from django.utils import timezone
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

def month_to_period(month):
    # TODO: this is applicable only to the northern hemisphere, excluding tropical regions
    period = []
    qualifier = []
    if month >= 3 and month <=6:
        # Spring: March-June
        period.append(0)
        qualifier.append(None)
        if month <=4:
            # Early: March, April
            qualifier[-1] = 0
        else:
            # Late : May, June
            qualifier[-1] = 1
    if month >= 7 and month <= 9:
        # Summer: July-September
        period.append(1)
        qualifier.append(None)
        if month == 7:
            # Early: July
            qualifier[-1] = 0
        elif month == 9:
            # Late: September
            qualifier[-1] = 1
    if month >= 9 and month <= 11:
        # Autumn: September-November
        if month <= 10:
            # Early: September, October
            period.append(2)
            qualifier.append(0)
        if month <= 10:
            # Late : October, November
            period.append(2)
            qualifier.append(1)
    if month >= 12 or month <= 3:
        # Winter: December, Mid-March
        period.append(3)
        qualifier.append(None)
        if month == 12:
            # Early: December,
            qualifier[-1] = 0
        if month >= 2:
            # Late: February, March
            qualifier[-1] = 1
    # Undefined: August, January
    return [f"{q}_{p}" for p,q in zip(period, qualifier)]

def timing_matches(when, period, available_when, available_period):
    # Returns true if both when and period are compatible with the available lists, unless the corresponding list is empty
    # This is considered as "doesn't matter"
    # Same think in the opposite direction, if either of when or period is None, it is considered as "doesn't matter"
    # Compatible is defined as: any of is in the available
    if when is not None:
        if type(when) not in (list, set, tuple):
            when = [when]
        when = set(when)
        when_cond = len(available_when)==0 or not when.isdisjoint(set(available_when))
    if period is not None:
        if type(period) not in (list, set, tuple):
            period = [period]
        period = set(period)
        period_cond = len(available_period)==0 or not period.isdisjoint(set(available_period))

    if when and period:
        return when_cond and period_cond
    elif when and not period:
        return when_cond
    elif not when and period:
        return period_cond

def make_timing(whens, periods):
    return {"when": [_.display_name for _ in whens], "period": [periodid_to_name(_) for _ in periods]}

def get_current_period():
    curr_month = timezone.now().month
    return month_to_period(curr_month)

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
    def get_all(published_only=True, category=None):
        objects = BonsaiTechnique.objects
        if published_only:
            objects = objects.filter(published=True)
        if category:
            objects = objects.filter(category=category)

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
