from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from rest_framework.decorators import api_view,permission_classes

from base.api_response import success_response, error_response
from cms.models import Cms
from company.models import Configuration


class CompanyDetailView(generics.GenericAPIView):
    permission_classes = [AllowAny]
        
    def get(self, request):
        
        objs =  Configuration.objects.filter(is_deleted=False)

        data_info = dict()
        for obj in objs:
            data_info[obj.code] = obj.value
        response_data = success_response(data_info)
        return Response(response_data, status=response_data["code"])


class CompanyConfigurationView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        
        objs =  Configuration.objects.filter(is_deleted=False)

        data_info = dict()
        for obj in objs:
            data_info[obj.code] = obj.value
        response_data = success_response(data_info)
        return Response(response_data, status=response_data["code"])
