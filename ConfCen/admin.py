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
from dws_cmdb.tasks import *
import requests

# Register your models here.

admin.site.site_title = "海豚运维管理系统"
admin.site.site_header = "海豚运维管理系统"


# @admin.register(k8s_Env)
# class k8s_EnvAdmin(admin.ModelAdmin):
#     exclude = []
#     form = k8s_EnvForm

#     list_display = (
#         "Id",
#         "name",
#         # "button_",
#     )
#     search_fields = (
#         "Id",
#         "name",
#     )

#     # def button_(self, obj):
#     #     if obj.Id:
#     #         return format_html(
#     #             '<td class="field-name"><a   class="el-button  " href="/ConfCen/init_kube/?Id={}">初始化</td>',
#     #             obj.Id,
#     #         )
#     #     else:
#     #         return "-"

#     # button_.short_description = format_html(
#     #     '<th scope="col" class="sortable field-button_"><div class="text"><a href="?o=3">操作</a></div><div class="clear"></div></th>'
#     # )
#     # button_.allow_tags = True


# class HiAppstoreForm(forms.ModelForm):
#     chart = forms.CharField(
#         widget=AceWidget(mode="yaml", theme="twilight", width="1000px", height="500px"),
#         initial=chart,
#     )
#     values = forms.CharField(
#         widget=AceWidget(mode="yaml", theme="twilight", width="1000px", height="500px"),
#         initial=values,
#     )
#     configmap = forms.CharField(
#         widget=AceWidget(mode="yaml", theme="twilight", width="1000px", height="500px"),
#         initial=configmap,
#     )

#     class Meta:
#         model = HiAppstoreTemplates
#         exclude = []


class HostConfigForm(forms.ModelForm):
    host_key = forms.CharField(
        widget=AceWidget(mode="sh", theme="twilight", width="1000px", height="500px"),
        initial=host_key,
    )

    class Meta:
        model = HostConfig
        exclude = []


class consuleMangerForm(forms.ModelForm):
    templates = forms.CharField(
        widget=AceWidget(mode="sh", theme="twilight", width="1000px", height="500px"),
        initial=consule_config,
    )

    class Meta:
        model = consuleManger
        exclude = []


@admin.register(HostConfig)
class HostConfigAdmin(admin.ModelAdmin):
    list_display = (
        # "Id",
        "Id_",
        "user",
        "name",
        "ip",
        "port",
        "pass_",
        "types",
        "button_",
    )  # list

    search_fields = ("Id", "user", "name", "ip", "port", "types")  # list

    exclude = []
    form = HostConfigForm

    def button_(self, obj):
        if obj.Id:
            print("===Password", obj.name)
            password = obj.password
            _password = urllib.parse.quote(password)
            private_key = re.sub(r"\s+", "", obj.host_key)

            return format_html(
                '<td class="field-name"><a     href="http://cmdb.keli.vip/DeployCen/exec_cmd/?Id={}&Cmd=/bin/bash&ws=103.63.139.134">登陆终端</td>',
                obj.Id,
            )
            return format_html(
                '<td class="field-name"><a     href="http://cmdb.keli.vip/DeployCen/exec_cmd/?Id=1202&Cmd=/bin/bash&LocalMode=no&ws=103.63.139.134&Password={}&Username={}&Host={}:{}">登陆终端</td>',
                _password,
                obj.user,
                obj.ip,
                obj.port,
            )

        else:
            return "-"

    button_.short_description = format_html(
        '<th scope="col" class="sortable field-button_"><div class="text"><a href="?o=3">操作</a></div><div class="clear"></div></th>'
    )
    button_.allow_tags = True

    def pass_(self, obj):
        if obj.Id:
            print("===Password", obj.name)
            return format_html(
                '<td class="field-name"><a  class="show_password" value="{}">查看密码</td>',
                obj.Id,
            )

    pass_.short_description = format_html(
        '<th scope="col" class="sortable field-button_"><div class="text"><a href="?o=3">密码</a></div><div class="clear"></div></th>'
    )
    pass_.allow_tags = True

    def Id_(self, obj):
        if obj.Id:
            print("===Password", obj.name)
            return format_html(
                '<td class="field-name"><a  value="{}" class="show_password" href="#true">{}</a></td>',
                obj.Id,
                obj.Id,
            )

    Id_.short_description = format_html(
        '<th scope="col" class="sortable field-button_"><div class="text"><a href="?o=3">Id</a></div><div class="clear"></div></th>'
    )
    Id_.allow_tags = True


config = """
name: config
    - 1
    - 2
    - 3

"""


class Custom_EnvForm(forms.ModelForm):
    config = forms.CharField(
        widget=AceWidget(mode="yaml", theme="twilight", width="1000px", height="500px"),
        initial=config,
    )

    class Meta:
        model = Custom_Env
        exclude = []


@admin.register(Custom_Env)
class Custom_EnvAdmin(admin.ModelAdmin):
    list_display = ("Id", "name", "config")  # list

    search_fields = ("Id", "name", "config")  # list

    exclude = []
    form = Custom_EnvForm


class TemplatesForm(forms.ModelForm):
    templates = forms.CharField(
        widget=AceWidget(mode="sh", theme="twilight", width="1000px", height="500px"),
        initial="",
    )

    class Meta:
        model = Templates
        exclude = []


@admin.register(Templates)
class TemplatesAdmin(admin.ModelAdmin):
    list_display = ("Id", "name")  # list

    search_fields = ("Id", "name")  # list

    exclude = []
    form = TemplatesForm


class k8s_EnvForm(forms.ModelForm):
    kube_config = forms.CharField(
        widget=AceWidget(mode="yaml", theme="twilight", width="1000px", height="500px"),
        initial="",
    )

    class Meta:
        model = k8s_Env
        exclude = []


@admin.register(k8s_Env)
class k8s_EnvAdmin(admin.ModelAdmin):
    list_display = ("Id", "name")

    search_fields = ("Id", "name")

    exclude = []
    form = k8s_EnvForm


class Task_typeForm(forms.ModelForm):
    templates = forms.CharField(
        widget=AceWidget(mode="sh", theme="twilight", width="1000px", height="500px"),
        required=False,
    )

    class Meta:
        model = Task_type
        exclude = []


def get_random_password(length):
    characters = string.ascii_letters + string.digits
    token = "".join(secrets.choice(characters) for _ in range(length))
    return token


class WebhookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["SECRET"].initial = get_random_password(32)

    exclude = []
    form = Webhook


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = (
        "Id",
        "name",
        "url",
        "SECRET",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "Id",
        "url",
        "SECRET",
        "created_at",
        "updated_at",
    )
    form = WebhookForm


@admin.register(Task_type)
class Task_typeAdmin(admin.ModelAdmin):
    list_display = ("Id", "name")

    search_fields = ("Id", "name")

    exclude = []
    form = Task_typeForm


Pipeline_default_temp = """
pipeline {
    agent any
    
    {{ jenkins_parameters }}
    {{ form_task_type }}
    stages {
        stage('上传文件处理') {
            steps {
              
               {{ jenkins_stashedFile }}
                sh '''

                    sh dotask_send_msg.sh  开始执行任务-{{ task_name }}-用户{{  user  }}
                    dos2unix  *_key *.sh 
                    chmod 600 *_key 
                    echo "hello wolrd"
                    
                '''
            }
        }
        
      
    }
}
"""


class PipelineForm(forms.ModelForm):
    templates = forms.CharField(
        widget=AceWidget(mode="sh", theme="twilight", width="1000px", height="500px"),
        initial=Pipeline_default_temp,
    )

    class Meta:
        model = Pipeline
        exclude = []


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ("Id", "name")

    search_fields = ("Id", "name")

    exclude = []
    form = PipelineForm


helloworld = """
- 打印1: 
  - hellowolrd1
  - hellowolrd2
- 打印2: hellowolrd
"""
# class TaskCreateForm(forms.ModelForm):

#     LocalVariable = forms.CharField(
#         widget=AceWidget(mode="yaml", theme="twilight", width="1000px", height="500px"),
#         initial=helloworld,

#     )

#     class Meta:
#         model = TaskCreate
#         exclude = []


@admin.register(TaskCreate)
class TaskCreateAdmin(admin.ModelAdmin):
    list_display = (
        "Id",
        "name",
        "templateGroup",
        "pipeline",
        "Custom_Env",
        "task_type",
        "HostGroup",
        "k8s_Env",
    )

    search_fields = ("Id", "name")

    exclude = []

    # form = TaskCreateForm


