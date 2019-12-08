"""app_fisher URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Fisher App API')


urlpatterns = [
    # path('', schema_view),

    # path('admin/', admin.site.urls),
    path('', include_docs_urls(title='Backend API List')),
    path('api/', include('auth.urls')),  # auth module urls
    path('api/', include('user.urls')),  # user module urls
    path('api/', include('product.urls')),  # product module urls
    path('api/', include('task.urls')),  # task module urls

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

