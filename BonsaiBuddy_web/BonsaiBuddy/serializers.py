from bson import ObjectId
from bson.errors import InvalidId
from django.utils.encoding import smart_str
from rest_framework import serializers, fields

from BonsaiAdvice.models import periodid_to_name


class StringListSerializer(serializers.Serializer):
    def to_representation(self, value):
        return value


class ObjectIdFieldSerializer(fields.Field):
    def to_internal_value(self, data):
        if data == 'null_bson_id':
            return None
        try:
            return ObjectId(str(data))
        except InvalidId:
            raise serializers.ValidationError(
                '`{}` is not a valid ObjectID'.format(data))

    def to_representation(self, value):
        if not ObjectId.is_valid(value):
            raise InvalidId
        return smart_str(value)


class PeriodSerializer(serializers.MultipleChoiceField):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret
