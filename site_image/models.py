from django.db import models
from base.models  import BaseModel
from app_fisher.settings import BACKEND_HOST


class SiteImage(BaseModel):

    image = models.ImageField(upload_to='img/site', null=True, db_column='image')
    title = models.CharField(max_length=255, db_column='title')
    image_type = models.CharField(max_length=255, blank=True, null=True, db_column='image_type')
    image_key = models.CharField(max_length=255, blank=True, null=True, db_column='image_key')
    image_link = models.CharField(max_length=255, blank=True, null=True, db_column='image_link')
    description = models.TextField(blank=True, null=True, db_column='description')

    class Meta:
        verbose_name_plural = 'SiteImages'
        verbose_name = 'SiteImage'
        db_table = 'site_image_master'

    def get_image_url(self):
        return  "{}{}".format(BACKEND_HOST,self.image.url) if self.image else None 