def consule_apply(name, templates):
    print("保存更新consule", name)

    # Consul 的地址和端口
    consul_address = "http://103.63.136.110:30491"
    # 要更新的 key
    key = name
    # 要更新的新值
    print(templates, "==")

    new_value = yaml.dump(templates)

    # 使用的 token
    token = "e180dbae-6d96-55a5-7238-50acab878bdb"

    # 更新 URL
    url = f"{consul_address}/v1/kv/{key}"

    # 设置 headers
    headers = {
        "X-Consul-Token": token,
        "Content-Type": "application/x-yaml",  # 指定 YAML 格式
    }

    # 执行 PUT 请求以更新 key-value
    response = requests.put(url, headers=headers, data=new_value)

    # 检查响应
    if response.status_code == 200:
        print("Key/Value 更新成功！")
    elif response.status_code == 403:
        print("权限错误：Token 无效或没有足够的权限。")
    else:
        print(f"更新失败，状态码：{response.status_code}，响应内容：{response.text}")


@admin.register(consuleManger)
class consuleMangerAdmin(admin.ModelAdmin):
    list_display = (
        "Id",
        "name",
        "describe",
        "button_",
    )

    search_fields = ("Id", "name")  # list

    def save_model(self, request, obj, form, change):

        ####consule 更新

        consule_apply(obj.name, yaml.safe_load(obj.templates))

        ####
        super().save_model(request, obj, form, change)

    exclude = []
    form = consuleMangerForm

    def button_(self, obj):
        if obj.Id:
            config = ""
            try:

                config = yaml.safe_load(obj.templates)
                temp = """

{% for c in content %}
<ul>
<li>服务{{ c.name }}  外网访问地址{{ wlan }}:{{ c.port }} 对应子服务器如下</li>
{% for s in c.server %}
<li>{{ s }}</li>
{% endfor%}
</ul>
{% endfor%}

"""
                tp = Template(temp)
                content = tp.render(content=config, wlan=obj.wlan)
                print(content)

                return format_html(
                    '<td class="field-name">{}</td>',
                    format_html(content),
                )
            except yaml.YAMLError as e:
                print("错误：解析 YAML 文件时出错。", e)
                return format_html(
                    '<td class="field-name">yaml异常{}</td>',
                    e,
                )

        else:
            return "-"

    button_.short_description = format_html(
        '<th scope="col" class="sortable field-button_"><div class="text"><a href="?o=3">配置信息</a></div><div class="clear"></div></th>'
    )
    button_.allow_tags = True


