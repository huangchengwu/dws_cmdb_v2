from django.contrib import admin
from .models import *
from django import forms
from django_ace import AceWidget
from django.utils.html import format_html
from ConfCen.models import *
import yaml
from DeployCen.models import *
import time
from dws_cmdb.tasks import *
from ConfCen.views import get_env_info
from jinja2 import Template
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from django.conf import settings  # noqa
import re


# 就是建组和关联
class ProjdepForm(forms.ModelForm):
    ConfigContent = forms.CharField(
        widget=AceWidget(mode="yaml", theme="twilight", width="1000px", height="500px"),
        initial="",
    )
    Describe = forms.CharField(
        widget=AceWidget(
            mode="django", theme="twilight", width="1000px", height="500px"
        ),
        initial="",
                required=False  # 设置为可选

    )

    class Meta:
        model = Projdep
        
        exclude = []

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # 获取传递的用户对象
        super().__init__(*args, **kwargs)
        print(user)
        # 检查用户是否为超级用户
        if user.is_superuser:
            # 超级用户：可能不禁用任何字段，或者提供高级选项
            pass
        elif user.is_staff:
            # 管理员但不是超级用户：可能禁用某些字段
            try:
                self.fields["Group"].disabled = True
            except KeyError as err:
                print(err)

        else:
            # 普通用户：可能禁用更多字段
            self.fields["Group"].disabled = True
            self.fields["some_other_field"].disabled = True

    # if self.instance and self.instance.pk:
    #     # 检查用户权限
    #     print("yonghu",self.instance.Group)
    #     if user and not user.has_perm('ProjManage.change_projdep'):
    #         # 如果用户没有修改权限，则禁用 Group 字段
    #         self.fields['Group'].disabled = True

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     # 检查实例是否存在（即表单是在编辑模式下）
    #     if self.instance and self.instance.pk:
    #         # 禁用 Group 字段
    #         self.fields['Group'].disabled = True
    #         # 可选：也可以使用只读属性
    #         # self.fields['Group'].widget.attrs['readonly


# Register your models here.
@admin.register(Projdep)
class ProjdepAdmin(admin.ModelAdmin):
    form = ProjdepForm
    list_display = [
        "Id",
        "name",
        "cid",
        "Group",
        "show_log",
        "show_workspace",
        "Describe_",
        "button_",
    ]
    search_fields = (
        "Id",
        "name",
        "cid",
        "Group",
    )
    exclude = ["cid","task_name","action", "log_id"]

    def get_form(self, request, obj=None, **kwargs):
        # 获取默认的表单类
        form = super().get_form(request, obj, **kwargs)

        # 定义一个新的表单类，覆盖初始化以传递用户
        class CustomProjdepForm(form):
            def __init__(self, *args, **kwargs):

                kwargs["user"] = request.user  # 将当前用户传递给表单

                super().__init__(*args, **kwargs)

        return CustomProjdepForm

    def changelist_view(self, request, extra_context=None):
        context = {}
        froms = ProjdepForm
        if request.user.has_perm("ProjManage.TBD_查看空间") == True:
            context["workspace"] = {"status": "0"}
        else:
            context["workspace"] =  {"status": "1"} 
        if request.user.is_superuser:
            button = {}
            describe={}
            print("返回所有数据")
            tasklist = Projdep.objects.all()
            for t in tasklist:
                TaskButton = yaml.safe_load(t.TaskEnc_select_Custom_Env.TaskButton)
                button[t.Id] = TaskButton
              
                try:
                    c = yaml.safe_load(t.ConfigContent)
                    tp = Template(t.Describe)
                    html = tp.render(c)
                    describe["describe_%s"%(t.Id)] = html
                except :
                    describe["describe_%s"%(t.Id)] ="你的yaml异常啦请检查!!!"

            context["button"] = json.dumps(button, indent=4)
            context["describe"] = json.dumps(describe, indent=4)
            
            context["tasklist_json"] = json.dumps(
                json.loads(serialize("json", tasklist)), indent=4
            )
            
        else:
            button = {}
            describe={}
            user = request.user
            # 获取用户所有权限
            user_permissions = user.user_permissions.all()
            matched_choices = []
            tasklist = Projdep.objects.none()
            # 遍历每一个权限对象
            for permission in user_permissions:
                pattern = r"^TBD_"
                if re.match(pattern, permission.codename):
                    matched_choices.append(permission.codename)
                    queryset = Projdep.objects.filter(Group=permission.codename)
                    print("mam", queryset)
                    tasklist |= queryset
            for t in tasklist:
                TaskButton = yaml.safe_load(t.TaskEnc_select_Custom_Env.TaskButton)
                button[t.Id] = TaskButton

                try:
                    c = yaml.safe_load(t.ConfigContent)
                    tp = Template(t.Describe)
                    html = tp.render(c)
                    describe["describe_%s"%(t.Id)] = html
                except :
                    describe["describe_%s"%(t.Id)] ="你的yaml异常啦请检查!!!"


            context["button"] = json.dumps(button, indent=4)
            context["describe"] = json.dumps(describe, indent=4)

            context["tasklist_json"] = json.dumps(
                json.loads(serialize("json", tasklist)), indent=4
            )
            print(context["tasklist_json"])

        context["froms"] = froms
        context["permissions"] = Projdep._meta.permissions
        if request.method == "POST":
            if request.user.has_perm("DeployCen.add_taskdeploy") != True:
                return HttpResponse("没权限执行任务")
            ace_editor_content = request.POST.get("ace-editor-content")

            t = ProjdepForm(request.POST)
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

            return render(request, "custom/projdep.html", context=context)

        return render(request, "custom/projdep.html", context=context)

    def get_queryset(self, request):
        # 将 request 传递给 queryset，以便在后续方法中使用
        self.request = request

        qs = super().get_queryset(request)

        if request.user.is_superuser:

            return qs  # 返回所有数据
        else:

            user = request.user
            # 获取用户所有权限
            user_permissions = user.user_permissions.all()
            matched_choices = []
            combined_queryset = Projdep.objects.none()

            # 遍历每一个权限对象
            for permission in user_permissions:

                pattern = r"^TBD_"

                if re.match(pattern, permission.codename):
                    matched_choices.append(permission.codename)
                    queryset = Projdep.objects.filter(Group=permission.codename)
                    combined_queryset |= queryset

            return combined_queryset

    # def save_model(self, request, obj, form, change):
    #     version = int(time.time())
    #     obj.cid = version

    #     #
    #     matching_custom_env = Custom_Env.objects.filter(name=obj.name + "项目部署配置")

    #     # 判断是否存在满足条件的数据
    #     if matching_custom_env.exists():

    #         matching_custom_env.update(config=obj.ConfigContent)

    #     else:
    #         Custom_Env(name=obj.name + "项目部署配置", config=obj.ConfigContent).save()
    #     ct = Custom_Env.objects.filter(name=obj.name + "项目部署配置")

    #     Id = obj.TaskEnc_select_Custom_Env.TaskEnctaskcreate.Id

    #     tc = TaskCreate.objects.filter(Id=Id)

    #     t = Task_type.objects.filter(Id=tc[0].task_type.Id)

    #     TaskDeploy(
    #         taskdeploy_env=tc[0], task_type=t[0], User=request.user, version=version
    #     ).save()
    #     taskDeploy_obj = TaskDeploy.objects.get(version=version)
    #     taskDeploy_obj.select_Custom_Env = ct[0]
    #     taskDeploy_obj.save()

    #     obj.log_id = taskDeploy_obj.Id
    #     super().save_model(request, obj, form, change)  # 默认保存模型

    #     build_jenkins_.delay(taskDeploy_obj.Id, str(request.user))

    def show_log(self, obj):
        try:

            html = (
                '<td class="field-name"><a href="/DeployCen/show_task/?Id='
                + obj.log_id
                + '">查看日志</a></td>'
            )
            return format_html(html)

        except:

            return format_html(
                '<td class="field-name"><a href="/DeployCen/show_task/?Id="">查看日志</a></td>'
            )

    def Describe_(self, obj):
        if obj.Id:

            try:
                env_info = get_env_info()
                c = yaml.safe_load(obj.ConfigContent)
                env_info = merge_dicts(env_info, c)

                tp = Template(obj.Describe)
                html = tp.render(env_info)
                return format_html('<td class="field-name">' + html + "</td>")

            except:
                html = "未正确配置Describe"
                return format_html('<td class="field-name">' + html + "</td>")

        else:
            return "-"

    # 查看空间
    def show_workspace(self, obj):
        if obj.Id:
            print("查看空间域名",settings.Domain)
            
            html = (
                """<a  style="color: #409eff;" onclick="window.open('http://cmdb.keli.vip:9999/?password=8a0501a0b53ca58f60a7b0fd&folder=/var/lib/jenkins/workspace/%s-%s/')">查看空间 </a>"""
                % (obj.cid, obj.TaskEnc_select_Custom_Env.TaskEnctaskcreate)
            )
            if hasattr(self, "request"):
                user = self.request.user

                if user.has_perm("ProjManage.TBD_查看空间") == False:
                    html = "无权限查看"

            return format_html('<td class="field-name"> ' + html + "</td>")
        else:
            return "-"

    def button_(self, obj):
        if obj.Id:

            TaskButton = yaml.safe_load(obj.TaskEnc_select_Custom_Env.TaskButton)

            b = ""
            for key, value in TaskButton.items():
                b += (
                    '<li  style="list-style-type: none;"><button type="button" name="TaskEnc_exec" class="el-button"  value="%s"  ><span>%s</span></a></li><br>'
                    % (
                        obj.Id,
                        key,
                    )
                )

            return format_html('<td class="field-name"><ul>' + b + "</ul></td>")
        else:
            return "-"

    button_.short_description = format_html(
        '<th scope="col" class="sortable field-button_"><div class="text"><a href="?o=3">操作</a></div><div class="clear"></div></th>'
    )
    button_.allow_tags = True
    Describe_.short_description = format_html(
        '<th scope="col" class="sortable field-button_"><div class="text"><a href="?o=3">描述信息</a></div><div class="clear"></div></th>'
    )
    Describe_.allow_tags = True
    show_log.short_description = format_html(
        '<th scope="col" class="sortable field-button_"><div class="text"><a href="?o=3">日志收集</a></div><div class="clear"></div></th>'
    )
    show_log.allow_tags = True

    show_workspace.short_description = format_html(
        '<th scope="col" class="sortable field-button_"><div class="text"><a href="?o=3">查看空间</a></div><div class="clear"></div></th>'
    )
    show_workspace.allow_tags = True
