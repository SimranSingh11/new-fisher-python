from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from role_permission.permissions import CheckRolePermission

from base.models import BaseAPISet
from . import models
from . import serializers

class FaqAPISet(BaseAPISet):

    permission_classes = [IsAuthenticated, CheckRolePermission]
    model = models.Faq
    serializer_class = serializers.FaqSerializer
    search_fields = ['title']
    dropdown_fields = ['id', 'title']
