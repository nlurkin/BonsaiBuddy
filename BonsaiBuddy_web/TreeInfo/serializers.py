from BonsaiAdvice.models import period_enum
from rest_framework import serializers as rest_serializers
from rest_framework_mongoengine import serializers

from BonsaiBuddy.serializers import ObjectIdFieldSerializer, PeriodSerializer

from .models import TechniqueMapper, TreeInfo


class LazyReferenceFieldSerializer(rest_serializers.Serializer):
    classname = rest_serializers.CharField()
    id = rest_serializers.CharField()

    def to_representation(self, instance):
        return {'classname': instance.document_type.__name__, 'id': str(instance.id)}


class TechniqueMapperSerializer(serializers.EmbeddedDocumentSerializer):
    oid = ObjectIdFieldSerializer()
    technique = LazyReferenceFieldSerializer()
    objective = LazyReferenceFieldSerializer()
    stage = LazyReferenceFieldSerializer(many=True)
    period = PeriodSerializer(
        choices=period_enum,)

    class Meta:
        model = TechniqueMapper
        fields = ['oid', 'comment', 'technique',
                  'objective', 'stage', 'period']


class TreeInfoSerializer(serializers.DocumentSerializer):
    id = ObjectIdFieldSerializer()
    techniques = TechniqueMapperSerializer(TechniqueMapper, many=True)
    description = rest_serializers.CharField(allow_blank=True)
    placement = rest_serializers.CharField(allow_blank=True)
    watering = rest_serializers.CharField(allow_blank=True)
    fertilizing = rest_serializers.CharField(allow_blank=True)
    pruning_wiring = rest_serializers.CharField(allow_blank=True)
    repotting = rest_serializers.CharField(allow_blank=True)
    propagation = rest_serializers.CharField(allow_blank=True)
    pests = rest_serializers.CharField(allow_blank=True)

    class Meta:
        model = TreeInfo
        fields = ['id', 'name', 'display_name', 'latin_name', 'description', 'placement', 'watering',
                  'fertilizing', 'pruning_wiring', 'repotting', 'propagation', 'pests', 'published', 'techniques']

    def create_update_techniques(self, instance, techniques_data):
        if techniques_data is not None:
            for technique in techniques_data:
                tree = instance.techniques.filter(oid=technique['oid']).first()
                if tree:
                    # Update existing tree
                    TechniqueMapperSerializer().update(tree, technique)
                else:
                    # Create new tree and add it to instance.my_trees
                    new_tree = TechniqueMapperSerializer().create(technique)
                    instance.my_trees.append(new_tree)

    def update(self, instance, validated_data):
        techniques_data = validated_data.pop('techniques')

        self.create_update_techniques(instance, techniques_data)

        return super().update(instance, validated_data)

    def create(self, validated_data):
        techniques_data = validated_data.pop('techniques')

        instance = super().create(validated_data)
        self.create_update_techniques(instance, techniques_data)

        return instance
