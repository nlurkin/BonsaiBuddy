from django import forms
from BonsaiBuddy.widgets import TagifyWidget, SelectPlaceholder
from utils import build_tree_list, build_objectives, build_periods, build_when

class ReqAdviceInfo():
        def __init__(self, query):
            self.tree = query.get("tree", None)
            self.objective = query.get("objective", None)
            self.period = query.get("period", None)
            self.when = query.get("when", None)

        def is_complete(self):
            # Requires tree, objective, and either of period or when
            return (not self.tree or not self.objective or not (self.period or self.when))

class AdviceConfigForm(forms.Form):
    tree           = forms.ChoiceField(label="Tree species", choices=build_tree_list(), widget=SelectPlaceholder)
    objective      = forms.ChoiceField(label="Objective", choices=build_objectives(), widget=TagifyWidget(maxTags=1))
    period         = forms.ChoiceField(label="Period", choices=build_periods(), required=False)
    when           = forms.MultipleChoiceField(label="When", choices=build_when(), widget=TagifyWidget, required=False)
    is_submitted   = forms.BooleanField(initial=True, widget=forms.HiddenInput, required=False)
