from django import forms
from TreeInfo.models import TreeInfo
import calendar

def build_tree_list():
    return [(_.name.lower(), _.name) for _ in TreeInfo.objects.all()]

def build_periods():
    return [(_, f"{calendar.month_abbr[(_*2)+1]}-{calendar.month_abbr[(_+1)*2]}") for _ in range(6)]
class AdviceConfigForm(forms.Form):
    tree           = forms.CharField(label="Tree species", widget=forms.Select(choices=build_tree_list()))
    objective      = forms.CharField(label="Objective")
    period         = forms.CharField(label="Period", widget=forms.Select(choices=build_periods()))
    when           = forms.CharField(label="When")


