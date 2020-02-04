from rest_framework import serializers
from . import models


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    customer_id = serializers.IntegerField(required=False, allow_null=True)
    address = serializers.CharField(required=True)
    latitude = serializers.CharField(required=False, allow_null=True)
    longitude = serializers.CharField(required=False, allow_null=True)    
    amount = serializers.CharField(required=True)
    tax = serializers.CharField(required=True)
    net_amount = serializers.CharField(required=True)
    status = serializers.CharField(required=True)

    class Meta:
        model = models.Order
        fields = '__all__'
