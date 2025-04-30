from django.db import models
from django.utils import timezone
from ConfCen.models import *
from django.http import FileResponse
# Create your models here.
values = """
storageClassName:   csi-cephfs-sc
redis:
  image: redis:alpine
  storage: 8Gi
  password: idc123456
"""
class monitor(models.Model):
    Id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=255, verbose_name="发布状态", default="进行中")
    def __str__(self):
        return str(self.Id)


class TaskDeploy(models.Model):
    Id = models.AutoField(primary_key=True)
    taskdeploy_env = models.ForeignKey(
        TaskCreate,
        on_delete=models.CASCADE,
        verbose_name="任务选择",
        related_name="pk_taskcreate",
        null=True,
    )
    task_type = models.ForeignKey(
        Task_type,
        on_delete=models.CASCADE,
        verbose_name="任务类型",
        related_name="pk_task_type",
        null=True,
    )
    select_HostGroup = models.ForeignKey(
        HostGroup,
        on_delete=models.CASCADE,
        verbose_name="select_HostGroup",
        related_name="pk_select_HostGroup",
        null=True,
        blank=True,
    )
    select_k8s_Env = models.ForeignKey(
        k8s_Env,
        on_delete=models.CASCADE,
        verbose_name="select_k8s_Env",
        related_name="pk_select_k8s_Env",
        null=True,
        blank=True,
    )
    select_Custom_Env = models.ForeignKey(
        Custom_Env,
        on_delete=models.CASCADE,
        verbose_name="自定义变量配置",
        related_name="pk_select_Custom_Env",
        null=True,
        blank=True,
    )
    class Meta:
        verbose_name = "任务列表"
        verbose_name_plural = verbose_name

    log_id = models.CharField(max_length=255, verbose_name="日志id", default="0")
    version = models.CharField(max_length=255, verbose_name="版本号", default="100")
    User = models.CharField(max_length=255, verbose_name="创建用户", null=True, blank=True)

    status = models.CharField(max_length=255, verbose_name="发布状态", default="进行中")

    result = models.TextField(verbose_name="任务结果", default="")



    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return str(self.taskdeploy_env)



