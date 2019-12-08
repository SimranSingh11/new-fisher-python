from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'product'

router = DefaultRouter(trailing_slash=False)

router.register('size', views.SizeAPISet, base_name="size")
router.register('category', views.CategoryAPISet, base_name="category")
router.register('sub-category', views.SubCategoryAPISet, base_name="sub-category")
router.register('importing', views.ImportingAPISet, base_name="importing")
router.register('type', views.TypeAPISet, base_name="type")
router.register('product', views.ProductAPISet, base_name="product")

urlpatterns = [
   
    
]+router.urls