from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . import models


class SiteImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, validators=[UniqueValidator(queryset=models.SiteImage.objects.filter(is_deleted=False), message="Title already exists",)], error_messages={'required': 'Please enter title'})
    image_type = serializers.CharField(required=True, error_messages={'required': 'Please enter Image Type'})
    image_key = serializers.CharField(required=True, validators=[UniqueValidator(queryset=models.SiteImage.objects.filter(is_deleted=False), message="Key name already exists",)], error_messages={'required': 'Please enter Image Key'})
    image_link = serializers.CharField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)
    
    is_active = serializers.BooleanField(read_only=True)
    image_url = serializers.SerializerMethodField()


    class Meta:
        model = models.SiteImage
        fields = ('id', 'title', 'image', 'image_type', 'image_key', 'image_link',
                    'description', 'is_active', 'image_url', )


    def get_image_url(self, obj):
        return obj.get_image_url()
