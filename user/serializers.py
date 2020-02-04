from rest_framework import serializers
from user.models import User
from base.utils import p_print, save_file


class SalesmanSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    dial_code = serializers.CharField(required=False, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_null=True)
    email = serializers.EmailField(required=True)
    date_of_birth = serializers.DateTimeField(required=False, allow_null=True)
    image = serializers.ImageField(required=False, allow_null=True)
    full_name = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    contact_number = serializers.SerializerMethodField()
    birth_date = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(read_only=True)
    role_id = serializers.IntegerField(required=False)
    salesman_id = serializers.CharField(read_only=True)


    class Meta:
        model = User
        
        fields = ('id', 'first_name', 'last_name', 'dial_code', 'phone_number', 'email','image_url',
                  'image', 'date_of_birth', 'address', 'full_name', 'is_active', 'is_verified',
                  'contact_number', 'date_joined', 'birth_date', 'role_id', 'salesman_id')
        
        read_only_fields = ('is_active', 'is_verified')

    def to_internal_value(self, attr_data):

        from my_helpers.datetime_helper import timestamp_to_datetime
        data = attr_data.copy()
        date_of_birth = data.get('date_of_birth', None)
        if date_of_birth:
            data['date_of_birth'] = timestamp_to_datetime(int(date_of_birth))

        return super().to_internal_value(data)

    def get_full_name(self, obj):
        return "{} {}".format(obj.first_name, obj.last_name).strip()


    def get_image_url(self, obj):
        return obj.get_image_path()


    def get_contact_number(self, obj):
        return obj.get_contact_number()

    def get_birth_date(self, obj):
        from my_helpers.datetime_helper import datetime_to_timestamp
        return datetime_to_timestamp(obj.date_of_birth)
