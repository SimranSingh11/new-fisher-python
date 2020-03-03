from django.urls import path
from role_permission import views
from rest_framework.routers import DefaultRouter

app_name = 'role_permission'

router = DefaultRouter(trailing_slash=False)
router.register('app_module', views.AppModuleAPISet, base_name="app_module")
router.register('app_model', views.AppModelAPISet, base_name="app_model")
router.register('permission', views.PermissionAPISet, base_name="permission")
router.register('role', views.RoleAPISet, base_name="role")

urlpatterns = [
       path('role_permission/<int:role_id>', views.RolePermissionList.as_view()),
       path('update_permission_data/', views.UpdatePermissionsData.as_view()),


]+router.urls