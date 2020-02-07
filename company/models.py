from django.db import models
from base.models import BaseModel

# Create your models here.

class Configuration(BaseModel):
    app_name = models.CharField(max_length=255, db_column='app_name')
    logo = models.ImageField(upload_to='img/company', null=True, db_column='image')
    description = models.TextField(blank=True, null=True, db_column='description')
    currency = models.CharField(max_length=10, db_column='currency')
    page_size = models.IntegerField(default=10, db_column='page_size')

    facebook_link = models.CharField(max_length=255, db_column='facebook_link')
    twitter_link = models.CharField(max_length=255, db_column='twitter_link')
    youtube_link = models.CharField(max_length=255, db_column='youtube_link')

    class Meta:
        verbose_name_plural = 'Configurations'
        verbose_name = 'Configuration'
        db_table = 'configuration_master'
    
    def get_logo_url(self):
        return  "{}{}".format(BACKEND_HOST,self.logo.url) if self.logo else None 