tm = """#!/bin/bash

cat >private_key<<EOF
{% for host in HostGroup[form_HostGroup] %}{{ host.host_key }}{% endfor %}
EOF


chmod 600 private_key

# cat >private_key<<EOF
# -----BEGIN RSA PRIVATE KEY-----
# MIIEpAIBAAKCAQEAw0TmAlWBJztnK2P4jWNvHuVZG3nAn4JjJ20vYOCb7cOYTK6i
# 0i8/bm9zqAoKi3mcUXItjZjh2mvibrDieFH17EkSOJA/2A6IoMPSj9jM7148ue1W
# jWBj26O31iTP7Eg94hn/A6kuxnyVfwgzvjPNZfrZNaHOBKr46VQ2yN9NI4YJozge
# dSr4PSBKosOuw9p57mGOSXQqY3eiVleN1DXSoGYDxI5fp40qC40TfzMsJUAZ/ZQI
# 8DwBjqWpZfMFvE/3VyJnGHX8cuuiZHN+9QHWuHzMC+3w0NFpE7l1sUedeYpUdMJ+
# ebKpu0XTR3KGrzP32FZxmbyN7Ga/vknBuJGX1wIDAQABAoIBAQCt67wB8C5sxxgJ
# Ka3EIQBkQFqxgivy5qtx/mnom6XGjCQmiJU1KCgTMOmOjgL+X36/fDbem4DujpDL
# jnjoOfgUULEN+E0lHyzKJCBzRuKhgQoNgDtLCMNoadXfwkH/bgjQTd85X4Lt/yEY
# WDHeAz26y0aT4l4hAjdZe0ygdWO7cqI/Vzav9iYYHR3pSExRDg7FLvJT/yhONWtp
# Xsv8Ev98ZNR80mWL5NBNIqbfBpoy1nDryoDTdsuKLxSTF77poDxXBqH242L/ZWzt
# 0AJnK1Ac2mNEl0t95ZowIU9uPRpQkUyDkmTuRTi67RoBi3NbhGZ6DLxnTleDyOMj
# rKbLcfLBAoGBAPss0cGolKBmkFvfLqwu4y59kFQUoMnC529bVu2OX7cpmME7dkws
# IZh+wZsCJiEwiEnl8qFZwquFrABkuAzOijJZmrgiuvp2VgBlRIWNV5vuT2wlvmY3
# Z6603yQatOG8ITsVpJF6tGYhhO+S3awLPDpsZrzblPrIeX9kalBKi8t/AoGBAMcF
# J9Th3OQC91Z3NY2wceat0rh7qAu2+aiS//iWZY42mCMKCZfQWfRyak1GB9zCghSs
# n2/pc9CDe05Mu4ih2gXL0ZGatpil+XvzO5qgJREFHA85lv12nwEzPnRBI1pD+2Hx
# E5vFSTXvKR+1DHk2jiRVaj+OwoRFus2sGJ8OzD+pAoGAIMW1TKZZViBrv4D8Tv0D
# KWK6vS2/2PN0TQRG8FH+TSDBTJ0cj03GyGXpjvcV0IjLj5DQOptCmiyjx51colck
# kvM8C8CEUv+zsvODoEVT5AWRGVRHZoDeJ150KvrNFRL95v6o7U5sUVMYTEYGZFdG
# 8XyJXyTraFlV+Pg6IuXHHbMCgYBLe1EYFHHKqLVWPfA5xOnuK474GS4rA0K9BMPA
# bIon3dzlrTDmO0dixuI6XI0u1Taw0KfHsisSsktZ7xBRSdF+0UayipMmYgy1ThMV
# Ghf01JNH0vfJOewkcGMHhIz79zyocN6W/cQ+iG54cBpC/sX6UcryQBrWP/wRdWwB
# J4OfwQKBgQC9fzDBlgwcT+142NJn4XePiEwl58zbm++RmZcwhsynHEcecAQdom8b
# uODBKBi9tqxG7AUd+tV0ynmdMksDaQ5sDlRcT78V6E7sfsJ5pL0BUf049mA/hoFO
# GcfHz6yO5E8X/yOc3YvLbz9S9LnXKURoz44eA6athX15z2OGihaGkQ==
# -----END RSA PRIVATE KEY-----
# EOF
# cat > hosts<<EOF
# [server]

# 103.63.139.42  ansible_port=2260 ansible_user=root




# [all:vars]
# ansible_ssh_private_key_file=/var/jenkins_home/workspace/1701069965-PWF_AK_UI_Test/private_key
# #True  安装测试环境
# #False 开始测试
# init_env=False

# ansible_ssh_extra_args='-o StrictHostKeyChecking=no '
# EOF

cat > palybook.yaml  <<EOF
- hosts: all
  remote_user: root
  tasks:
    - name: 更新
      shell: |
        #!/bin/bash
        ls -l
        source /etc/profile
        cd /hitosea/wwww/wallet-ui
        bash cmd build
    # - name: 拉取目录
    #   synchronize:
    #     src: /path/to/remote/directory
    #     dest: /path/to/local/directory
    #     mode: pull
    # - name: 上传目录
    #   synchronize:
    #     src: /path/to/local/directory
    #     dest: /path/to/remote/directory
    #     mode: push
EOF


ansible-playbook -i hosts palybook.yaml  

"""

_Pipeline_default_temp = """
pipeline {
    agent any
    
    {{ jenkins_parameters }}
    {{ form_task_type }}
    stages {
        stage('上传文件处理') {
            steps {
              
               {{ jenkins_stashedFile }}
                sh '''
                    sh dotask_send_msg.sh  开始执行任务-{{ task_name }}-用户{{  user  }}
                    #dos2unix  *_key *.sh 
                    #chmod 600 *_key 
                    ## 这个脚本名字请跟任务名一致
                    bash ./hellowolrd
                    sh dotask_send_msg.sh  
                '''
            }
        }
        
      
    }
}
"""


# 就是建组和关联
class AutoTaskCreateForm(forms.ModelForm):
    templates = forms.CharField(
        widget=AceWidget(mode="sh", theme="twilight", width="1000px", height="500px"),
        initial=_Pipeline_default_temp,
    )
    default_shell = forms.CharField(
        widget=AceWidget(mode="sh", theme="twilight", width="1000px", height="500px"),
        initial=tm,
    )

    class Meta:
        model = AutoTaskCreate
        exclude = []


