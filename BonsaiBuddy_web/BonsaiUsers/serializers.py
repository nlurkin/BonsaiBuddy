from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'permissions',
                  'last_login', 'first_name', 'last_name', 'is_active']

    def get_permissions(self, obj):
        return [_ for _ in obj.get_all_permissions()]
