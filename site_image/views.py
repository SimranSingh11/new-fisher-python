from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from base.api_response import success_response, error_response, api_message, response_text, get_serializer_errors
from base.models import BaseAPISet

from role_permission.permissions import CheckRolePermission

from . import models
from . import serializers


class SiteImageAPISet(BaseAPISet):

    permission_classes = [IsAuthenticated, CheckRolePermission]
    model = models.SiteImage
    serializer_class = serializers.SiteImageSerializer
    search_fields = ['title']
    dropdown_fields = ['id', 'title']
