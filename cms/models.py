from django.db import models
from base.models import BaseModel
# Create your models here.

class Cms(BaseModel):
    title = models.CharField(max_length=255, db_column='title')
    key = models.TextField(null=True, blank=True, db_column='key')
    content = models.TextField(null=True, blank=True, db_column='content')

    class Meta:
        verbose_name_plural = 'Cms'
        verbose_name = 'Cms'
        db_table = 'cms_master'