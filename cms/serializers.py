from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . import models


class CmsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, validators=[UniqueValidator(queryset=models.Cms.objects.filter(is_deleted=False), message="Cms already exists",)], error_messages={'required': 'Please enter title'})
    # key = serializers.CharField(required=True)
    content = serializers.CharField(required=True)
    is_active = serializers.BooleanField(read_only=True)
   
    class Meta:
        model = models.Cms
        fields = ('id', 'title', 'key', 'content','is_active')