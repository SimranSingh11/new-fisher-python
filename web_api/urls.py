from django.urls import path, include

urlpatterns = [
    path('', include('web_api.company.urls')),
    path('', include('web_api.cms.urls')),
    path('', include('web_api.product.urls')),  
    path('', include('web_api.site_image.urls')),  

]