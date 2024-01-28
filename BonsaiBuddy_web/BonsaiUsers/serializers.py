from BonsaiBuddy.serializers import ObjectIdFieldSerializer
from .models import TreeCollection, User, UserProfile
from rest_framework import serializers as rest_serializers
from rest_framework_mongoengine import serializers


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
