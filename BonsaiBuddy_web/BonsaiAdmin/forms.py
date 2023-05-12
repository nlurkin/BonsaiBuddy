from django import forms
from TreeInfo.models import TreeInfo, TechniqueMapper
from BonsaiAdvice.models import BonsaiTechnique, BonsaiObjective, BonsaiWhen
from utils import build_technique_categories, build_periods, build_tree_list, build_techniques, build_objectives, build_when
from BonsaiBuddy.widgets import SelectPlaceholder

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
    category = forms.ChoiceField(choices=build_technique_categories(), widget=SelectPlaceholder)
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
    global_period = forms.ChoiceField(choices=build_periods(), required=False, widget=SelectPlaceholder)
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
    class Media:
        js = ("https://code.jquery.com/jquery-3.6.4.min.js", "BonsaiAdmin/dyn_form.js",)

    tree_name = forms.ChoiceField(choices=build_tree_list(), disabled=True, required=False)
    tree_name_hidden = forms.CharField(widget=forms.HiddenInput())
    oid = forms.CharField(widget=forms.HiddenInput(), required=False)
    technique = forms.ChoiceField(choices=build_techniques(), widget=SelectPlaceholder)
    objective = forms.ChoiceField(choices=build_objectives(), widget=SelectPlaceholder)
    when = forms.ChoiceField(choices=build_when(), required=False, widget=SelectPlaceholder)
    period = forms.ChoiceField(choices=build_periods(), required=False)

    def create_update(self):
        tree  = TreeInfo.get(self.cleaned_data['tree_name_hidden'])
        technique_id = BonsaiTechnique.get(self.cleaned_data['technique']).id
        objective_id = BonsaiObjective.get(self.cleaned_data['objective']).id
        when_id = None if not self.cleaned_data['when'] else BonsaiWhen.get(self.cleaned_data['when']).id
        period = [self.cleaned_data['period']] if len(self.cleaned_data['period'])>0 else []
        if self.cleaned_data["oid"]:
            # Modifying an existing entry
            oid = self.cleaned_data['oid']
            mapper = tree.techniques.get(oid=oid)
            if self.cleaned_data["DELETE"]:
                # Requires deletion of the entry
                tree.techniques.remove(mapper)
            else:
                mapper.technique=technique_id
                mapper.objective=objective_id
                mapper.when=when_id
                mapper.period=period
        else:
            # Creating a new entry
            mapper = TechniqueMapper(technique = technique_id, objective=objective_id, when=when_id, period=period)
            tree.techniques.append(mapper)
        tree.save()