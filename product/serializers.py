from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from . import models


class SizeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, validators=[UniqueValidator(queryset=models.Size.objects.filter(is_deleted=False), message="already exists",)], error_messages={'required': 'Please enter title'})
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Size
        fields = ('id', 'title', 'is_active')


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, validators=[UniqueValidator(queryset=models.Category.objects.filter(is_deleted=False), message="already exists",)], error_messages={'required': 'Please enter title'})
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Category
        fields = ('id', 'title', 'is_active')


class SubCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, validators=[UniqueValidator(queryset=models.SubCategory.objects.filter(is_deleted=False), message="already exists",)], error_messages={'required': 'Please enter title'})
    category_id = serializers.IntegerField(required=True, error_messages={'required': 'Please select category'})
    is_active = serializers.BooleanField(read_only=True)
    category_title = serializers.SerializerMethodField()

    class Meta:
        model = models.SubCategory
        fields = ('id', 'title', 'category_id', 'is_active', 'category_title')

    def get_category_title(self, obj):
        return obj.category.title


class ImportingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, validators=[UniqueValidator(queryset=models.Importing.objects.filter(is_deleted=False), message="already exists",)], error_messages={'required': 'Please enter title'})
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Importing
        fields = ('id', 'title', 'is_active')
   

class TypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, validators=[UniqueValidator(queryset=models.Type.objects.filter(is_deleted=False), message="already exists",)], error_messages={'required': 'Please enter title'})
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = models.Type
        fields = ('id', 'title', 'is_active')


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, validators=[UniqueValidator(queryset=models.Product.objects.filter(is_deleted=False), message="already exists",)], error_messages={'required': 'Please enter title'})
    importing_id = serializers.IntegerField(required=True, error_messages={'required': 'Please select importing'})
    category_id = serializers.IntegerField(required=True, error_messages={'required': 'Please select category'})
    subcategory_id = serializers.IntegerField(required=True, error_messages={'required': 'Please select subcategory'})
    type_id = serializers.IntegerField(required=True, error_messages={'required': 'Please select type'})
    price = serializers.FloatField(required=True, error_messages={'required': 'Please select price'})

    is_active = serializers.BooleanField(read_only=True)
    is_favorite = serializers.BooleanField(read_only=True)
    importing_title = serializers.SerializerMethodField()
    category_title = serializers.SerializerMethodField()
    subcategory_title = serializers.SerializerMethodField()
    size_ids = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()


    class Meta:
        model = models.Product
        fields = ('id', 'title', 'image', 'glace', 'description', 'price',
                    'extra_note', 'is_active', 'is_favorite', 'importing_id', 
                    'category_id','subcategory_id', 'category_title', 'image_url',
                    'subcategory_title', 'importing_title', 'size_ids', 'type_id' )

    def get_importing_title(self, obj):
        return obj.importing.title

    def get_category_title(self, obj):
        return obj.category.title

    def get_subcategory_title(self, obj):
        return obj.subcategory.title

    def get_size_ids(self, obj):
        s_list = [e.pk for e in obj.sizes.all()]
        print("s_list: ",s_list)

        return s_list

    def get_image_url(self, obj):
        return obj.get_image_url()


class ProductFavoriteSerializer(serializers.Serializer):
    is_favorite = serializers.BooleanField(required=True)

