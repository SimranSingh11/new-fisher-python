from django.db import models
from base.models import BaseModel
# Create your models here.


class Faq(BaseModel):
    title = models.CharField(null=True, blank=True, max_length=255, db_column='title')
    question = models.TextField(null=True, blank=True, db_column='question')
    answer = models.TextField(null=True, blank=True, db_column='answer')

    class Meta:
        verbose_name_plural = 'Faqs'
        verbose_name = 'Faq'
        db_table = 'faq_master'
