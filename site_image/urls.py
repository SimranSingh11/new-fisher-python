from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'site_image'

router = DefaultRouter(trailing_slash=False)

router.register('site_image', views.SiteImageAPISet, base_name="site_image")

urlpatterns = [
   
    
]+router.urls