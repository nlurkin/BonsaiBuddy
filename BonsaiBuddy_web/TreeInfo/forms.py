from django import forms
from .models import Question

class CreateForm(forms.Form):
    question_text = forms.CharField(max_length=200, widget=forms.Textarea)
    pub_date = forms.DateTimeField(input_formats=['%d/%m/%Y'])

    def create(self):
        q = Question(**self.cleaned_data)
        q.save()