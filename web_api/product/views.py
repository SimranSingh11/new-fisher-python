from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# from rest_framework.decorators import api_view,permission_classes
from django.db.models import Q
from base.utils import get_serach_term, p_print


from base.api_response import success_response, error_response
from product import models


class ProductListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    search_fields = []
    filter_fields = ['category_id', ]
    page_size = 10
    sort_by= ['-pk']

    def get_queryset(self):
        return models.Product.objects.all()


    # function for searching in list
    def get_search_query(self, request):
        
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
        
        query_condition = Q()
        for field in self.filter_fields:
            if request.GET.get(field, None):
                value = request.GET.get(field)
                query_condition = query_condition & eval("Q({0}={1})".format(field, value))
        return query_condition



    # function for pagination
    def get_pagination_data(self, request, query_condition):
        
        import math
        page_size = request.GET.get('size', str(self.page_size))
        page_size = int(page_size) if page_size.isdigit() else self.page_size
        current_page = request.GET.get('page', '1')
        current_page = int(current_page) if current_page.isdigit() else 1
        limit = page_size * current_page
        offset = limit - page_size

        objects = models.Product.objects.filter(query_condition).order_by(*self.sort_by)[offset:limit]
        total_objects = models.Product.objects.filter(query_condition).order_by(*self.sort_by).count()
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

    def get_object_list(self, objects):
        data_list = list()

        for obj in objects:
            data_info = dict()
            data_info['id'] = obj.pk
            data_info['title'] = obj.title
            data_info['image'] = obj.get_image_url()
            data_info['glace'] = obj.glace
            data_info['description'] = obj.description
            data_info['extra_note'] = obj.extra_note
            data_info['importing'] = obj.get_importing()
            data_info['category'] = obj.get_category()
            data_info['subcategory'] = obj.get_subcategory()
            data_info['is_favorite'] = obj.is_favorite
            data_info['type'] = obj.get_type()
            data_info['sizes'] = obj.get_size()
            data_info['price'] = obj.price
            data_list.append(data_info)
        return data_list

    def get(self, request):

        queryset = self.get_queryset()
        
        query_condition = Q(is_deleted=False, is_active=True)

        if self.search_fields:
            query_condition = query_condition & self.get_search_query(request)

        if self.filter_fields:
            query_condition = query_condition & self.get_filter_query(request)

        response_data_dict = self.get_pagination_data(request, query_condition)

        data = response_data_dict

        response_data = success_response(data=data)

        return Response(response_data, status=response_data["code"])



class ProductDetailView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        """
        for Retrieve product data
        """
        obj =  models.Product.objects.filter(pk=pk, is_deleted=False, is_active=True).first()

        if obj:            
            data_info = dict()
            data_info['id'] = obj.pk
            data_info['title'] = obj.title
            data_info['image'] = obj.get_image_url()
            data_info['glace'] = obj.glace
            data_info['description'] = obj.description
            data_info['extra_note'] = obj.extra_note
            data_info['importing'] = obj.get_importing()
            data_info['category'] = obj.get_category()
            data_info['subcategory'] = obj.get_subcategory()
            data_info['is_favorite'] = obj.is_favorite
            data_info['type'] = obj.get_type()
            data_info['sizes'] = obj.get_size()
            data_info['price'] = obj.price            
            response_data = success_response(data=data_info)
        else:
            response_data = error_response(code=404)

        return Response(response_data, status=response_data["code"])



class SizeListView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        for Retrieve product data
        """
        objs =  models.Size.objects.filter(is_deleted=False, is_active=True)

        data_list = list()
        for obj in objs:
            data_info = dict()
            data_info['id'] = obj.pk
            data_info['title'] = obj.title
            data_list.append(data_info)  
        response_data = success_response(data=data_list)

        return Response(response_data, status=response_data["code"])


class CategoryListView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        for Retrieve product data
        """
        objs =  models.Category.objects.filter(is_deleted=False, is_active=True)

        data_list = list()
        for obj in objs:
            data_info = dict()
            data_info['id'] = obj.pk
            data_info['title'] = obj.title
            data_list.append(data_info)  
       
        response_data = success_response(data=data_list)

        return Response(response_data, status=response_data["code"])


class SubCategoryListView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        for Retrieve product data
        """
        objs =  models.SubCategory.objects.filter(is_deleted=False, is_active=True)

        data_list = list()
        for obj in objs:
            data_info = dict()
            data_info['id'] = obj.pk
            data_info['title'] = obj.title
            data_list.append(data_info)  
        response_data = success_response(data=data_list)

        return Response(response_data, status=response_data["code"])


class ImportingListView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        for Retrieve product data
        """
        objs =  models.Importing.objects.filter(is_deleted=False, is_active=True)

        data_list = list()
        for obj in objs:
            data_info = dict()
            data_info['id'] = obj.pk
            data_info['title'] = obj.title
            data_list.append(data_info)  
        response_data = success_response(data=data_list)

        return Response(response_data, status=response_data["code"])


class TypeListView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        for Retrieve product data
        """
        objs =  models.Type.objects.filter(is_deleted=False, is_active=True)

        data_list = list()
        for obj in objs:
            data_info = dict()
            data_info['id'] = obj.pk
            data_info['title'] = obj.title
            data_list.append(data_info)  
        response_data = success_response(data=data_list)

        return Response(response_data, status=response_data["code"])



class BannerImagesListView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        for Retrieve Banner data
        """
        objs =  models.Product.objects.filter(is_deleted=False, is_active=True)

        data_list = list()
        for obj in objs:
            data_info = dict()
            data_info['id'] = obj.pk
            data_info['title'] = obj.title
            data_info['price'] = obj.price
            data_info['image'] = obj.get_image_url()
            data_list.append(data_info)  
        response_data = success_response(data=data_list)

        return Response(response_data, status=response_data["code"])


