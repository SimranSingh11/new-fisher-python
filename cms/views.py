from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from role_permission.permissions import CheckRolePermission
from rest_framework import generics

from base.api_response import success_response, error_response
from base.models import BaseAPISet

from . import models
from . import serializers

class CmsAPISet(BaseAPISet):

    permission_classes = [IsAuthenticated, CheckRolePermission]
    model = models.Cms
    serializer_class = serializers.CmsSerializer
    search_fields = ['title']
    dropdown_fields = ['id', 'title']


class GetCmsPage(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, key):
        cms_obj = models.Cms.objects.filter(is_deleted=False, is_active=True, key=key).first()

        if cms_obj:
            data_info = dict()
            data_info['key'] = cms_obj.key
            data_info['title'] = cms_obj.title
            data_info['content'] = cms_obj.content
            response_data = success_response(data_info)
        else:
            response_data = error_response()

        return Response(response_data, status=response_data["code"])
