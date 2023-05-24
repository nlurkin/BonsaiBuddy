from django import forms


class CreateUpdateForm(forms.Form):
    update = forms.BooleanField(initial=False, widget=forms.HiddenInput, required=False)
    delete = forms.BooleanField(initial=False, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_order = []
        for field in self.declared_fields:
            if field == "delete":
                continue
            field_order.append(field)
        field_order.append("delete")

        self.order_fields(field_order)

    def create_update(self, **kwargs):
        '''
        Returns true if the object is valid after this method
        '''
        update_val = self.cleaned_data["update"]
        delete_val = self.cleaned_data["delete"]
        del self.cleaned_data["update"]
        del self.cleaned_data["delete"]
        if update_val and delete_val:
            self.delete_object(**kwargs)
            return False
        elif update_val:
            self.update_object(**kwargs)
        else:
            self.create_object(**kwargs)
        return True
