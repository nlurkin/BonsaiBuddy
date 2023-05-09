from django import forms
from BonsaiBuddy.widgets import TagifyWidget
from utils import build_tree_list, build_objectives, build_periods, build_when

class AdviceConfigForm(forms.Form):
    tree           = forms.ChoiceField(label="Tree species", choices=build_tree_list())
    objective      = forms.ChoiceField(label="Objective", choices=build_objectives(), widget=TagifyWidget(maxTags=1))
    period         = forms.ChoiceField(label="Period", choices=build_periods(), required=False)
    when           = forms.MultipleChoiceField(label="When", choices=build_when(), widget=TagifyWidget, required=False)
    is_submitted   = forms.BooleanField(initial=True, widget=forms.HiddenInput, required=False)
