from django import forms
from TreeInfo.models import TreeInfo
from BonsaiAdvice.models import BonsaiTechnique, BonsaiObjective, BonsaiWhen

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
            original = TreeInfo.objects.get(name=pk)
            original.update(**self.cleaned_data)
        else:
            q = TreeInfo(**self.cleaned_data)
            q.save()

def build_technique_category():
    return [(_.lower(), _) for _ in ["Pruning", "Defoliation", "Deadwood"]]

class BonsaiTechniqueForm(forms.Form):
    short_name = forms.CharField(max_length=200)
    display_name = forms.CharField(max_length=200)
    category = forms.CharField(widget=forms.Select(choices=build_technique_category()))
    description = forms.CharField(widget=forms.Textarea, required=False)
    published = forms.BooleanField(initial=False, required=False)
    update = forms.BooleanField(initial=False, widget=forms.HiddenInput, required=False)

    def create_update(self):
        update_val = self.cleaned_data["update"]
        del self.cleaned_data["update"]
        if update_val:
            pk = self.cleaned_data["short_name"]
            original = BonsaiTechnique.objects.get(short_name=pk)
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
            original = BonsaiObjective.objects.get(short_name=pk)
            original.update(**self.cleaned_data)
        else:
            q = BonsaiObjective(**self.cleaned_data)
            q.save()

class BonsaiWhenForm(forms.Form):
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
            original = BonsaiWhen.objects.get(short_name=pk)
            original.update(**self.cleaned_data)
        else:
            q = BonsaiWhen(**self.cleaned_data)
            q.save()

