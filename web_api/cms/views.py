from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from rest_framework.decorators import api_view,permission_classes

from base.api_response import success_response, error_response
from cms.models import Cms
from faq.models import Faq


# =================================================================================== #
# CmsPageView
# methods:
# (1) get : to get cms page data
# =================================================================================== #

class CmsPageView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, key):
        """
        for Retrieve cmsn data
        """

        cms_obj =  Cms.objects.filter(key=key, is_deleted=False).first()

        if cms_obj:
            data_info = dict()
            response_data = success_response(data=data_info)
        else:
            response_data = error_response()

        return Response(response_data, status=response_data["code"])



class FaqListView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        for Retrieve product data
        """
        obj =  Faq.objects.filter(is_deleted=False).first()

        if obj:
            data_info = dict()
            response_data = success_response(data=data_info)
        else:
            response_data = error_response()

        return Response(response_data, status=response_data["code"])

