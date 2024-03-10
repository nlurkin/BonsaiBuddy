from django import forms
from BonsaiBuddy.widgets import TagifyWidget, SelectPlaceholder
from utils import build_tree_list, build_objectives, build_periods, build_stage


class ReqAdviceInfo():
    def __init__(self, query, serialized_data=None):
        if serialized_data:
            self.tree = serialized_data['tree']
            self.objective = serialized_data['objective']
            self.period = serialized_data['period'] if 'period' in serialized_data else None
            self.stage = serialized_data['stage'] if 'stage' in serialized_data else None
            self.oid = None
        else:
            self.tree = query.get("tree", None)
            self.objective = query.get("objective", None)
            self.period = query.get("period", None)
            self.stage = query.get("stage", None)
            self.oid = query.get("oid", None)
            if self.stage:
                self.stage = self.stage.split(",")

    def is_complete(self):
        # Requires tree, objective, and either of period or stage, or just oid
        descriptors = (self.tree is not None and self.objective is not None and (
            self.period is not None or self.stage is not None))
        oid = self.oid is not None
        return (descriptors or oid)


class AdviceConfigForm(forms.Form):
    error_messages = {
        "missing_timing": "At least one of Period or Stage needs to be provided.",
    }

    tree = forms.ChoiceField(
        label="Tree species", choices=build_tree_list(), widget=SelectPlaceholder)
    objective = forms.ChoiceField(
        label="Objective", choices=build_objectives(), widget=TagifyWidget(maxTags=1))
    period = forms.ChoiceField(
        label="Period", choices=build_periods(), required=False)
    stage = forms.MultipleChoiceField(
        label="Stage", choices=build_stage(), widget=TagifyWidget, required=False)
    is_submitted = forms.BooleanField(
        initial=True, widget=forms.HiddenInput, required=False)

    def clean_period(self):
        # Check that at least one of period or stage has been provided
        period = self.cleaned_data.get("period")
        stage = self.cleaned_data.get("stage")
        if not period and not stage:
            raise forms.ValidationError(
                self.error_messages["missing_timing"], code="missing_timing")
