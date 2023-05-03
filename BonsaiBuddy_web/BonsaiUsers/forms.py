from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import UserProfile
import bcrypt
import pycountry

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

def build_country_list():
    countries = [(country.name.lower(), country.name) for country in sorted(pycountry.countries, key= lambda x: x.name)]
    countries.insert(0, ("unknown", "Unknown"))
    return countries

class UpdateUserProfileForm(forms.Form):

    country = forms.CharField(widget=forms.Select(choices=build_country_list()))

    def save(self, username):
        user = UserProfile.get_user(username)
        user.country = self.cleaned_data.get("country")
        user.save()

class ModifyPasswordForm(forms.Form):
    error_messages = {
        "password_mismatch": "The two password fields didn't match.",
        "username_exists": "The selected username already exists.",
    }
    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "old-password"}),
        help_text="Old password"
    )
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
        self.user = kwargs.pop("user")
        print(self.user)
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

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if old_password:
            up = UserProfile.get_user(self.user.username)
            if not bcrypt.checkpw(old_password.encode("utf-8"), up.password):
                self.add_error("old_password", "The old password is incorrect")
        return old_password


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

    def save(self, username):
        password = self.cleaned_data.get("password2")
        user = UserProfile.get_user(username)
        user.update_password(password)
