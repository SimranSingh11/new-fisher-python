from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . import models


class FaqSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # title = serializers.CharField(required=True, validators=[UniqueValidator(queryset=models.Faq.objects.filter(is_deleted=False), message="FAQ already exists",)], error_messages={'required': 'Please enter title'})
    question = serializers.CharField(required=True)
    answer = serializers.CharField(required=True)
    is_active = serializers.BooleanField(read_only=True)
   
    class Meta:
        model = models.Faq
        fields = ('id', 'title', 'question', 'answer','is_active')