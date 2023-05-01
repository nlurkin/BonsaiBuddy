from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import UserProfile

class CustomUserCreationForm(forms.Form):
    error_messages = {
        "password_mismatch": "The two password fields didn't match.",
        "username_exists": "The selected username already exists.",
    }
    username = forms.CharField()
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    def __init__(self, *args, **kwargs):
        self.instance = UserProfile()
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def clean_username(self):
        """Reject usernames that differ only in case."""
        username = self.cleaned_data.get("username")
        if (username and len(UserProfile.objects(username__iexact=username))>0):
            raise ValidationError(self.error_messages["username_exists"], code="username_exists")
        else:
            return username

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password2")
        user = UserProfile(username=username)
        user.create_user(password)
        return username, password

class UpdateUserProfileForm(forms.Form):
    country = forms.CharField(widget=forms.Select(choices=[("unknown", "Unknown"), ("belgium", "Belgium")]))

    def save(self, username):
        user = UserProfile.objects.get(username=username)
        user.country = self.cleaned_data.get("country")
        user.save()
