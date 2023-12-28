from rest_framework_mongoengine import serializers

from .models import TreeInfo


class TreeInfoSerializer(serializers.DocumentSerializer):
    class Meta:
        model = TreeInfo
        fields = ['name', 'display_name', 'latin_name', 'description', 'placement', 'watering',
                  'fertilizing', 'pruning_wiring', 'repotting', 'propagation', 'pests', 'published']
