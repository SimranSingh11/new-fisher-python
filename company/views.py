from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

from django.db import models
from django.db.models import Q

from base.api_response import success_response, error_response, get_serializer_errors, response_text
from base.utils import get_serach_term, p_print

from . import serializers
from . import models


class ConfigurationView(generics.GenericAPIView):
    model  = models.Configuration
    serializer_class = serializers.ConfigurationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        config_objs =  self.model.objects.all() 
        config_data = list()
        
        for obj in config_objs:
            data_info = dict()
            data_info['name'] = obj.name.replace("_"," ")
            data_info['code'] = obj.code
            data_info['value'] = obj.value
            config_data.append(data_info) 
        
        response_data = success_response(data=config_data)

        return Response(response_data, status=response_data["code"])


    def post(self, request):
        """
        Update Configurations
        """

        request_data  = request.data

        serializer_class = self.get_serializer_class()

        for config_data in request_data:

            code = config_data.get('code')
            c_obj = self.model.objects.filter(code=code).first()
            
            if c_obj:
                serializer = serializer_class(c_obj, data=config_data)
            else:
                serializer = serializer_class(data=config_data)

            if serializer.is_valid():
                serializer.save()
                
        response_data = success_response()

        return Response(response_data, status=response_data["code"])


    