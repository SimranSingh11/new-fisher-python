from django.db import models
from base.models import BaseModel
from user.models import User
from product.models import Product, Size
from . import contants

# Create your models here.


class Order(BaseModel):

    customer = models.ForeignKey(User, related_name='order_customer', on_delete=models.CASCADE, db_column='customer_id')
    address = models.CharField(max_length=255, db_column='address')   
    latitude = models.FloatField(default=0.0, db_column='latitude')
    longitude = models.FloatField(default=0.0, db_column='longitude')
    amount = models.FloatField(default=0.0, db_column='amount')
    tax = models.FloatField(default=0.0, db_column='tax')
    net_amount = models.FloatField(default=0.0, db_column='net_amount')
    status = models.IntegerField(default=contants.PENDING, db_column='status')

    class Meta:
        verbose_name_plural = 'Orders'
        verbose_name = 'Order'
        db_table = 'order_master'


class OrderItem(BaseModel):

    order = models.ForeignKey(User, related_name='order_item_order', on_delete=models.CASCADE, db_column='order_id')
    product = models.ForeignKey(Product, related_name='order_item_product', on_delete=models.CASCADE, db_column='product_id')
    size = models.ForeignKey(Size, related_name='order_item_size', on_delete=models.CASCADE, db_column='size_id')
    quantity = models.IntegerField(default=1, db_column='quantity')
    amount = models.FloatField(default=0.0, db_column='amount')

    class Meta:
        verbose_name_plural = 'OrderItems'
        verbose_name = 'OrderItem'
        db_table = 'order_item_master'
