from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'faq'

router = DefaultRouter(trailing_slash=False)

router.register('faq', views.FaqAPISet, base_name="faq")

urlpatterns = [
   
    
]+router.urls