from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model

auth_model = get_user_model()


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    new_password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
  
    def validate(self, data):
        if not data.get('new_password'):
            raise serializers.ValidationError({'new_password': "Please enter a password and confirm it"})

        if data.get('new_password') != data.get('confirm_password'):
            raise serializers.ValidationError({'confirm_password': " Passwords don't match"})
            
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    dial_code = serializers.CharField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = auth_model
        fields = ('first_name', 'last_name', 'dial_code', 'phone_number', 'email', 'image')
