import json

"""
=============================================================
common function to get serializer errors in dictionary format
=============================================================
"""
def get_serializer_errors(error_dict):
    """
    return dict of serializer errors
    @:param: error_dict
    ''
    """
    result = dict()
    error_dict = dict(error_dict)
    for error in error_dict:
        result[error] = json.dumps(error_dict[error]).strip('"[]')
    return result


"""
=============================================================
common function to success response
=============================================================
"""
def success_response(data=list(), message=None, code=200):
    """
    common success response for api
    ''
    """
    success = True

    result = dict()
    if data != list():
        result['data'] = data
    if message:
        result['data']['message'] = message
    if data == list() and (message == '' or (not message)):
        result['data'] = data

    result['error'] = []
    result['success'] = success
    result['code'] = code

    return result

"""
=============================================================
common function to error response
=============================================================
"""
def error_response(error=list(), code=200):
    """
    common error response for api   
    """
    success = False
    result = dict()
    result['data'] = dict()
    result['error'] = error
    result['success'] = success
    result['code'] = code
    return result


"""
=============================================================
common response text of code for api
=============================================================
"""
response_text = {
    200: "Success",
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    500: 'Internal Server Error',
    601: 'Data Duplication',
    602: 'Could Not Save',
    603: 'No data found',
}


"""
=============================================================
common messages for api
=============================================================
"""
api_message = {			
    'user_not_exist' : 'User not exists',
    'email_not_exist' : 'Email not exists',
    'wrong_credentials' : 'Wrong credentials',
    'wrong_password' : 'Wrong password',
    'account_deactivated' : 'Account deactivated',
    'login_success' : 'Login success',
    'success_logout' : 'Logout success',
    'success_password_changed': 'Password has been successfully changed.',
}
