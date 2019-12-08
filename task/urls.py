from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'task'

router = DefaultRouter(trailing_slash=False)

router.register('task', views.TaskAPISet, base_name="task")


urlpatterns = [
   
    
]+router.urls