from django.db import models
from mdeditor.fields import MDTextField
from ConfCen.models import * 
# Create your models here.


class HelpDocuments(models.Model):
    Id = models.AutoField(primary_key=True)
    
    title = models.CharField(
        max_length=255, verbose_name="标题", default="cloud7", unique=True)
    
    content = MDTextField(verbose_name="内容")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "帮助文档"
        verbose_name_plural = verbose_name
