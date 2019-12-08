from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


app_name = 'users'

router = DefaultRouter(trailing_slash=False)

router.register('salesman', views.SalesmanAPISet, base_name="salesman")
router.register('customer', views.CustomerAPISet, base_name="customer")

urlpatterns = [

]+router.urls