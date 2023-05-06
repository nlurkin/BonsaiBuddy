from django import forms
from TreeInfo.models import TreeInfo

def build_tree_list():
    return [(_.name.lower(), _.name) for _ in TreeInfo.objects.all()]

class AdviceConfigForm(forms.Form):
    tree           = forms.CharField(label="Tree species", widget=forms.Select(choices=build_tree_list()))
    objective      = forms.CharField(label="Objective")
    period         = forms.CharField(label="Period")
    when           = forms.CharField(label="When")


