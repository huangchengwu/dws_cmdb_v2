from django.db import models
from ConfCen.models import * 
# Create your models here.
class k8s_cluster_create(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="名字", default="集群名字", unique=True
    )
    types = [
        ("正式集群", "正式集群"),
        ("测试集群", "测试集群"),
    ]

    Master = models.ManyToManyField(HostConfig)

    Node = models.ManyToManyField(HostConfig)

 
    types = models.CharField(
        choices=types, max_length=255, verbose_name="类型", default=0
    )

    class Meta:
        verbose_name = "集群创建"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    


class k8s_node(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="名字", default="hellowolrd", unique=True
    )

    config = models.TextField(
        max_length=255, verbose_name="配置", default="", unique=True
    )
    class Meta:
        verbose_name = "添加node"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
class k8s_master(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="名字", default="hellowolrd", unique=True
    )

 
    class Meta:
        verbose_name = "添加master"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name