from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, DjangoModelPermissions
from rest_framework import generics
from role_permission.permissions import CheckRolePermission

from base.models import BaseAPISet
from . import models
from . import serializers
from . import helpers
from role_permission.permissions import CheckRolePermission


class AppModuleAPISet(BaseAPISet):
    
    permission_classes = [IsAuthenticated, CheckRolePermission]
    model = models.AppModule
    serializer_class = serializers.AppModuleSerializer
    check_company = False
    apply_pagination = False



class AppModelAPISet(BaseAPISet):

    permission_classes = [IsAuthenticated, CheckRolePermission]
    model = models.AppModel
    serializer_class = serializers.AppModelSerializer
    check_company = False
    apply_pagination = False


    def get_object_list(self, objects):
        """
        return list of objectd data dict
        @:param: list of objects
        ''
        """

        from .models import AppModule

        module_ids = list(set([e.module_id for e in objects]))

        module_objs = AppModule.objects.filter(pk__in=module_ids)
        module_name_dict = {e.pk:e.name for e in module_objs}

        response_dict = dict()

        for obj in objects:
            module_name = module_name_dict.get(obj.module_id)
            if not response_dict.get(module_name):
                response_dict[module_name] = list()
            
            data = dict()
            data['id'] = obj.pk
            data['name'] = obj.name
            data['module_id'] = obj.module_id
            response_dict[module_name].append(data)

        return response_dict


class PermissionAPISet(BaseAPISet):
    
    permission_classes = [IsAuthenticated, CheckRolePermission]
    model = models.Permission
    serializer_class = serializers.PermissionSerializer
    check_company = False
    apply_pagination = False
    sort_by = ['pk']
    


    def get_object_list(self, objects):
        """
        return list of objectd data dict
        @:param: list of objects
        ''
        """

        from .models import AppModel

        model_ids = list(set([e.model_id for e in objects]))

        model_objs = AppModel.objects.filter(pk__in=model_ids)
        model_name_dict = {e.pk:e.name for e in model_objs}

        response_dict = dict()

        for obj in objects:
            model_name = model_name_dict.get(obj.model_id)
            if not response_dict.get(model_name):
                response_dict[model_name] = list()
            
            data = dict()
            data['id'] = obj.pk
            data['name'] = obj.name
            data['code'] = obj.code
            data['model_id'] = obj.model_id
            response_dict[model_name].append(data)

        result_list = list()
        for key,value in response_dict.items():
            res_obj = dict()
            res_obj['key'] = key
            res_obj['value'] = value
            result_list.append(res_obj)
        
        return result_list



class RoleAPISet(BaseAPISet):
    
    permission_classes = [IsAuthenticated, CheckRolePermission]
    model = models.Role
    serializer_class = serializers.RoleSerializer
    check_company = False
    # apply_pagination = False
    search_fields = ['name']
    dropdown_fields = ['id', 'name']

    def get_object_data(self, instance):
        """
        return object data dict
        @:param: object
        """
        pass

        data_info = dict()
        if instance:
            data_info['id'] = instance.pk
            data_info['name'] = instance.name
            data_info['permission'] =  helpers.get_role_wise_permissions_detail(instance.pk)
        
        return data_info
            

# =================================================================================== #
# UserProfileView
# methods:
# (1) get : to get profile
# (2) post : to update profile
# =================================================================================== #

from rest_framework.response import Response
from base.api_response import success_response, error_response, get_serializer_errors, response_text, api_message

