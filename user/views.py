from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from base.models import BaseAPISet

from user import serializers
from user import models
from user import constants

from role_permission.permissions import CheckRolePermission


class SalesmanAPISet(BaseAPISet):

    permission_classes = [IsAuthenticated, CheckRolePermission]
    queryset = models.User.objects.filter(is_deleted=False, user_type=constants.SALSEMAN)
    serializer_class = serializers.SalesmanSerializer
    search_fields = ['first_name', 'last_name']
    dropdown_fields = ['id', 'first_name', 'last_name']

    def perform_create(self, serializer, request):
        from user.helpers import generate_salesman_id, send_registration_mail
        instance = serializer.save()
        instance.created_by = request.user.id
        instance.updated_by = request.user.id
        instance.user_type = constants.SALSEMAN
        instance.salesman_id = generate_salesman_id()
        instance.save()

        send_registration_mail(instance)

        return instance


class CustomerAPISet(BaseAPISet):

    permission_classes = [IsAuthenticated, CheckRolePermission]
    queryset = models.User.objects.filter(is_deleted=False, user_type=constants.CUSTOMER)
    serializer_class = serializers.SalesmanSerializer
    search_fields = ['first_name', 'last_name']
    dropdown_fields = ['id', 'first_name', 'last_name']

    def perform_create(self, serializer, request):
        instance = serializer.save()
        instance.created_by = request.user.id
        instance.updated_by = request.user.id
        instance.user_type = constants.CUSTOMER
        instance.save()
        return instance
