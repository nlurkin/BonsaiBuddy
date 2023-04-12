from django import forms
from TreeInfo.models import TreeInfo

class CreateForm(forms.Form):
    name = forms.CharField(max_length=200, label="Tree name")
    latin_name = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea, required=False)
    published = forms.BooleanField(initial=False, required=False)

    def create(self):
        q = TreeInfo(**self.cleaned_data)
        q.save()