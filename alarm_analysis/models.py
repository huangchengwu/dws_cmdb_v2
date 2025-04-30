from django.db import models
 


# Create your models here.
class Alert(models.Model):
    Id = models.AutoField(primary_key=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    class Meta:
        verbose_name = "报警信息"
        verbose_name_plural = verbose_name


class AlertGroup(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="组名", default="报警类名", unique=True
    )

    group = models.ManyToManyField(Alert)
    message = models.TextField(verbose_name="ai分析内容", null=True, blank=True)
    types = [
        ("未处理", "未处理"),
        ("已处理", "已处理"),
    ]
    types = models.CharField(
        choices=types, max_length=255, verbose_name="任务类型", default=0
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "报警组"
        verbose_name_plural = verbose_name
