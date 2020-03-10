from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from base.utils import get_serach_term, p_print


from base.api_response import success_response, error_response
from site_image import models


class BannerImagesListView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        for Retrieve Banner data
        """
        objs =  models.SiteImage.objects.filter(is_deleted=False, is_active=True, image_type='banner')

        data_list = list()
       
        for obj in objs:
            data_info = dict()
            data_info['id'] = obj.pk
            data_info['title'] = obj.title
            data_info['image'] = obj.get_image_url()
            data_list.append(data_info)  
       
        response_data = success_response(data=data_list)

        return Response(response_data, status=response_data["code"])