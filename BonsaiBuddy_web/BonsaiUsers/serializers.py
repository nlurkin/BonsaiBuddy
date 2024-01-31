import bcrypt
from BonsaiBuddy.serializers import ObjectIdFieldSerializer
from .models import TreeCollection, User, UserProfile
from rest_framework import serializers as rest_serializers
from rest_framework_mongoengine import serializers
from django.contrib.auth import password_validation


class UserSerializer(rest_serializers.ModelSerializer):
    permissions = rest_serializers.SerializerMethodField()
    groups = rest_serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'permissions', 'groups',
                  'last_login', 'first_name', 'last_name', 'is_active', 'is_superuser']

    def get_permissions(self, obj):
        return [_ for _ in obj.get_all_permissions()]

    def get_groups(self, obj):
        return [_.name for _ in obj.groups.all()]


class TreeCollectionSerializer(serializers.EmbeddedDocumentSerializer):
    oid = ObjectIdFieldSerializer()

    class Meta:
        model = TreeCollection
        fields = ['oid', 'treeReference', 'objective']


class ProfileSerializer(serializers.DocumentSerializer):
    my_trees = TreeCollectionSerializer(TreeCollection, many=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class ChangePasswordSerializer(serializers.DocumentSerializer):
    password = rest_serializers.CharField(write_only=True, required=True, validators=[
        password_validation.validate_password])
    password2 = rest_serializers.CharField(write_only=True, required=True)
    old_password = rest_serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserProfile
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise rest_serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        up = UserProfile.get_user(user.username)
        if not bcrypt.checkpw(old_password.encode("utf-8"), up.password):
            raise rest_serializers.ValidationError(
                {"description": "The old password is incorrect"})
        return old_password

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
