from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action

from django.db import models
from django.db.models import Q
from django.forms.models import model_to_dict
from django.http import Http404
from django.conf import settings

from base.api_response import success_response, error_response, get_serializer_errors, response_text
from base.utils import get_serach_term, p_print

from base.constants import PAGE_SIZE


class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return super(AllObjectsManager, self).get_queryset()


class DeletedManager(models.Manager):
    def get_queryset(self):
        return super(DeletedManager, self).get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    """
    common model with default common fields
    """
    objects = AllObjectsManager()
    is_active = models.BooleanField(default=True, db_column='is_active')
    is_deleted = models.BooleanField(db_index=True, default=False, db_column='is_deleted')
    created_by = models.IntegerField(blank=True, null=True, db_column='created_by')
    created_date = models.DateTimeField(blank=True, null=True, db_column='created_date', auto_now_add=True)
    updated_by = models.IntegerField(blank=True, null=True, db_column='updated_by')
    updated_date = models.DateTimeField(blank=True, null=True, db_column='updated_date', auto_now=True)

    class Meta:
        abstract = True


# ==================================================================================================#
#  BaseAPISet: Common class for listing and CRUD operation
# ==================================================================================================#

class BaseAPISet(viewsets.ModelViewSet):
    """
    BaseAPISet: Common class for listing and CRUD operation on Model

    @:param: No
    list - GET method will used for listing objects
    create - POST method will used for add new object

    with @:param: id(primary key)
    retrieve - GET method will used for get object detail
    update - PUT method will used for update object
    partial_update - PATCH method will used for  active/inactive object
    destroy - DELETE method will used for delete object
    ''
    """
    
    permission_classes = [AllowAny]
    model = None
    queryset = None
    serializer_class = None
    search_fields = None
    filter_fields = None
    sort_by = ['-created_date']
    apply_pagination = True
    page_size = PAGE_SIZE
    dropdown_fields = []

    def get_serializer_class(self):
        return self.serializer_class

    def get_queryset(self):

        if hasattr(self,'queryset') and self.queryset != None:
            return self.queryset
        elif hasattr(self,'model') and self.model:
             return self.model.objects.all()
        else:
            raise Http404("queryset or model does not exist")

    def get_object(self, pk):
        
        queryset = self.get_queryset()
        get_instance = queryset.filter(is_deleted=False, pk=pk).first()
        
        return get_instance

    def get_object_list(self, objects):
        """
        return list of objectd data dict
        @:param: list of objects
        ''
        """
        object_list = list()

        serializer_class = self.get_serializer_class()

        if not serializer_class:
            for obj in objects:
                object_list.append(model_to_dict(obj))
        else:
            for obj in objects:
                # object_list.append(model_to_dict(obj))
                object_list.append(serializer_class(obj).data)

        return object_list

    def get_object_data(self, instance):
        """
        return object data dict
        @:param: object
        ''
        """
        serializer_class = self.get_serializer_class()

        if not serializer_class:
            return model_to_dict(instance)

        else:
            # return model_to_dict(instance)
            return serializer_class(instance).data

    def get_object_view_data(self, instance):
        """
        return object data dict for viww
        @:param: object
        ''
        """
        serializer_class = self.get_serializer_class()

        if not serializer_class:
            return model_to_dict(instance)

        else:
            # return model_to_dict(instance)
            return serializer_class(instance).data

    # function for searching in list
    def get_search_query(self, request):
        """
        return search query condition
        @:param: request
        ''
        """
        query_condition = Q()
        if self.search_fields:
            if request.GET.get('search', None):
                search_term = request.GET.get('search').split(' ')
                if search_term:
                    sq_list = ['Q({0}__icontains="{1}")'.format(x, get_serach_term(y)) for x in self.search_fields for y
                               in search_term]
                    search_query_condition = ' | '.join(sq_list)
                    query_condition = query_condition & eval(search_query_condition)
        return query_condition

    # function for filter the list
    def get_filter_query(self, request):
        """
        return filter query condition
        @:param: request
        ''
        """
        query_condition = Q()
        for field in self.filter_fields:
            if request.GET.get(field, None):
                value = request.GET.get(field)
                query_condition = query_condition & eval("Q({0}={1})".format(field, value))
        return query_condition

    # function for pagination
    def get_pagination_data(self, request, query_condition):
        """
        return table list data with pagination
        @:param: request, query condition for objects list
        ''
        """
        import math
        page_size = request.GET.get('size', str(self.page_size))
        page_size = int(page_size) if page_size.isdigit() else self.page_size
        current_page = request.GET.get('page', '1')
        current_page = int(current_page) if current_page.isdigit() else 1
        limit = page_size * current_page
        offset = limit - page_size

        queryset = self.get_queryset()

        objects = queryset.filter(query_condition).order_by(*self.sort_by)[offset:limit]
        total_objects = queryset.filter(query_condition).order_by(*self.sort_by).count()
        total_pages = math.ceil(total_objects / page_size)

        pagination_data = dict()
        pagination_data['has_previous'] = True if (total_pages and current_page) > 1 else False
        pagination_data['has_next'] = True if (total_pages and current_page) < total_pages else False
        pagination_data['total_page'] = total_pages
        pagination_data['current_page'] = current_page
        pagination_data['size'] = page_size
        pagination_data['count'] = total_objects

        result = dict()
        result['data'] = self.get_object_list(objects)
        result['pagination'] = pagination_data

        return result

    def update_serializer_context(self, request):
        
        context = dict()

        if request.method == 'POST':
            context['created_by'] = request.user.id if request.user else None
        context['updated_by'] = request.user.id if request.user else None

        return context

    # ================ GET Method for getting  Table objects List ========================================= #

    def list(self, request):
        """
        @:param ==>
        search : for searching |
        page : for page no |
        size : for page size 
        """
        queryset = self.get_queryset()
        
        query_condition = Q(is_deleted=False)

        if self.search_fields:
            query_condition = query_condition & self.get_search_query(request)

        if self.filter_fields:
            query_condition = query_condition & self.get_filter_query(request)

        if self.apply_pagination:
            response_data_dict = self.get_pagination_data(request, query_condition)
        else:
            objects = queryset.filter(query_condition).order_by(*self.sort_by)
            response_data_dict = self.get_object_list(objects)

        data = response_data_dict

        response_data = success_response(data=data)

        return Response(response_data, status=response_data["code"])

    # ================ POST Method for create object (for new entry) ========================================= #

    def perform_create(self, serializer, request):
        instance = serializer.save()
        instance.created_by = request.user.id
        instance.updated_by = request.user.id
        instance.save()
        return instance

    def create(self, request):
        """
        Create a new object.
        """
        if settings.DEBUG:
            p_print("POST ==>: request.data", request.data)

        extra_context = self.update_serializer_context(request)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data, context=extra_context)

        if serializer.is_valid():
            self.perform_create(serializer, request)
            data = []
            response_data = success_response(data=data)

        else:
            if settings.DEBUG:
                print("\nSerializer Errors: ", serializer.errors, "\n")
            error = get_serializer_errors(serializer.errors)
            response_data = error_response(error)

        return Response(response_data, status=response_data["code"])

    # ==================================================================================================#

    def retrieve(self, request, pk):
        """
        Retrieve object by Id.
        """
        get_instance = self.get_object(pk)
 
        if get_instance:
            data = self.get_object_data(get_instance)
            response_data = success_response(data=data)
        else:
            error = { 'id': response_text[603]}
            response_data = error_response(error)

        return Response(response_data, status=response_data["code"])

    # ================ PUT Method to Update object details ========================================= #

    def perform_update(self, serializer, request):
        instance = serializer.save()
        instance.updated_by = request.user.id
        instance.save()
        return instance

    def update(self, request, pk):
        """
        Update object by Id.
        """
        if settings.DEBUG:
            print("\n============ PUT ==>: request.data =============\n")
            print("DEBUG: ", settings.DEBUG)
            print("\nrequest.data: ", request.data)
            print("\n=================================================\n")

        get_instance = self.get_object(pk)

        extra_context = self.update_serializer_context(request)

        if get_instance:

            serializer_class = self.get_serializer_class()
            serializer = serializer_class(get_instance, data=request.data, context=extra_context)

            if serializer.is_valid():
                self.perform_update(serializer, request)
                data = []
                response_data = success_response(data=data)
            else:
                if settings.DEBUG:
                    print("\nSerializer Errors: ", serializer.errors, "\n")
                error = get_serializer_errors(serializer.errors)
                response_data = error_response(error)

        else:
            error = { 'id': response_text[603]}
            response_data = error_response(error)
            return Response(response_data, status=response_data["code"])

        return Response(response_data, status=response_data["code"])

    # ================ PATCH Method to Change status (is_active : true/false) ================================= #

    def partial_update(self, request, pk):
        """
        Change active status (active/inactive) of object by Id.
        """
        instance = self.get_object(pk)

        if instance:
            instance.is_active = False if instance.is_active else True
            instance.updated_by = request.user.id
            instance.save()
            data = {'is_active': instance.is_active}
            response_data = success_response(data=data)
        else:
            error = { 'id': response_text[603]}
            response_data = error_response(error)

        return Response(response_data, status=response_data["code"])

    # ================ Delete Method to delete object =================================================== #

    def perform_destroy(self, instance, request):
        instance.is_active = False
        instance.is_deleted = True
        instance.updated_by = request.user.id
        instance.save()
        return instance    

    def destroy(self, request, pk):
        """
        Delete object by pk.
        """
        
        instance = self.get_object(pk)

        if instance:
            self.perform_destroy(instance, request)
            response_data = success_response()
        else:
            error = { 'id': response_text[603]}
            response_data = error_response(error)
        return Response(response_data, status=response_data["code"])

    # ================ Extra Method's  =================================================== #

    @action(detail=True, methods=['get'], name='view')
    def view(self, request, pk):
        """
        Retrieve object by Id for view.
        """
        get_instance = self.get_object(pk)

        if get_instance:
            data = self.get_object_view_data(get_instance)
            response_data = success_response(data=data)
        else:
            error = { 'id': response_text[603]}
            response_data = error_response(error)

        return Response(response_data, status=response_data["code"])

    @action(detail=False, methods=['get'], name='dropdown')
    def dropdown(self, request):
        """
        Get Dropdown List for model objects.
        """

        dropdown_list = list()

        if self.dropdown_fields:

            queryset = self.get_queryset()

            objects = queryset.filter(is_deleted=False, is_active=True).order_by(*self.sort_by).values(*self.dropdown_fields)

            print("objects", objects)
            # print("==> ", dict(objects))
            for obj in objects:
                data_info = dict()
                for ele in self.dropdown_fields:
                    data_info[ele] = obj[ele]

                dropdown_list.append(data_info)

        data = dropdown_list
        response_data = success_response(data=data)
        return Response(response_data, status=response_data["code"])

# ==================================================================================================#


