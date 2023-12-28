from BonsaiAdvice.models import get_periods, periodid_to_name
from rest_framework import serializers as r_serializers
from rest_framework_mongoengine import serializers

from .models import TechniqueMapper, TreeInfo


class LazyReferenceFieldSerializer(r_serializers.BaseSerializer):
    def to_representation(self, instance):
        return {'classname': instance.document_type.__name__, 'id': str(instance.id)}


class PeriodSerializer(r_serializers.ChoiceField):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return [periodid_to_name(_) for _ in ret]


class TechniqueMapperSerializer(serializers.EmbeddedDocumentSerializer):
    technique = LazyReferenceFieldSerializer()
    objective = LazyReferenceFieldSerializer()
    stage = LazyReferenceFieldSerializer(many=True)
    period = PeriodSerializer(
        choices=[f"{_[0][0]}_{_[0][1]}" for _ in get_periods()])

    def get_period(self, obj):
        return

    class Meta:
        model = TechniqueMapper
        fields = ['oid', 'comment', 'technique',
                  'objective', 'stage', 'period']


class TreeInfoSerializer(serializers.DocumentSerializer):
    techniques = TechniqueMapperSerializer(TechniqueMapper, many=True)

    class Meta:
        model = TreeInfo
        fields = ['name', 'display_name', 'latin_name', 'description', 'placement', 'watering',
                  'fertilizing', 'pruning_wiring', 'repotting', 'propagation', 'pests', 'published', 'techniques']
