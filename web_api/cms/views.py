from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from rest_framework.decorators import api_view,permission_classes

from base.api_response import success_response, error_response
from cms.models import Cms
from faq.models import Faq


class CmsPageView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, key):

        cms_obj =  Cms.objects.filter(key=key, is_deleted=False).first()

        if cms_obj:
            data_info = dict()
            data_info['title'] = cms_obj.title
            data_info['key'] = cms_obj.key
            data_info['content'] = cms_obj.content
            response_data = success_response(data=data_info)
        else:
            response_data = error_response()

        return Response(response_data, status=response_data["code"])



class FaqListView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        
        faq_objs =  Faq.objects.filter(is_deleted=False, is_active=True)

        faq_list = list()

        for obj in faq_objs:
            data_info = dict()
            data_info['title'] = obj.title
            data_info['question'] = obj.question
            data_info['answer'] = obj.answer
            faq_list.append(data_info)
        
        response_data = success_response(data=faq_list)

        return Response(response_data, status=response_data["code"])

