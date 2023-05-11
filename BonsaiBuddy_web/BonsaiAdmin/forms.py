from django import forms
from TreeInfo.models import TreeInfo
from BonsaiAdvice.models import BonsaiTechnique, BonsaiObjective, BonsaiWhen
from utils import build_technique_categories, build_periods, build_tree_list, build_techniques, build_objectives, build_when

class TreeInfoForm(forms.Form):
    name           = forms.CharField(max_length=200, label="Tree name")
    latin_name     = forms.CharField(max_length=200)
    description    = forms.CharField(widget=forms.Textarea, required=False)
    placement      = forms.CharField(widget=forms.Textarea, required=False)
    watering       = forms.CharField(widget=forms.Textarea, required=False)
    fertilizing    = forms.CharField(widget=forms.Textarea, required=False)
    pruning_wiring = forms.CharField(widget=forms.Textarea, required=False)
    repotting      = forms.CharField(widget=forms.Textarea, required=False)
    propagation    = forms.CharField(widget=forms.Textarea, required=False)
    pests          = forms.CharField(widget=forms.Textarea, required=False)
    published      = forms.BooleanField(initial=False, required=False)
    update         = forms.BooleanField(initial=False, widget=forms.HiddenInput, required=False)

    def create_update(self):
        update_val = self.cleaned_data["update"]
        del self.cleaned_data["update"]
        if update_val:
            pk = self.cleaned_data["name"]
            original = TreeInfo.get(pk)
            original.update(**self.cleaned_data)
        else:
            q = TreeInfo(**self.cleaned_data)
            q.save()

class BonsaiTechniqueForm(forms.Form):
    short_name = forms.CharField(max_length=200)
    display_name = forms.CharField(max_length=200)
    category = forms.ChoiceField(choices=build_technique_categories())
    description = forms.CharField(widget=forms.Textarea, required=False)
    published = forms.BooleanField(initial=False, required=False)
    update = forms.BooleanField(initial=False, widget=forms.HiddenInput, required=False)

    def create_update(self):
        update_val = self.cleaned_data["update"]
        del self.cleaned_data["update"]
        if update_val:
            pk = self.cleaned_data["short_name"]
            original = BonsaiTechnique.get(pk)
            original.update(**self.cleaned_data)
        else:
            q = BonsaiTechnique(**self.cleaned_data)
            q.save()

class BonsaiObjectiveForm(forms.Form):
    short_name = forms.CharField(max_length=200)
    display_name = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea, required=False)
    published = forms.BooleanField(initial=False, required=False)
    update = forms.BooleanField(initial=False, widget=forms.HiddenInput, required=False)

    def create_update(self):
        update_val = self.cleaned_data["update"]
        del self.cleaned_data["update"]
        if update_val:
            pk = self.cleaned_data["short_name"]
            original = BonsaiObjective.get(pk)
            original.update(**self.cleaned_data)
        else:
            q = BonsaiObjective(**self.cleaned_data)
            q.save()

class BonsaiWhenForm(forms.Form):
    short_name = forms.CharField(max_length=200)
    display_name = forms.CharField(max_length=200)
    global_period = forms.ChoiceField(choices=build_periods(), required=False)
    description = forms.CharField(widget=forms.Textarea, required=False)
    published = forms.BooleanField(initial=False, required=False)
    update = forms.BooleanField(initial=False, widget=forms.HiddenInput, required=False)

    def create_update(self):
        update_val = self.cleaned_data["update"]
        del self.cleaned_data["update"]
        if update_val:
            pk = self.cleaned_data["short_name"]
            original = BonsaiWhen.get(pk)
            original.update(**self.cleaned_data)
        else:
            q = BonsaiWhen(**self.cleaned_data)
            q.save()

class TechniqueAssociationForm(forms.Form):
    tree_name = forms.ChoiceField(choices=build_tree_list(), disabled=True, required=False)
    tree_name_hidden = forms.CharField(widget=forms.HiddenInput())
    technique = forms.ChoiceField(choices=build_techniques())
    objective = forms.ChoiceField(choices=build_objectives())
    when = forms.ChoiceField(choices=build_when(), required=False)
    period = forms.ChoiceField(choices=build_periods(), required=False)
