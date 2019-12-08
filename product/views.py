from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from base.api_response import success_response, error_response, api_message, response_text, get_serializer_errors
from base.models import BaseAPISet

from . import models
from . import serializers


class SizeAPISet(BaseAPISet):

    permission_classes = [IsAuthenticated]
    model = models.Size
    serializer_class = serializers.SizeSerializer
    search_fields = ['title']
    dropdown_fields = ['id', 'title']


class CategoryAPISet(BaseAPISet):

    permission_classes = [IsAuthenticated]
    model = models.Category
    serializer_class = serializers.CategorySerializer
    search_fields = ['title']
    dropdown_fields = ['id', 'title']


class SubCategoryAPISet(BaseAPISet):

    permission_classes = [IsAuthenticated]
    model = models.SubCategory
    serializer_class = serializers.SubCategorySerializer
    search_fields = ['title']
    filter_fields = ['category_id']
    dropdown_fields = ['id', 'title', 'category_id']


class ImportingAPISet(BaseAPISet):

    permission_classes = [IsAuthenticated]
    model = models.Importing
    serializer_class = serializers.ImportingSerializer
    search_fields = ['title']
    dropdown_fields = ['id', 'title']


class TypeAPISet(BaseAPISet):

    permission_classes = [IsAuthenticated]
    model = models.Type
    serializer_class = serializers.TypeSerializer
    search_fields = ['title']
    dropdown_fields = ['id', 'title']


class ProductAPISet(BaseAPISet):

    permission_classes = [IsAuthenticated]
    model = models.Product
    serializer_class = serializers.ProductSerializer
    search_fields = ['title']
    dropdown_fields = ['id', 'title']

    def get_serializer_class(self):
        if self.action == 'favorite':
            return serializers.ProductFavoriteSerializer       
        return self.serializer_class


    def get_object_list(self, objects):
        """
        return list of objectd data dict
        @:param: list of objects
        """
        object_list = list()

        for obj in objects:
            list_data = dict()
            list_data['id'] = obj.pk
            list_data['title'] = obj.title
            list_data['category_title'] = obj.category.title
            list_data['subcategory_title'] = obj.subcategory.title
            list_data['importing_title'] = obj.importing.title
            list_data['is_active'] = obj.is_active
            list_data['is_favorite'] = obj.is_favorite            
            object_list.append(list_data)

        return object_list

    def perform_create(self, serializer, request):

        instance = serializer.save()
        instance.created_by = request.user.id
        instance.updated_by = request.user.id
        instance.save()
        
        sizes = request.data.get('sizes', [])
        instance.sizes.set([int(e) for e in sizes.split(',')])

        return instance


    def perform_update(self, serializer, request):
        instance = serializer.save()
        instance.updated_by = request.user.id
        instance.save()

        sizes = request.data.get('sizes', [])
        instance.sizes.clear()
        instance.sizes.set([int(e) for e in sizes.split(',')])

        return instance

    @action(detail=True, methods=['post'], name='favorite')
    def favorite(self, request, pk):
        """
        favorite/Unfavorite product by id.
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        if serializer.is_valid():
            self.model.objects.filter(pk=pk).update(is_favorite=serializer.data.get('is_favorite'))
            response_data = success_response()
        else:
            error = get_serializer_errors(serializer.errors)
            response_data = error_response(error)

        return Response(response_data, status=response_data["code"])
    

    @action(detail=False, methods=['get'], name='form_dropdowm_list')
    def form_dropdowm_list(self, request):
        """
        get dropdown list for add product form
        """
        from django.db.models import Q

        result_data = dict()

        q_condition = Q(is_deleted=False, is_active=True)

        category_list =  models.Category.objects.filter(q_condition).values_list('id', 'title')
        category_list = [{'id':obj[0], 'title': obj[1]} for obj in category_list]

        subcategory_list =  models.SubCategory.objects.filter(q_condition).values_list('id', 'title', 'category_id')
        subcategory_list = [{'id':obj[0], 'title': obj[1], 'category_id': obj[2]} for obj in subcategory_list]

        importing_list =  models.Importing.objects.filter(q_condition).values_list('id', 'title')
        importing_list = [{'id':obj[0], 'title': obj[1]} for obj in importing_list]

        type_list =  models.Type.objects.filter(q_condition).values_list('id', 'title')
        type_list = [{'id':obj[0], 'title': obj[1]} for obj in type_list]

        size_list =  models.Size.objects.filter(q_condition).values_list('id', 'title')
        size_list = [{'id':obj[0], 'title': obj[1]} for obj in size_list]

        result_data['category'] = category_list
        result_data['subcategory'] = subcategory_list
        result_data['importing'] = importing_list
        result_data['type'] = type_list
        result_data['size'] = size_list


        response_data = success_response(data=result_data)
        return Response(response_data, status=response_data["code"])