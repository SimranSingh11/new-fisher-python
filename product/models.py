from django.db import models
from base.models import BaseModel
from app_fisher.settings import BACKEND_HOST
# Create your models here.


class Size(BaseModel):
    title = models.CharField(max_length=255, db_column='title')
  
    class Meta:
        verbose_name_plural = 'Sizes'
        verbose_name = 'Size'
        db_table = 'size_master'


class Category(BaseModel):
    title = models.CharField(max_length=255, db_column='title')

    class Meta:
        verbose_name_plural = 'Categorys'
        verbose_name = 'Category'
        db_table = 'category_master'


class SubCategory(BaseModel):
    title = models.CharField(max_length=255, db_column='title')
    category = models.ForeignKey(Category, related_name='subcategory_category', on_delete=models.CASCADE, db_column='category_id')

    class Meta:
        verbose_name_plural = 'SubCategorys'
        verbose_name = 'SubCategory'
        db_table = 'subcategory_master'


class Importing(BaseModel):
    title = models.CharField(max_length=255, db_column='title')
  
    class Meta:
        verbose_name_plural = 'Importings'
        verbose_name = 'Importing'
        db_table = 'importing_master'


class Type(BaseModel):
    title = models.CharField(max_length=255, db_column='title')
  
    class Meta:
        verbose_name_plural = 'Types'
        verbose_name = 'Type'
        db_table = 'type_master'


class Product(BaseModel):
    title = models.CharField(max_length=255, db_column='title')
    image = models.ImageField(upload_to='img/product', null=True, db_column='image')
    glace = models.CharField(max_length=255, blank=True, null=True, db_column='glace')
    description = models.TextField(blank=True, null=True, db_column='description')
    extra_note = models.TextField(blank=True, null=True, db_column='extra_note')
    importing = models.ForeignKey(Importing, related_name='product_importing', on_delete=models.CASCADE, db_column='importing_id')
    category = models.ForeignKey(Category, related_name='product_category', on_delete=models.CASCADE, db_column='category_id')
    subcategory = models.ForeignKey(SubCategory, related_name='product_subcategory', on_delete=models.CASCADE, db_column='subcategory_id')
    is_favorite = models.BooleanField(default=False, db_column='is_favorite')
    type = models.ForeignKey(Type, related_name='product_type', on_delete=models.CASCADE, db_column='type_id')
    sizes = models.ManyToManyField(Size)
    price = models.FloatField(default=0.0, db_column='price')

    class Meta:
        verbose_name_plural = 'Products'
        verbose_name = 'Product'
        db_table = 'product_master'
    
    def get_image_url(self):
        return  "{}{}".format(BACKEND_HOST,self.image.url) if self.image else None 

    def get_importing(self):
        data_info = dict()
        data_info['title'] = self.importing.title
        return data_info
    
    def get_category(self):
        data_info = dict()
        data_info['title'] = self.category.title
        return data_info


    def get_subcategory(self):
        data_info = dict()
        data_info['title'] = self.subcategory.title
        return data_info

    def get_type(self):
        data_info = dict()
        data_info['title'] = self.type.title
        return data_info

    def get_size(self):
        print("self.sizes: ", self.sizes)
        data_info = dict()
        data_info['size'] = [ {'id': ele.pk, 'title': ele.title}  for ele in self.sizes.filter(is_deleted=False, is_active=True)] 
        return data_info