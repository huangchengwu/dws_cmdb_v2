from django.contrib import admin
from .models import *
from django import forms
from django_ace import AceWidget
from django.utils.html import format_html
from django.shortcuts import render
from django.http import HttpResponse
from dws_cmdb.tasks import *
from django.contrib.auth.decorators import permission_required
from django.conf import settings  

# class k8sPmForm(forms.ModelForm):
#     values = forms.CharField(
#         widget=AceWidget(mode="yaml", theme="twilight", width="1000px", height="500px"),
#         initial=values,
#     )
#     configmap = forms.CharField(
#         widget=AceWidget(mode="yaml", theme="twilight", width="1000px", height="500px"),
#         initial=configmap,
#     )

#     class Meta:
#         model = k8sPm
#         exclude = ["task_log"]


# @admin.register(k8sPm)
# class k8sPmAdmin(admin.ModelAdmin):
#     exclude = []
#     form = k8sPmForm

#     list_display = (
#         "Id",
#         "name",
#         "namespace",
#         "git",
#         "branch",
#         "version",
#         "status",
#         "created_at",
#         "updated_at",
#         "button_",
#     )
#     search_fields = (
#         "Id",
#         "name",
#         "namespace",
#         "git",
#         "branch",
#         "version",
#         "status",
#     )

#     def button_(self, obj):
#         if obj.Id:
#             return format_html(
#                 '<td class="field-name"><button id="deploy" type="button"  value="{}"  class="el-button" ><!----><i class="el-icon-video-play"></i><span>发布</span></button><button id="uninstall" type="button" value="{}" class="el-button" ><!----><i class="el-icon-delete"></i><span>卸载</span></button></td>',
#                 obj.Id,
#                 obj.Id,
#             )
#         else:
#             return "-"

#     button_.short_description = format_html(
#         '<th scope="col" class="sortable field-button_"><a href="?o=3">操作</a></div><div class="clear"></th>'
#     )
#     button_.allow_tags = True


# @admin.register(projectDeploy)
# class projectDeployAdmin(admin.ModelAdmin):
#     list_display = (
#         "Id",
#         "deploy_env",
#         "status",
#         "version",
#         "content",
#         "created_at",
#         "updated_at",
#     )

#     search_fields = (
#         "Id",
#         "deploy_env",
#         "status",
#         "version",
#         "content",
#         "created_at",
#         "updated_at",
#     )


class TaskDeployForm(forms.ModelForm):
    # random_id = forms.CharField(max_length=128, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['random_id'].initial = get_random_password(10)

        # self.fields['job_id'].widget.attrs.update({'class': 'el-input__inner'})  # 设置label的class属性
        # self.fields['random_id'].widget.attrs.update({'class': 'el-input__inner'})  # 设置label的class属性
        # self.fields['file_type_temp'].widget.attrs.update({'class': 'el-input__inner'})  # 设置label的class属性
        self.fields["taskdeploy_env"].widget.attrs.update(
            {"class": "el-input__inner"}
        )  # 设置label的class属性

    class Meta:
        model = TaskDeploy
        exclude = []
        fields = [
            "taskdeploy_env",
            "task_type",
            "select_k8s_Env",
            "select_HostGroup",
            "select_Custom_Env",
        ]

# #监控中心
# @admin.register(monitor)
# class TaskDeployAdmin(admin.ModelAdmin):
   
#     class Meta:
#         verbose_name = "监控中心"
#         verbose_name_plural = verbose_name

# 执行任务


@admin.register(TaskDeploy)
class TaskDeployAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        context = {}

        context["CMDB_DOMAIN"] = getattr(settings, "CMDB_DOMAIN", "http://127.0.0.1")
        print(context)
        froms = TaskDeployForm

        
        log_status = request.GET.get('log')

        if log_status == None:
     
            tasklist = TaskDeploy.objects.order_by('-created_at')[:30]
        else:
            tasklist = TaskDeploy.objects.all()
        context["tasklist"] = tasklist

        context["froms"] = froms

        if request.method == "POST":
            if request.user.has_perm("DeployCen.add_taskdeploy") != True:
                return HttpResponse("没权限执行任务")
            ace_editor_content = request.POST.get("ace-editor-content")

            t = TaskDeployForm(request.POST)
            instance = t.save(commit=False)
            instance.User = request.user
            instance.version = int(time.time())
            tc = TaskCreate.objects.get(Id=instance.taskdeploy_env.Id)
            if instance.select_k8s_Env != None:
                print("修改select_k8s_Env", instance.select_k8s_Env)

                tc.k8s_Env = instance.select_k8s_Env
            else:
                tc.k8s_Env = None
            if instance.select_HostGroup != None:
                print("修改select_HostGroup", instance.select_HostGroup)

                tc.HostGroup = instance.select_HostGroup
            else:
                tc.HostGroup = None
            if instance.select_Custom_Env != None:
                print("修改select_Custom_Env", instance.select_Custom_Env)
                c = Custom_Env.objects.get(name=instance.select_Custom_Env)
                c.config = ace_editor_content
                c.save()
                tc.Custom_Env = instance.select_Custom_Env

            else:
                tc.Custom_Env = None
            if instance.task_type != None:
                print("修改task_type", instance.task_type)

                tc.task_type = instance.task_type
            else:
                tc.task_type = None
            tc.save()
            instance.save()
           
            build_jenkins_.delay(instance.Id, str(request.user))
            
            return render(request, "custom/taskdeploy.html", context=context)

        return render(request, "custom/taskdeploy.html", context=context)

    # list_display = (
    #     "Id",
    #     "taskdeploy_env",
    #     "status",
    #     "created_at",
    #     "updated_at",
    #     "log_",
    #     "button_",
    # )
    # search_fields = (
    #     "Id",
    #     "taskdeploy_env",
    #     "status",
    # )

    # def log_(self, obj):
    #     return format_html(
    #         '<td class="field-name"><a href="/DeployCen/show_task/?Id={}">2023年9月28日 14:39</a></td>',
    #         obj.Id,
    #     )

    # def button_(self, obj):
    #     if obj.Id:
    #         return format_html(
    #             """<td class="field-name">
    #             <button id="deploy_app" type="button"  value="{}"  class="el-button" ><!----><i class="el-icon-video-play"></i><span>任务执行</span></button>
    #             <button id="deploy_app" type="button"  value="{}"  class="el-button" ><!----><i class="el-icon-video-play"></i><span>更新配置</span></button></td>""",
    #             obj.Id,
    #             obj.Id,
    #             obj.Id,
    #         )
    #     else:
    #         return "-"

    # log_.short_description = format_html(
    #     '<th scope="col" class="sortable field-button_"><a href="?o=3">日志查看</a></div><div class="clear"></th>'
    # )
    # log_.allow_tags = True
    # button_.short_description = format_html(
    #     '<th scope="col" class="sortable field-button_"><a href="?o=3">操作</a></div><div class="clear"></th>'
    # )
    # button_.allow_tags = True
    # form = TaskDeployForm
