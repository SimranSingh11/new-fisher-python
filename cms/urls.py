from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'cms'

router = DefaultRouter(trailing_slash=False)

router.register('cms', views.CmsAPISet, base_name="cms")

urlpatterns = [
    path('get_cms_page/<str:key>', views.GetCmsPage.as_view(), name="get_cms_page"),
    
]+router.urls