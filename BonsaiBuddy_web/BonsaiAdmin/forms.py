from functools import partial

from BonsaiAdvice.models import BonsaiObjective, BonsaiTechnique, BonsaiStage, periodid_to_name
from BonsaiBuddy.forms import CreateUpdateForm
from BonsaiBuddy.widgets import SelectPlaceholder, TagifyWidget
from django import forms
from TreeInfo.models import TechniqueMapper, TreeInfo
from utils import (build_objectives, build_periods, build_technique_categories,
                   build_techniques, build_tree_list, build_stage)
from django.utils.safestring import mark_safe


class TreeInfoForm(CreateUpdateForm):
    display_name = forms.CharField(max_length=200, label="Tree name")
    name = forms.CharField(widget=forms.HiddenInput, required=False)
    latin_name = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea, required=False)
    placement = forms.CharField(widget=forms.Textarea, required=False)
    watering = forms.CharField(widget=forms.Textarea, required=False)
    fertilizing = forms.CharField(widget=forms.Textarea, required=False)
    pruning_wiring = forms.CharField(widget=forms.Textarea, required=False)
    repotting = forms.CharField(widget=forms.Textarea, required=False)
    propagation = forms.CharField(widget=forms.Textarea, required=False)
    pests = forms.CharField(widget=forms.Textarea, required=False)
    published = forms.BooleanField(initial=False, required=False)

    def clean_name(self):
        # Name is just the lower case display name
        display_name = self.cleaned_data.get("display_name")
        return display_name.lower()

    def update_object(self):
        pk = self.cleaned_data["name"]
        original = TreeInfo.get(pk)
        original.update(**self.cleaned_data)

    def create_object(self):
        q = TreeInfo(**self.cleaned_data)
        q.save()

    def delete_object(self):
        pk = self.cleaned_data["name"]
        original = TreeInfo.get(pk)
        original.delete()


class BonsaiTechniqueForm(CreateUpdateForm):
    short_name = forms.CharField(max_length=200)
    display_name = forms.CharField(max_length=200)
    category = forms.ChoiceField(
        choices=build_technique_categories(), widget=SelectPlaceholder)
    sequence = forms.IntegerField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "description-lg"}), required=False)
    published = forms.BooleanField(initial=False, required=False)

    def update_object(self):
        pk = self.cleaned_data["short_name"]
        original = BonsaiTechnique.get(pk)
        original.update(**self.cleaned_data)

    def create_object(self):
        q = BonsaiTechnique(**self.cleaned_data)
        q.save()

    def delete_object(self):
        pk = self.cleaned_data["short_name"]
        original = BonsaiTechnique.get(pk)
        original.delete()


class BonsaiObjectiveForm(CreateUpdateForm):
    short_name = forms.CharField(max_length=200)
    display_name = forms.CharField(max_length=200)
    sequence = forms.IntegerField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "description-lg"}), required=False)
    published = forms.BooleanField(initial=False, required=False)

    def update_object(self):
        pk = self.cleaned_data["short_name"]
        original = BonsaiObjective.get(pk)
        original.update(**self.cleaned_data)

    def create_object(self):
        q = BonsaiObjective(**self.cleaned_data)
        q.save()

    def delete_object(self):
        pk = self.cleaned_data["short_name"]
        original = BonsaiObjective.get(pk)
        original.delete()


class BonsaiStageForm(CreateUpdateForm):
    short_name = forms.CharField(max_length=200)
    display_name = forms.CharField(max_length=200)
    global_period = forms.MultipleChoiceField(choices=build_periods(), required=False, widget=TagifyWidget)
    sequence = forms.IntegerField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "description-lg"}), required=False)
    published = forms.BooleanField(initial=False, required=False)

    def update_object(self):
        pk = self.cleaned_data["short_name"]
        original = BonsaiStage.get(pk)
        original.update(**self.cleaned_data)

    def create_object(self):
        q = BonsaiStage(**self.cleaned_data)
        q.save()

    def delete_object(self):
        pk = self.cleaned_data["short_name"]
        original = BonsaiStage.get(pk)
        original.delete()


class TechniqueAssociationForm(forms.Form):
    class Media:
        js = ("https://code.jquery.com/jquery-3.6.4.min.js",
              "BonsaiAdmin/dyn_form.js",)

    tree_name_hidden = forms.CharField(widget=forms.HiddenInput())
    oid = forms.CharField(widget=forms.HiddenInput(), required=False)
    technique = forms.ChoiceField(
        choices=partial(build_techniques, published_only=False), widget=SelectPlaceholder)
    objective = forms.ChoiceField(
        choices=partial(build_objectives, published_only=False), widget=SelectPlaceholder)
    stage = forms.MultipleChoiceField(
        choices=partial(build_stage, published_only=False), required=False, widget=TagifyWidget)
    period = forms.MultipleChoiceField(
        choices=build_periods, required=False, widget=TagifyWidget)
    comment = forms.CharField(widget=forms.Textarea, required=False)

    def create_update(self):
        tree = TreeInfo.get(self.cleaned_data['tree_name_hidden'])
        technique_id = BonsaiTechnique.get(self.cleaned_data['technique']).id
        objective_id = BonsaiObjective.get(self.cleaned_data['objective']).id
        stage_id = [None if not stage else BonsaiStage.get(
            stage).id for stage in self.cleaned_data['stage']]
        period = self.cleaned_data['period'] if len(
            self.cleaned_data['period']) > 0 else []
        if self.cleaned_data["oid"]:
            # Modifying an existing entry
            oid = self.cleaned_data['oid']
            mapper = tree.techniques.get(oid=oid)
            if self.cleaned_data["DELETE"]:
                # Requires deletion of the entry
                tree.techniques.remove(mapper)
            else:
                mapper.technique = technique_id
                mapper.objective = objective_id
                mapper.stage = stage_id
                mapper.period = period
                mapper.comment = self.cleaned_data['comment']
        else:
            # Creating a new entry
            mapper = TechniqueMapper(
                technique=technique_id, objective=objective_id, stage=stage_id, period=period, comment = self.cleaned_data["comment"])
            tree.techniques.append(mapper)
        tree.save()

    def summary(self):
        if not "objective" in self.initial:
            return mark_safe("")
        stage = self.initial["objective"]
        technique = self.initial["technique_name"]
        timing = ",".join([periodid_to_name(_) for _ in self.initial["period"]])
        if self.initial["stage"]:
            timing += " (" + ",".join(self.initial['stage']) + ")"
        return mark_safe(f"<div style='width:30ch;'>&nbsp;{technique}</div> - <div style='width:15ch;'>&nbsp;{stage}</div> - {timing}")