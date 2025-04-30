from django.db import models

class WebManger(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="网站名字", default="", unique=True
    )
    username = models.CharField(
        max_length=255, verbose_name="用户名称", default=""
    )
    password = models.CharField(
        max_length=255, verbose_name="密码", default=""
    )
    url = models.CharField(
        max_length=255, verbose_name="网站链接", default="", unique=True
    )
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "网站管理"
        verbose_name_plural = verbose_name