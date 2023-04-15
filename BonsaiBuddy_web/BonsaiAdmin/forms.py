from django import forms
from TreeInfo.models import TreeInfo

class TreeInfoForm(forms.Form):
    name = forms.CharField(max_length=200, label="Tree name")
    latin_name = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea, required=False)
    published = forms.BooleanField(initial=False, required=False)
    update = forms.BooleanField(initial=False, widget=forms.HiddenInput, required=False)

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

