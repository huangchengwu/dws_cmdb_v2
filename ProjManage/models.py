from django.db import models
from ConfCen.models import *


 


# Create your models here.
class Projdep(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="项目名字", null=True, blank=True
    )
    group_list =[
            ("TBD_diylink正式", "TBD_diylink正式"),
            ("TBD_diylink测试", "TBD_diylink测试"),
            ("TBD_点餐测试", "TBD_点餐测试"),
            ("TBD_点餐正式", "TBD_点餐正式"),
            ("TBD_其他正式", "TBD_其他正式"),
            ("TBD_其他测试", "TBD_其他测试"),
            ("TBD_查看空间", "TBD_查看空间"),
        ]
    
    TaskEnc_select_Custom_Env = models.ForeignKey(
        TaskEnc,
        on_delete=models.CASCADE,
        verbose_name="任务封装",
        related_name="pk_TaskEnc_select_Custom_Env",
        null=True,
        blank=True,
    )

    Group = models.CharField(
        max_length=255,
        choices=group_list,
        default="TBD_其他测试",
        verbose_name="项目组",
    )

    cid = models.CharField(max_length=255, verbose_name="cid", null=True, blank=True)
    # action= models.CharField(max_length=255, verbose_name="当前动作",default="deploy")
    log_id = models.CharField(
        max_length=255, verbose_name="log_id", null=True, blank=True
    )
    ConfigContent = models.TextField(verbose_name="配置内容", null=True, blank=True)
    Describe = models.TextField(verbose_name="描述", default="", null=True, blank=True)
    task_name =  models.CharField(
        max_length=255, verbose_name="任务名", null=True, blank=True
    )
    class Meta:
        verbose_name = "项目部署"
        verbose_name_plural = verbose_name

        permissions = [
            ("TBD_diylink正式", "TBD_diylink正式"),
            ("TBD_diylink测试", "TBD_diylink测试"),
            ("TBD_点餐测试", "TBD_点餐测试"),
            ("TBD_点餐正式", "TBD_点餐正式"),
            ("TBD_其他正式", "TBD_其他正式"),
            ("TBD_其他测试", "TBD_其他测试"),
            ("TBD_查看空间", "TBD_查看空间"),
        ]
    def __str__(self):
        return "name : "+self.name+"group : "+self.Group