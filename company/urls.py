from django.urls import include, path
from . import views

app_name = 'company'

urlpatterns = [
   path('configuration', views.ConfigurationView.as_view())
]