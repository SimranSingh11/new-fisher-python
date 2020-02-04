from rest_framework.permissions import AllowAny, IsAuthenticated

from role_permission.permissions import CheckRolePermission

from base.models import BaseAPISet

from . import models
from . import serializers



class OrderAPISet(BaseAPISet):

    permission_classes = [IsAuthenticated, CheckRolePermission]
    model = models.Order
    serializer_class = serializers.OrderSerializer
    # search_fields = ['id' ,'task', 'assignee__first_name', 'assignee__last_name']
