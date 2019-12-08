from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'auth'

router = DefaultRouter(trailing_slash=False)
router.register('auth', views.UserAuthAPISet, base_name="auth")

urlpatterns = [
    path('profile', views.UserProfileView.as_view(), name="user_profile"),

]+router.urls