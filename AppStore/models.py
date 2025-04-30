from django.db import models

# Create your models here.

class AppMarket(models.Model):
    Id = models.AutoField(primary_key=True)
    class Meta:
        verbose_name = "云应用管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Id
