from rest_framework_mongoengine import serializers
from BonsaiBuddy.serializers import ObjectIdFieldSerializer, PeriodSerializer

from .models import BonsaiObjective, BonsaiStage, BonsaiTechnique, period_enum


class BonsaiTechniqueSerializer(serializers.DocumentSerializer):
    id = ObjectIdFieldSerializer()

    class Meta:
        model = BonsaiTechnique
        fields = '__all__'


class BonsaiObjectiveSerializer(serializers.DocumentSerializer):
    id = ObjectIdFieldSerializer()

    class Meta:
        model = BonsaiObjective
        fields = '__all__'


class BonsaiStageSerializer(serializers.DocumentSerializer):
    id = ObjectIdFieldSerializer()
    global_period = PeriodSerializer(
        choices=period_enum)

    class Meta:
        model = BonsaiStage
        fields = '__all__'
