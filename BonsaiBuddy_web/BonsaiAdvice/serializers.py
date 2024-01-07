from rest_framework_mongoengine import serializers
from BonsaiBuddy.serializers import ObjectIdFieldSerializer

from .models import BonsaiObjective, BonsaiTechnique


class BonsaiTechniqueSerializer(serializers.DocumentSerializer):
    id = ObjectIdFieldSerializer()

    class Meta:
        model = BonsaiTechnique
        fields = '__all__'
