from django.contrib import admin
from .models import *
from django.shortcuts import render
from django.utils.html import format_html

# Register your models here.
## 去获取指标查询
## 使用kubeconfig去获取接口查询
@admin.register(WebManger)
class   WebMangerAdmin(admin.ModelAdmin):
 
    list_display = (
        "Id",
        "name",
        "username",
        # "password",
        "url_",
    )
    search_fields = (
        "Id",
        "name",
        "username",
        # "password",
    )

    def url_(self, obj):
        if obj.Id:
    
            try:
                html='<td class="field-name"><a href="'+obj.url+ '" target="_blank">链接</a></td>'
                return format_html(html)
            except:
                return format_html(
                    '<td class="field-name"><a href="">-</a></td>'
                )
        else:
            return "-"
    url_.short_description = format_html(
        '<th scope="col" class="sortable field-button_"><div class="text"><a href="?o=3">链接</a></div><div class="clear"></div></th>'
    )
    url_.allow_tags = True
 