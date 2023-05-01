from django.contrib.auth.backends import BaseBackend
from BonsaiUsers.models import User, UserProfile
from django.utils import timezone
import bcrypt


class DjangoBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        # Check the user profile exists
        try:
            up = UserProfile.objects.get(username=username)
            # Check the password
            if not bcrypt.checkpw(password.encode("utf-8"), up.password):
                return None
            up.last_login = timezone.now()
            up.save()
        except UserProfile.DoesNotExist:
            return None

        # If yes, extract the django user, or create a new one
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # Create a new user. There's no need to set a password
            # because only the password from settings.py is checked.
            user = User(username=username)
            user.save()
        return user

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user
