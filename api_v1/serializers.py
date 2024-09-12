from rest_framework import serializers

from .models import HandBook, HandBookElement


class HandBookSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='title')
    code = serializers.CharField(source='uniq_code')

    class Meta:
        model = HandBook
        fields = ['id', 'code', 'name']


class HandBookElementSerializer(serializers.ModelSerializer):
    code = serializers.CharField(source='uniq_code')

    class Meta:
        model = HandBookElement
        fields = ['code', 'value']


class CheckElementSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)
    value = serializers.CharField(required=True)
    version = serializers.CharField(required=False)
