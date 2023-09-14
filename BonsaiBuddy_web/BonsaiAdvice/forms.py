from django import forms
from BonsaiBuddy.widgets import TagifyWidget, SelectPlaceholder
from utils import build_tree_list, build_objectives, build_periods, build_when

class ReqAdviceInfo():
        def __init__(self, query):
            self.tree = query.get("tree", None)
            self.objective = query.get("objective", None)
            self.period = query.get("period", None)
            self.when = query.get("when", None)
            self.oid = query.get("oid", None)
            if self.when:
                 self.when = self.when.split(",")

        def is_complete(self):
            # Requires tree, objective, and either of period or when, or just oid
            descriptors = (self.tree is not None and self.objective is not None and (self.period is not None or self.when is not None))
            oid = self.oid is not None
            return (descriptors or oid)

class AdviceConfigForm(forms.Form):
    error_messages = {
        "missing_timing": "At least one of Period or When needs to be provided.",
    }

    tree           = forms.ChoiceField(label="Tree species", choices=build_tree_list(), widget=SelectPlaceholder)
    objective      = forms.ChoiceField(label="Objective", choices=build_objectives(), widget=TagifyWidget(maxTags=1))
    period         = forms.ChoiceField(label="Period", choices=build_periods(), required=False)
    when           = forms.MultipleChoiceField(label="When", choices=build_when(), widget=TagifyWidget, required=False)
    is_submitted   = forms.BooleanField(initial=True, widget=forms.HiddenInput, required=False)

    def clean_period(self):
         # Check that at least one of period or when has been provided
         period = self.cleaned_data.get("period")
         when = self.cleaned_data.get("when")
         if not period and not when:
              raise forms.ValidationError(self.error_messages["missing_timing"], code="missing_timing")