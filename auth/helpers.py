from user.models import User
# from role_permission.helpers import get_role_wise_module_permissions, get_super_module_permissions
from user.helpers import  get_user_obj_data



def get_profile_data(user_object):
    return get_user_obj_data(user_object)

    
def get_login_user_dict(request, user_object, token):
    
    user_info = get_user_obj_data(user_object)
    token_info = {
        'token': token.key,
        'type':'Token'
    }
    result = dict()
    result['User'] = user_info
    result['Token'] = token_info

    permission_dict = dict()  # TODO get_super_module_permissions() if user_object.is_superuser else get_role_wise_module_permissions(user_object.role_id)
    result['Permission'] = permission_dict

    return result 


def get_user_dict(request, user_object):    
    user_info = get_user_obj_data(user_object)
 
    return user_info


def password_reset_email(request, user_object):
    
    from django.utils import timezone
    from django.conf import settings
    from base.utils import get_unique_id
    from app_fisher.settings import FRONTRND_BASE_URL
    from my_helpers.email_thread import EmailThread

    activation_code = get_unique_id()
    user_object.forgot_pass_verify_code = activation_code
    user_object.forgot_pass_verify_code_date = timezone.now()
    user_object.save()

    # TODO make proper link
    email_link = 'http://' + FRONTRND_BASE_URL + '/auth/reset-password/' + str(activation_code)

    subject = "{0} - Forgot your password".format(settings.APP_NAME)
    message = "{0} ".format(email_link)
    to_user = [user_object.email]
    email = EmailThread()
    email.set_email(subject=subject, message=message, to_email_list=to_user)
    email.start()
