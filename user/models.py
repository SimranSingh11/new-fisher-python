from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
from user.constants import USER_TYPE_CHOICES
from app_fisher.settings import BACKEND_HOST
from base.models import BaseModel
from base.utils import get_unique_id


class User(AbstractUser, BaseModel):
    username = models.CharField(max_length=100, unique=True ,default=get_unique_id , db_column='username')
    image = models.ImageField(upload_to='img/user', null=True, db_column='image')
    user_type = models.CharField(choices=USER_TYPE_CHOICES,max_length=2,null=True,blank=True,db_column='user_type')
    dial_code = models.CharField(max_length=10, blank=True, null=True, db_column='dial_code')
    phone_number = models.CharField(max_length=15, blank=True, null=True, db_column='phone_number')
    language = models.IntegerField(blank=True, null=True, db_column='language')
    role_id = models.IntegerField(null=True, blank=True, db_column='role_id')
    forgot_pass_verify_code = models.CharField(max_length=100, blank=True, null=True, db_column='forgot_pass_verify_code')
    forgot_pass_verify_code_date = models.DateTimeField(blank=True, null=True, db_column='forgot_pass_verify_code_date')
    
    # Salseman
    date_of_birth = models.DateTimeField(blank=True, null=True, db_column='date_of_birth')
    address = models.TextField(blank=True, null=True, db_column='adsress')
    is_verified = models.BooleanField(default=False, db_column='is_verified')
    id_proof = models.ImageField(upload_to='img/id', null=True, db_column='id_proof')

    class Meta:
        verbose_name_plural = 'Users'
        verbose_name = 'User'
        db_table = 'user_master'

    def get_contact_number(self):
        dial_code = self.dial_code if self.dial_code else ''
        phone_number = self.phone_number if self.phone_number else ''

        return mark_safe("{} {}".format(dial_code, phone_number))


    def get_image_path(self):
        return  "{}{}".format(BACKEND_HOST,self.image.url) if self.image else None 
        # return  self.image 



