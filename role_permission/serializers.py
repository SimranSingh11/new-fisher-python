from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from . import models


class AppModuleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = models.AppModule
        fields = ['id','name', ]


class AppModelSerializer(serializers.ModelSerializer):    
    name = serializers.CharField(required=True)
    module_id = serializers.IntegerField(required=True)

    class Meta:
        model = models.AppModel
        fields = ['id','name','module_id' ]


class PermissionSerializer(serializers.ModelSerializer):    

    name = serializers.CharField(required=True)
    code = serializers.CharField(required=True)
    model_id = serializers.IntegerField(required=True)

    class Meta:
        model = models.Permission
        fields = ['id','name','code', 'model_id']
        validators = [
            UniqueTogetherValidator(
                queryset=models.Permission.objects.filter(is_deleted=False).all(),
                fields=['code', 'model_id'],
                message="Already exists"
            )
        ]


class RoleSerializer(serializers.ModelSerializer):    
    class Meta:
        model = models.Role
        fields = ['id','name']



class RolePermissionSerializer(serializers.ModelSerializer):    
    class Meta:
        model = models.RolePermission
        fields = ['role_id','permission_id']

        validators = [
            UniqueTogetherValidator(
                queryset=models.RolePermission.objects.filter(is_deleted=False).all(),
                fields=['role_id', 'permission_id'],
                message="Already exists"
            )
        ]


class UserPermissionSerializer(serializers.ModelSerializer):    
    class Meta:
        model = models.UserPermission
        fields = '__all__'


class UpdateRolePermissionSerializer(serializers.Serializer):
    permission_ids = serializers.ListField(required=True)