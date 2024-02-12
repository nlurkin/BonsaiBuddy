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
    comment = rest_serializers.CharField(allow_blank=True)

    class Meta:
        model = TechniqueMapper
        fields = ['oid', 'comment', 'technique',
                  'objective', 'stage', 'period']

    def create(self, validated_data):
        instance = TechniqueMapper(
            technique=validated_data['technique']['id'], objective=validated_data['objective']['id'],
            stage=[stage['id'] for stage in validated_data['stage']], period=validated_data['period'],
            comment=validated_data["comment"])

        return instance


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
                technique_mapper = instance.techniques.filter(
                    oid=technique['oid']).first()

                if technique_mapper:
                    # Update existing tree
                    TechniqueMapperSerializer().update(technique_mapper, technique)
                else:
                    # Create new tree and add it to instance.my_trees
                    new_tree = TechniqueMapperSerializer().create(technique)
                    instance.techniques.append(new_tree)

    def update(self, instance, validated_data):
        if 'techniques' in validated_data:
            techniques_data = validated_data.pop('techniques')

            self.create_update_techniques(instance, techniques_data)

        return super().update(instance, validated_data)

    def create(self, validated_data):
        techniques_data = validated_data.pop('techniques')

        instance = super().create(validated_data)
        self.create_update_techniques(instance, techniques_data)

        return instance
