import bcrypt
from BonsaiAdvice.models import BonsaiObjective
from BonsaiBuddy.forms import CreateUpdateForm
from BonsaiBuddy.widgets import SelectPlaceholder
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from TreeInfo.models import TreeInfo
from utils import build_objectives, build_tree_list

from .models import TreeCollection, UserProfile, build_country_list


class PasswordValidationClass():
    error_messages = {
        "password_mismatch": "The two password fields didn't match.",
    }
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
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            try:
                password_validation.validate_password(password, None)
            except ValidationError as error:
                self.add_error("password2", error)
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(self.error_messages["password_mismatch"], code="password_mismatch")


class CustomUserCreationForm(PasswordValidationClass, forms.Form):
    error_messages = {**PasswordValidationClass.error_messages,
        "username_exists": "The selected username already exists.",
    }
    username = forms.CharField()

    def clean_username(self):
        """Reject usernames that differ only in case."""
        username = self.cleaned_data.get("username")
        if (username and len(UserProfile.objects(username__iexact=username))>0):
            raise ValidationError(self.error_messages["username_exists"], code="username_exists")
        else:
            return username

    def save(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password2")
        user = UserProfile(username=username)
        user.create_user(password)
        return user

class ModifyPasswordForm(PasswordValidationClass, forms.Form):
    error_messages = {**PasswordValidationClass.error_messages,
        "incorrect_old": "The old password is incorrect.",
    }
    old_password = forms.CharField(
        label="Old password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "old-password"}),
        help_text="Old password"
    )

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if old_password:
            up = UserProfile.get_user(self.user.username)
            if not bcrypt.checkpw(old_password.encode("utf-8"), up.password):
                raise ValidationError("incorrect_old", self.error_messages["incorrect_old"])
        return old_password

    def save(self, username):
        password = self.cleaned_data.get("password2")
        user = UserProfile.get_user(username)
        user.update_password(password)


class UpdateUserProfileForm(forms.Form):
    country = forms.ChoiceField(choices=build_country_list(), widget=SelectPlaceholder)

    def save(self, username):
        user = UserProfile.get_user(username)
        user.country = self.cleaned_data.get("country")
        user.save()


class MyTreeForm(CreateUpdateForm):
    oid            = forms.CharField(widget=forms.HiddenInput, required=False)
    tree_name      = forms.ChoiceField(choices=build_tree_list())
    objective      = forms.ChoiceField(choices=build_objectives())

    def get_refs_dict(self):
        return {"treeReference": TreeInfo.get(self.cleaned_data["tree_name"]),
                "objective": BonsaiObjective.get(self.cleaned_data["objective"])}

    def update_object(self, username):
        profile = UserProfile.get_user(username)
        tree = profile.get_my_tree(self.cleaned_data["oid"])
        refs_dict = self.get_refs_dict()
        tree.treeReference = refs_dict["treeReference"]
        tree.objective = refs_dict["objective"]
        profile.save()

    def create_object(self, username):
        profile = UserProfile.get_user(username)
        tree = TreeCollection(**self.get_refs_dict())
        profile.my_trees.append(tree)
        profile.save()