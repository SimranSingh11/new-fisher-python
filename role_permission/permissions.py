from rest_framework import permissions
from base.utils import p_print
from . import models


class  CheckRolePermission(permissions.BasePermission):
    """
    Check Role wise Permission
    """

    def has_permission(self, request, view):
         
        if request.user.is_superuser:
            return True
        
        if not request.user.is_authenticated:
            return False

        kwargs = view.kwargs
        role_id = request.user.role_id            
        
        action = None
        app_lable = None
        model_name = None

        if hasattr(view, 'model') and view.model != None:
            app_lable = view.model._meta.app_label.lower()
            model_name = view.model.__name__.lower()

        if hasattr(view, 'queryset') and view.queryset != None:
            app_lable = view.queryset.model._meta.app_label.lower()
            model_name = view.queryset.model.__name__.lower()

        if hasattr(view, 'action'):
            view_action = view.action

            if view_action == 'list':
                action = 'list'
            elif view_action == 'retrieve':
                action = 'view'
            elif view_action == 'create':
                action = 'view'
            elif view_action == 'update':
                action = 'edit'
            elif view_action == 'partial_update':
                action = 'change_status'
            elif view_action == 'destroy':
                action = 'delete'
            else:
                action = view_action
        
        else:
            if not kwargs.get('pk'):                
                if request.method == 'GET':
                    action = 'list'
                elif request.method == 'POST':
                    action = 'add'
            else:
                if request.method == 'GET':
                    action = 'view'
                elif request.method == 'POST':
                    action = 'edit'
                elif request.method == 'PUT':
                    action = 'edit'
                elif request.method == 'PATCH':
                    action = 'change_status'
                elif request.method == 'DELETE':
                    action = 'delete'    

        is_allowed = models.RolePermission.objects.filter(role_id=role_id, permission__code=action, permission__model__name=model_name).exists()
 
        print("\n========= has_permission ===============\n")
        print('==> role_id: ', role_id)
        print("==> kwargs: ", kwargs)
        print("==> app_lable: ", app_lable)
        print("==> model_name: ", model_name)
        print("==> action: ", action)
        print('==> is_allowed: ', is_allowed)
        print("\n=======================================\n")

        return is_allowed