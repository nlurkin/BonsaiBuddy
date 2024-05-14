from rest_framework_mongoengine import serializers
from rest_framework import serializers as rest_serializers
from BonsaiBuddy.serializers import ObjectIdFieldSerializer, PeriodSerializer
from TreeInfo.models import TechniqueMapper
from TreeInfo.serializers import TechniqueMapperSerializer

from .models import BonsaiObjective, BonsaiStage, BonsaiTechnique, period_enum


class BonsaiTechniqueSerializer(serializers.DocumentSerializer):
    id = ObjectIdFieldSerializer()
    description = rest_serializers.CharField(allow_blank=True)

    class Meta:
        model = BonsaiTechnique
        fields = '__all__'


class BonsaiObjectiveSerializer(serializers.DocumentSerializer):
    id = ObjectIdFieldSerializer()
    description = rest_serializers.CharField(allow_blank=True)

    class Meta:
        model = BonsaiObjective
        fields = '__all__'


class BonsaiStageSerializer(serializers.DocumentSerializer):
    id = ObjectIdFieldSerializer()
    description = rest_serializers.CharField(allow_blank=True)
    global_period = PeriodSerializer(
        choices=period_enum)

    class Meta:
        model = BonsaiStage
        fields = '__all__'


class AssociationSearchSerializer(rest_serializers.Serializer):
    tree = rest_serializers.CharField(required=True)
    objective = rest_serializers.CharField()
    stage = rest_serializers.ListField(
        child=rest_serializers.CharField(), required=False)
    period = rest_serializers.CharField(required=False)


class AssociationSearchResultSerializer(rest_serializers.Serializer):
    techniques = TechniqueMapperSerializer(TechniqueMapper, many=True)