class RolePermissionList(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, CheckRolePermission]
    serializer_class = serializers.UpdateRolePermissionSerializer

    def get(self, request, role_id):
        """
        for Retrieve profile data
        """

        selected_permission_list = list(models.RolePermission.objects.filter(role_id=role_id, is_deleted=False).values_list('permission_id'))
        selected_permission_list = [e[0] for e in selected_permission_list]

        from .models import AppModel

        perm_objects = models.Permission.objects.filter(is_deleted=False).order_by('model_id','order_no')        
        model_ids = list(set([e.model_id for e in perm_objects]))

        model_objs = models.AppModel.objects.filter(pk__in=model_ids)
        model_name_dict = {e.pk:e.name for e in model_objs}

        response_dict = dict()

        for obj in perm_objects:
            model_name = model_name_dict.get(obj.model_id)
            if not response_dict.get(model_name):
                response_dict[model_name] = list()
            
            data = dict()
            data['id'] = obj.pk
            data['name'] = obj.name
            data['code'] = obj.code
            data['model_id'] = obj.model_id
            data['selected'] = True if obj.pk in selected_permission_list else False
        
            response_dict[model_name].append(data)

        result_list = list()
        for key,value in response_dict.items():
            res_obj = dict()
            res_obj['key'] = key
            res_obj['value'] = value
            result_list.append(res_obj)
        
        data = dict()
        data['selected_permission_list'] = selected_permission_list
        data['available_permission_list'] = result_list #get_profile_data(get_user)
        response_data = success_response(data=data)

        return Response(response_data, status=response_data["code"])

    def post(self, request,role_id):
        """
        for Update profile data
        """
                
        serializer_data = self.serializer_class(data=request.data)

        if serializer_data.is_valid():

            permission_ids  = serializer_data.data.get('permission_ids', list())

            print("\n ==> permission_ids: ", permission_ids)
            models.RolePermission.objects.filter(role_id=role_id).delete()

            for perm_id in permission_ids:
                data_obj = dict()
                data_obj['role_id'] = role_id
                data_obj['permission_id'] = perm_id
                data_obj['created_by'] = request.user.pk
                data_obj['updated_by'] = request.user.pk
                models.RolePermission.objects.create(**data_obj)

            data = permission_ids 
            response_data = success_response(data=data)

        else:
            error = get_serializer_errors(serializer_data.errors)
            response_data = error_response(error)

        return Response(response_data, status=response_data.get("code"))


class UpdatePermissionsData(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        for Retrieve profile data
        """

        from .models import AppModule, AppModel, Permission

        app_models = {
                'product': ['size', 'category', 'subcategory', 'importing', 'type', 'product'],
                'task': ['task'],
                'user': ['salesman', 'customer'],
                'role_permission': ['role'],
                'order': ['order'],
                'company': ['configuration'],
                'faq' : ['faq'],
                'cms':['cms'],
                'site_image': ['site_image']
            }
        
        action_list = [
            {'name': 'list', 'code': 'list',},
            {'name': 'view', 'code': 'view',},
            {'name': 'add', 'code': 'add',},
            {'name': 'edit', 'code': 'edit',},
            {'name': 'delete', 'code': 'delete',},
            {'name': 'change status', 'code': 'change_status',},
        ]

        for key in app_models.keys():
            obj = AppModule.objects.filter(name=key).first()
            if not obj:
                obj =  AppModule()
                obj.name =  key
                obj.save()

        c = 0
        for key,value_list in app_models.items():
            for value in value_list:
                module = AppModule.objects.filter(name=key).first()
                if module:
                    model_obj = AppModel.objects.filter(module_id=module.pk, name=value).first()
                    if not model_obj:
                        model_obj = AppModel()
                        model_obj.name = value
                        model_obj.module_id = module.pk
                        model_obj.save()

                    i = 0
                    for action in action_list:
                        i = i+1
                        perm_obj = Permission.objects.filter(code=action['code'], model_id=model_obj.pk).first()
                        if not perm_obj:
                            perm_obj = Permission()
                            perm_obj.name = action['name']
                            perm_obj.code = action['code']
                            perm_obj.model = model_obj
                            perm_obj.order_no = i
                            perm_obj.save()

                            c = c+1
            
        data = dict()
        data['permission_added'] = c
        response_data = success_response(data=data)

        return Response(response_data, status=response_data["code"])
