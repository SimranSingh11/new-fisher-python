from . import models


def get_role_wise_permissions_detail(role_id):
    
    perm_objs = models.RolePermission.objects.filter(role_id=role_id).values('permission_id','permission__name', 'permission__model__name', 'permission__model__module__name')

    permission_dict = dict()

    for obj in perm_objs:
        
        data_dict = dict()
        data_dict['id'] = obj['permission_id']
        data_dict['name'] = obj['permission__name']

        if not permission_dict.get(obj['permission__model__module__name']):
            permission_dict[obj['permission__model__module__name']] = dict()
        
        if not permission_dict[obj['permission__model__module__name']].get(obj['permission__model__name']):
            permission_dict[obj['permission__model__module__name']][obj['permission__model__name']] = list()
        
        permission_dict[obj['permission__model__module__name']][obj['permission__model__name']].append(data_dict)
    
    return permission_dict


def get_role_wise_module_permissions(role_id):
    
    # perm_objs = models.Permission.objects.filter(is_active=True).values('code', 'model__name', 'model__module__name')
    perm_objs = models.RolePermission.objects.filter(role_id=role_id).values('permission__code', 'permission__model__name', 'permission__model__module__name')

    permission_dict = dict()

    permission_dict['module'] = list()
    permission_dict['permission'] = dict()

    if role_id and perm_objs:
        for obj in perm_objs:
        
            if obj['permission__model__name'] not in permission_dict['module']:
                permission_dict['module'].append(obj['permission__model__name'])
            
            if not permission_dict['permission'].get(obj['permission__model__name']):
                permission_dict['permission'][obj['permission__model__name']] = list()
                    
            permission_dict['permission'][obj['permission__model__name']].append(obj['permission__code'])
        
    return permission_dict



def get_super_module_permissions():
    
    perm_objs = models.Permission.objects.filter(is_active=True).values('code', 'model__name', 'model__module__name')
    permission_dict = dict()

    permission_dict['module'] = list()
    permission_dict['permission'] = dict()


    for obj in perm_objs:
    
        if obj['model__module__name'] not in permission_dict['module']:
            permission_dict['module'].append(obj['model__module__name'])
        
        if not permission_dict['permission'].get(obj['model__name']):
            permission_dict['permission'][obj['model__name']] = list()
                
        permission_dict['permission'][obj['model__name']].append(obj['code'])
    
    return permission_dict