d = """发布 : "fa-solid fa-play"
测试 : "fa-solid fa-flask-vial"
更新 : "el-icon-refresh"
关机 : "el-icon-switch-button"
#签名是按钮 后面是图标 这个网页是图标地址 https://fontawesome.com/icons/circle-left?f=classic&s=regular Element UI图标库也支持哦
"""
_d = """domain: "test.keli.vip"
#模版中{{ domain }} 进行使用
"""


class TaskEncForm(forms.ModelForm):
    TaskButton = forms.CharField(
        widget=AceWidget(mode="yaml", theme="twilight", width="1000px", height="500px"),
        initial=d,
    )
    Custom_Env = forms.CharField(
        widget=AceWidget(mode="yaml", theme="twilight", width="1000px", height="500px"),
        initial=_d,
    )

    class Meta:
        model = TaskEnc
        exclude = []


@admin.register(TaskEnc)
class TaskEncAdmin(admin.ModelAdmin):
    form = TaskEncForm

    list_display = ("Id", "name", "TaskButton")

    class Meta:
        model = TaskEnc
        exclude = []


def merge_dicts(dict1, dict2):
    merged_dict = dict1.copy()  # 创建一个副本，确保不改变原始字典

    for key, value in dict2.items():
        merged_dict[key] = value  # 使用dict2的值替换dict1中的对应键的值

    return merged_dict


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
    build_jenkins_.delay(taskDeploy_obj.Id, user)


@admin.register(web_monitor)
class web_monitorAdmin(admin.ModelAdmin):

    list_display = (
        "Id",
        "url",
        "monitor_host",
        "monitor_status",
        "certificate_effective",
        "web_code",
        "describe",
        "web_type_status",
        "updated_at",
    )

    search_fields = (
        "Id",
        "url",
        "monitor_host",
        "monitor_status",
        "certificate_effective",
        "web_code",
        "describe",
    )

    exclude = ["certificate_effective", "web_code"]

    def save_model(self, request, obj, form, change):

        # 将对象序列化为字典
        obj_dict = model_to_dict(obj)
        # obj_dict["monitor_host"] = model_to_dict(obj.monitor_host)
        # print(obj_dicts)
        load_task("监控配置", obj_dict, str(request.user))
        super().save_model(request, obj, form, change)


##新增一键
@admin.register(AutoTaskCreate)
class AutoTaskCreateAdmin(admin.ModelAdmin):
    form = AutoTaskCreateForm

    def changelist_view(self, request, extra_context=None):
        return redirect("/admin/ConfCen/autotaskcreate/add")

    def save_model(self, request, obj, form, change):
        task_name = request.POST.get("name")
        self.some_value = "some value"
        templates = request.POST.get("templates")
        default_shell = request.POST.get("default_shell")

        print("======", default_shell)

        ts = Templates(name=task_name, templates=default_shell)
        ts.save()
        msg = Templates.objects.get(name="dotask_send_msg.sh")

        tg = TemplatesGroup.objects.create(name=task_name)

        tg.group.add(ts)
        tg.group.add(msg)

        tg.save()

        p = Pipeline(name=task_name, templates=templates)
        p.save()

        h = HostGroup(name=task_name)
        h.save()
        Cu = request.POST.get("Custom_Task_type")
        print("Cu", Cu)
        if Cu == "是":
            c = Custom_Env(name=task_name, config="name: %s" % task_name)
            c.save()
            print("自定义模版", c)
            t = TaskCreate(
                name=task_name,
                Custom_Env=c,
                pipeline=p,
                templateGroup=tg,
                HostGroup=h,
            )
            t.save()

            self.task_id = t
        else:
            print("无自定义模版")
            print(p)

            t = TaskCreate(name=task_name, pipeline=p, HostGroup=h, templateGroup=tg)
            t.save()

            self.task_id = t

        return

    def response_add(self, request, obj, post_url_continue=None):
        name = request.GET.get("name")
        print("====", self.task_id)
        t = TaskCreate.objects.get(name=self.task_id)

        return redirect("/admin/ConfCen/taskcreate/%s/change/" % (t.Id))


admin.site.register([TemplatesGroup, HostGroup])
