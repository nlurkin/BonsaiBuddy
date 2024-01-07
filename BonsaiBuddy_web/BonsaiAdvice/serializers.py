from rest_framework import serializers as r_serializers
from rest_framework_mongoengine import serializers

from .models import BonsaiTechnique


class BonsaiTechniqueSerializer(serializers.DocumentSerializer):

    class Meta:
        model = BonsaiTechnique
        fields = '__all__'
