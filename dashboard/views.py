from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

from django.db import models
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import Http404
from django.conf import settings

from base.api_response import success_response, error_response, get_serializer_errors, response_text
from base.utils import get_serach_term, p_print


class DashboardData(generics.ListAPIView):


    def get(self, request):
        """
        Retrieve dashboard data
        """

        from . import helpers

        data = dict()
        data['task'] = helpers.get_dashboard_task_data() 
        data['order'] = helpers.get_dashboard_order_data()
        data['customor'] = helpers.get_dashboard_customor_data()
        data['salesman'] = helpers.get_dashboard_salesman_data()
        data['revenue'] = helpers.get_dashboard_revenue_data()

        response_data = success_response(data=data)

        return Response(response_data, status=response_data["code"])

