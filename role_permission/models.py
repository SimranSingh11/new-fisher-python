from django.db import models
from base.models import BaseModel
from user.models import User
# Create your models here.


class AppModule(BaseModel):
    name = models.CharField(unique=True, max_length=15, db_column='name')
   
    class Meta:
        verbose_name_plural = 'AppModules'
        verbose_name = 'AppModule'
        db_table = 'app_module'
        

class AppModel(BaseModel):
    name = models.CharField(max_length=15, db_column='name')
    module = models.ForeignKey(AppModule, related_name='app_model_module', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'AppModels'
        verbose_name = 'AppModel'
        db_table = 'app_model'
        unique_together = ['name', 'module']


class Permission(BaseModel):
    name = models.CharField(max_length=15, db_column='name')
    code = models.CharField(max_length=15, db_column='code')
    order_no = models.IntegerField(default=0, db_column='order_no')
    model = models.ForeignKey(AppModel, related_name='permission_model', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Permissions'
        verbose_name = 'Permission'
        db_table = 'permission_master'
        

class Role(BaseModel):
    name = models.CharField(max_length=15, db_column='name')

    class Meta:
        verbose_name_plural = 'Roles'
        verbose_name = 'Role'
        db_table = 'role_master'


class RolePermission(BaseModel):
    role = models.ForeignKey(Role, related_name='role_permission_role', on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, related_name='role_permission_permission', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'RolePermissions'
        verbose_name = 'RolePermission'
        db_table = 'role_permission'


class UserPermission(BaseModel):
    user = models.ForeignKey(User, related_name='user_permission_user', on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, related_name='user_permission_permission', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'UserPermissions'
        verbose_name = 'UserPermission'
        db_table = 'user_permission'

