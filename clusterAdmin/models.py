from django.db import models
from ConfCen.models import *


# Create your models here.
class k8s_network(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="名字", default="专线1", unique=True
    )
    k8s_network_host = models.ForeignKey(
        HostConfig,
        on_delete=models.CASCADE,
        verbose_name="主机选择",
        related_name="pk_k8s_network_host",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "专线创建"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % (self.Id)


class k8s_cluster(models.Model):
    Id = models.AutoField(primary_key=True,default=0)
    name = models.CharField(
        max_length=255, verbose_name="名字", default="曼谷测试", unique=True
    )

    select_node_host = models.ManyToManyField(HostConfig)

    class Meta:
        verbose_name = "创建集群"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % (self.Id)


# 加节点
class node(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="名字", default="node[曼谷]", unique=True
    )

    k8s_cluster = models.ForeignKey(
        k8s_cluster,
        on_delete=models.CASCADE,
        verbose_name="归属集群",
        related_name="pk_k8s_cluster",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "添加节点"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class k8s_cluster_list(models.Model):
    Id = models.AutoField(primary_key=True)

    class Meta:
        verbose_name = "集群列表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % (self.Id)
