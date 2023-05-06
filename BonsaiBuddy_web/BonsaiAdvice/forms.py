from django import forms
from TreeInfo.models import TreeInfo

def build_tree_list():
    return [(_.name.lower(), _.name) for _ in TreeInfo.objects.all()]

class AdviceConfigForm(forms.Form):
    tree           = forms.CharField(label="Tree species", widget=forms.Select(choices=build_tree_list()))
    objective      = forms.CharField(label="Objective")
    period         = forms.CharField(label="Period")
    when           = forms.CharField(label="When")

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

