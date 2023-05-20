from django import forms


class CreateUpdateForm(forms.Form):
    update = forms.BooleanField(initial=False, widget=forms.HiddenInput, required=False)

    def create_update(self, **kwargs):
        update_val = self.cleaned_data["update"]
        del self.cleaned_data["update"]
        if update_val:
            self.update_object(**kwargs)
        else:
            self.create_object(**kwargs)
