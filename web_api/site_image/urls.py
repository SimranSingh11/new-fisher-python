from django.urls import path, include

from . import views

urlpatterns = [

    path('banner_image_list', views.BannerImagesListView.as_view(), name="banner_image_list"),

]