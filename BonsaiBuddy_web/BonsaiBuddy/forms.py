from django import forms


class CreateUpdateForm(forms.Form):
    update = forms.BooleanField(initial=False, widget=forms.HiddenInput, required=False)
    delete = forms.BooleanField(initial=False, required=False)


    def create_update(self, **kwargs):
        update_val = self.cleaned_data["update"]
        delete_val = self.cleaned_data["delete"]
        del self.cleaned_data["update"]
        del self.cleaned_data["delete"]
        if update_val and delete_val:
            self.delete_object(**kwargs)
        elif update_val and not delete_val:
            self.update_object(**kwargs)
        else:
            self.create_object(**kwargs)
