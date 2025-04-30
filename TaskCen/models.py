from django.db import models
from ConfCen.models import *



# Create your models here.
class Task(models.Model):
    Id = models.AutoField(primary_key=True)
    status = [
        ("发布中", "发布中"),
        ("已发布", "已发布"),
    ]
  
    deploy_env = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name="项目选择",
        related_name="pk_project",
        null=True,
    )
    content = models.TextField(verbose_name="发布内容", default="...")
    status = models.CharField(
        choices=status, max_length=255, verbose_name="发布状态", default=0
    )
  
    task_type = models.ForeignKey(
        Task_type,
        on_delete=models.CASCADE,
        verbose_name="任务类型",
        related_name="pk_task_type",
        null=True,
    )

    version = models.CharField(
        max_length=255, verbose_name="发布版本", default="", null=True, blank=True
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name = "任务创建"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.version
