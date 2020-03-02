from django.urls import path, include

from . import views

urlpatterns = [
    path('cms_page/<str:key>', views.CmsPageView.as_view(), name="cms_page"),
    path('faq_list', views.FaqListView.as_view(), name="faq_list"),

]