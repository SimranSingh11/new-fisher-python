from django.db import models
from base.models import BaseModel

# Create your models here.

class Configuration(BaseModel):

    name = models.CharField(null=True, blank=True, max_length=255, db_column='name')
    code = models.CharField(null=True, blank=True, max_length=255, db_column='code')
    value = models.CharField(null=True, blank=True, max_length=255, db_column='value')

    class Meta:
        verbose_name_plural = 'Configurations'
        verbose_name = 'Configuration'
        db_table = 'configuration_master'
    