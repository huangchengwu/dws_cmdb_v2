from django.contrib import admin
from .models import *
from django.shortcuts import render, HttpResponse, redirect
from jinja2 import Template
from django.utils.html import format_html
from django import forms
from django_ace import AceWidget
import string
import secrets
import urllib.parse
import time
from django.http import HttpResponseRedirect
import base64
import re
from django.forms.models import model_to_dict
import json
from django.core.serializers.json import DjangoJSONEncoder
from dws_cmdb.tasks import *


@admin.register(k8s_cluster)
class k8s_clusterAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        # 将对象序列化为字典
        obj_dict = model_to_dict(obj)
        name = (f"{obj._meta.verbose_name_plural}",)
        name = name[0]
        print(obj.select_node_host)
        # obj_dict["select_node_host"] = model_to_dict(obj.select_node_host)
        # load_task(name, obj_dict, str(request.user))
        super().save_model(request, obj, form, change)


class nodeForm(forms.ModelForm):

    class Meta:
        model = node
        exclude = []


# Register your models here.
@admin.register(node)
class nodeAdmin(admin.ModelAdmin):
    pass
    # list_display = ("Id", "name", "types", "node_host")  # list
    # search_fields = ("Id", "name", "types", "node_host")  # list
    # exclude = []

    # def changelist_view(self, request, extra_context=None):
    #     context = {}
    #     form = nodeForm
    #     context["form"] = form

    #     return render(request, "custom/nodedeploy.html", context=context)


def load_task(name, obj_dict, user):
    obj_yaml = yaml.dump(obj_dict)
    version = int(time.time())
   
    tc = TaskCreate.objects.get(name=name)
   
    c = Custom_Env(name="%s-%s" % (version, name), config=obj_yaml)
    c.save()
    TaskDeploy(
        taskdeploy_env=tc,
        task_type=tc.task_type,
        User=user,
        version=version,
        select_Custom_Env=c,
    ).save()
    taskDeploy_obj = TaskDeploy.objects.get(version=version)
    build_.delay(taskDeploy_obj.Id, user)


@admin.register(k8s_network)
class k8s_networkAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):

        # 将对象序列化为字典
        obj_dict = model_to_dict(obj)
        obj_dict["k8s_network_host"] = model_to_dict(obj.k8s_network_host)
        name = (f"{obj._meta.verbose_name_plural}",)

        load_task(name[0], obj_dict, str(request.user))
        super().save_model(request, obj, form, change)


@admin.register(k8s_cluster_list)
class k8s_cluster_listAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        context = {}

        if request.method == "POST":
            if request.user.has_perm("DeployCen.add_taskdeploy") != True:
                return HttpResponse("没权限执行任务")

            return render(request, "custom/k8s_cluster_list.html", context=context)

        return render(request, "custom/k8s_cluster_list.html", context=context)
