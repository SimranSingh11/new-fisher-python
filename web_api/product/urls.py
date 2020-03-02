from django.urls import path, include

from . import views

urlpatterns = [
    path('product_list', views.ProductListView.as_view(), name="product_list"),
    path('product_detail/<str:pk>', views.ProductDetailView.as_view(), name="product_detail"),

    path('size_list', views.SizeListView.as_view(), name="size_list"),

    path('category_list', views.CategoryListView.as_view(), name="category_list"),
    path('subcategory_list', views.SubCategoryListView.as_view(), name="subcategory_list"),
    path('importing_list', views.ImportingListView.as_view(), name="importing_list"),
    path('type_list', views.TypeListView.as_view(), name="type_list"),

]