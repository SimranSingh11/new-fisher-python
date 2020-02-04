from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'order'

router = DefaultRouter(trailing_slash=False)

router.register('order', views.OrderAPISet, base_name="order")


urlpatterns = [
   
    
]+router.urls