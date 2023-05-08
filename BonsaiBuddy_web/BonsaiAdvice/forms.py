from django import forms
from TreeInfo.models import TreeInfo
from .models import BonsaiWhen, BonsaiObjective, get_periods
from BonsaiBuddy.widgets import TagifyWidget

def build_tree_list():
    return [(_.name.lower(), _.name) for _ in TreeInfo.get_all()]

def build_periods():
    return [(None, "Undefined")] + [(f"{periodid[0]}_{periodid[1]}", f"{periodname[0]} {periodname[1]}") for periodid, periodname in get_periods()]

def build_objectives():
    return [(_.short_name, _.display_name) for _ in BonsaiObjective.get_all()]

def build_when():
    return [(_.short_name, _.display_name) for _ in BonsaiWhen.get_all()]

class AdviceConfigForm(forms.Form):
    tree           = forms.ChoiceField(label="Tree species", choices=build_tree_list())
    objective      = forms.ChoiceField(label="Objective", choices=build_objectives(), widget=TagifyWidget(maxTags=1))
    period         = forms.ChoiceField(label="Period", choices=build_periods(), required=False)
    when           = forms.MultipleChoiceField(label="When", choices=build_when(), widget=TagifyWidget, required=False)
