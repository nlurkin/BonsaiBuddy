from django import forms
from TreeInfo.models import TreeInfo

def build_tree_list():
    return [(_.name.lower(), _.name) for _ in TreeInfo.objects.all()]

def build_periods():
    seasons = ["Spring", "Summer", "Autumn", "Winter"]
    subsection = ["Early", "Late"]
    return [(f"{iseason}_{isub}", f"{sub} {season}") for isub, sub in enumerate(subsection) for iseason, season in enumerate(seasons)]

class AdviceConfigForm(forms.Form):
    tree           = forms.ChoiceField(label="Tree species", choices=build_tree_list())
    objective      = forms.CharField(label="Objective")
    period         = forms.ChoiceField(label="Period", choices=[(None, "Undefined")] + build_periods())
    when           = forms.CharField(label="When")


