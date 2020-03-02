from django.urls import path, include

from . import views

urlpatterns = [
    path('company_details', views.CompanyDetailView.as_view(), name="company_details"),
    path('company_config', views.CompanyConfigurationView.as_view(), name="company_config"),
]