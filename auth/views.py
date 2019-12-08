from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from rest_framework.decorators import api_view,permission_classes

from rest_framework import viewsets
from rest_framework.decorators import action

# from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.views.decorators.csrf import csrf_exempt

from base.api_response import success_response, error_response, get_serializer_errors, response_text, api_message

from auth import serializers
from auth.helpers import get_login_user_dict, password_reset_email, get_profile_data

auth_model = get_user_model()

# Create your views here.

# =================================================================================== #
# UserAuthAPISet
# methods:
# (1) login
# (2) logout
# =================================================================================== #

class UserAuthAPISet(viewsets.GenericViewSet):
    """
    UserAuthAPISet: class for user auth
    ''
    """
    serializer_class = serializers.LoginSerializer

    def get_serializer_class(self):
        if self.action == 'login':
            return serializers.LoginSerializer
        if self.action == 'change_password':
            return serializers.ChangePasswordSerializer
        if self.action == 'forgot_password':
            return serializers.ForgotPasswordSerializer
        if self.action == 'reset_password':
            return serializers.ResetPasswordSerializer
        
        return self.serializer_class


    # =================================================================================== #
    #  login
    # =================================================================================== #
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    # @csrf_exempt
    def login(self, request):
        """
        user login api 
        """
       
        print("\n=====> Login Data:",request.data)

        serializer_class = self.get_serializer_class()
        serializer_data = serializer_class(data=request.data)
       
        if serializer_data.is_valid():
            
            user_email = serializer_data.data.get('email')
            user_password = serializer_data.data.get('password')

            get_user = auth_model.objects.filter(is_deleted=False, email=user_email).first()

            if get_user:

                if get_user.is_active:

                    if get_user.check_password(user_password):
                        token = Token.objects.get_or_create(user=get_user)[0]  # TokenAuthentication
                        # get_user.is_online = True
                        get_user.save()            
                        data = get_login_user_dict(request, get_user, token)
                        message = api_message['login_success']
                        response_data = success_response(data=data, message=message)

                    else:
                        # Here email is exist but password is wrong so success is True but code is 400            
                        
                        error = {'password': api_message['wrong_password']}
                        response_data = error_response(error)
                                       
                else:        
                    
                    error = {'email': api_message['account_deactivated']}
                    response_data = error_response(error) 

            else:    
                
                error = {'email': api_message['email_not_exist']}
                response_data = error_response(error)  
        else:
            print("serializer_data:", serializer_data.errors)
            error = get_serializer_errors(serializer_data.errors)
            response_data = error_response(error)
           
        return Response(response_data, status=response_data.get("code"))


    # =================================================================================== #
    #  logout
    # =================================================================================== #

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """
        user logout api 
        ''
        """
        token = Token.objects.get(user=request.user)
        token.delete()
        # data = list()
        message = api_message['success_logout']
        response_data = success_response()      
        return Response(response_data,status=response_data["code"])


    # =================================================================================== #
    #  check_user_token
    # =================================================================================== #

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def check_user_token(self, request):
        """
        api to check user token
        ''
        """
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
        user = request.user
        token_obj = Token.objects.filter(key=token, user_id=user.id).first()
        if token_obj:
            success = True
            data = get_login_user_dict(request, user, token_obj)
            response_data = success_response(data=data)
        else:
            success = False
            
            error = {'token' : api_message['login_again']}
            response_data = error_response(error=error)

        return Response(response_data, status=response_data.get("code"))


    # =================================================================================== #
    #  change_password
    # =================================================================================== #

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """
        api to change user password
        ''
        """
        user = request.user

        serializer_class = self.get_serializer_class()

        serializer_data = serializer_class(data=request.data)

        if serializer_data.is_valid():

            old_password = request.data.get('old_password')
            if user.check_password(old_password):
                new_password = request.data.get('new_password')
                user.set_password(new_password)
                user.save()

                success = True
                data = []
                response_data = success_response(data=data)
            else:
                success = False
                
                error = {'old_password': "Old password not match"}
                response_data = error_response(error)

        else:
            success = False
            error = get_serializer_errors(serializer_data.errors)
            response_data = error_response(error)

        return Response(response_data, status=response_data.get("code"))


    # =================================================================================== #
    #  change_password
    # =================================================================================== #

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def forgot_password(self, request):
        """
        api to change forgot password
        ''
        """

        serializer_class = self.get_serializer_class()

        serializer_data = serializer_class(data=request.data)

        if serializer_data.is_valid():
            
            user_object = auth_model.objects.filter(is_deleted=False, email=serializer_data.data.get('email')).first()
            if not user_object:
                
                error = {'email': 'The contact email is not registered'}
                response_data = error_response(error)
         
            elif not user_object.is_active:
                
                error = {'email': 'The contact email is not active or verified, Please contact admin'}
                response_data = error_response(error)
            else:
                password_reset_email(request, user_object)
                data = dict()
                message = "Reset password link has been sent your registered email id, Please check your mail"
                response_data = success_response(data=data, message=message)
        else:
            error = get_serializer_errors(serializer_data.errors)
            response_data = error_response(error)

        return Response(response_data, status=response_data.get("code"))


    # =================================================================================== #
    #  reset_password
    # =================================================================================== #

    @action(detail=True, methods=['get', 'post'], permission_classes=[AllowAny])
    def reset_password(self, request, pk):
        """
        api to change forgot password
        ''
        """
        
        forgot_pass_token = pk
        response_data = success_response()

        if request.method == 'GET':
            
            user_object = auth_model.objects.filter(is_deleted=False, forgot_pass_verify_code=forgot_pass_token).first()

            if user_object:

                data = {
                    'valid': True,
                    'user_id':  user_object.pk
                    }
                response_data = success_response(data=data)
            else:
                error = {'valid': False }
                response_data = error_response(error)

        elif request.method == 'POST':
            
            serializer_class = self.get_serializer_class()

            serializer_data = serializer_class(data=request.data)
        
            if serializer_data.is_valid():
                user_object = auth_model.objects.filter(is_deleted=False, pk=serializer_data.data.get('user_id'),
                                                        forgot_pass_verify_code=forgot_pass_token).first()

                if user_object:
                    new_password = request.data.get('new_password')
                    user_object.set_password(new_password)
                    user_object.forgot_pass_verify_code = None  # TODO
                    user_object.save()

                    data = dict()
                    message = api_message['success_password_changed']
                    response_data = success_response(data=data, message=message)

                else:
                    
                    error = {'token' : 'Forgot password token is not valid, try again'}
                    response_data = error_response(error)

            else:
                error = get_serializer_errors(serializer_data.errors)
                response_data = error_response(error)

        return Response(response_data, status=response_data.get("code"))


# =================================================================================== #
# UserProfileView
# methods:
# (1) get : to get profile
# (2) post : to update profile
# =================================================================================== #

class UserProfileView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserProfileSerializer

    def get(self, request):
        """
        for Retrieve profile data
        """

        get_user = request.user
        data = get_profile_data(get_user)
        response_data = success_response(data=data)

        return Response(response_data, status=response_data["code"])

    def post(self, request):
        """
        for Update profile data
        """
                
        serializer_data = self.serializer_class(request.user, data=request.data)

        if serializer_data.is_valid():

            user_obj = serializer_data.save()
            user_obj.updated_by = request.user.pk
            user_obj.save()

            data = get_profile_data(user_obj)
            response_data = success_response(data=data)

        else:
            error = get_serializer_errors(serializer_data.errors)
            response_data = error_response(error)

        return Response(response_data, status=response_data.get("code"))

