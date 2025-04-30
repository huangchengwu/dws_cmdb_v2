from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from .models import *
from ConfCen.models import *
from utils.helm_enc import *
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework.decorators import action
from jinja2 import Template
import requests
from django.http import FileResponse
from django.http import HttpResponseForbidden, FileResponse
import os
from rest_framework.authtoken.models import Token
from dws_cmdb.tasks import *
from django.shortcuts import redirect
from urllib.parse import quote
from django.conf import settings  # noqa
from dws_cmdb.tasks import Task_disable
from ConfCen.views import *
import markdown
import io
import zipfile
from django.urls import reverse
from .admin import TaskDeployForm
from django.contrib.auth.decorators import login_required


def get_directory_contents(directory):
    contents = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            contents.append({"name": item, "type": "file"})
        elif os.path.isdir(item_path):
            contents.append({"name": item, "type": "folder"})
    return contents


def show_work_dir(request):
    context = {}

    Id = request.GET.get("Id")
    t = TaskDeploy.objects.get(Id=Id)

    current_path = os.getcwd() + "/static/assets/jenkins/%s-%s" % (
        t.version,
        t.taskdeploy_env,
    )

    files = os.listdir(current_path)
    f = {}

    for _f in files:
        pa = "%s-%s/" % (t.version, t.taskdeploy_env)

        f[_f] = pa

    files = f
    return render(request, "custom/file_browser.html", {"files": files})


def file_detail(request, path):
    file_path = os.path.join(os.getcwd() + "/static/assets/jenkins", path)
    print("路径", file_path)
    if os.path.isfile(file_path):
        if os.path.isfile(file_path):
            _, file_extension = os.path.splitext(file_path)

            if file_extension == ".html":
                with open(file_path, "r") as f:
                    file_content = f.read()

                return HttpResponse(file_content, content_type="text/html")
            if file_extension == ".md":  # 如果是 Markdown 文件
                with open(file_path, "r") as f:
                    markdown_content = f.read()
                # html_content = markdown.markdown(markdown_content)
                return HttpResponse(markdown_content, content_type="text/markdown")
            if file_extension == ".zip":
                # 下载压缩包
                file_name = os.path.basename(file_path)

                response = FileResponse(open(file_path, "rb"))
                quoted_file_name = quote(file_name)

                response["Content-Disposition"] = 'attachment; filename="{}"'.format(
                    quoted_file_name
                )
                print(response)
                return response
            if file_extension == ".gz":
                # 下载压缩包
                file_name = os.path.basename(file_path)

                response = FileResponse(open(file_path, "rb"))
                quoted_file_name = quote(file_name)

                response["Content-Disposition"] = 'attachment; filename="{}"'.format(
                    quoted_file_name
                )
                print(response)
                return response
            with open(file_path, "r") as f:
                file_content = f.read()
            return render(
                request, "custom/file_detail.html", {"file_content": file_content}
            )

    elif os.path.isdir(file_path):
        file_list = os.listdir(file_path)
        print(file_list)
        return render(request, "custom/file_detail.html", {"file_list": file_list})
    else:
        return render(
            request,
            "custom/file_detail.html",
            {"file_content": "空目录"},
        )

@login_required
def show_task(request):
    context = {}
    context["CMDB_DOMAIN"] = getattr(settings, "CMDB_DOMAIN", "http://127.0.0.1")

    Id = request.GET.get("Id")
    context["Id"] = Id
    t = TaskDeploy.objects.get(Id=Id)

    context["TaskDeploy"] = t

    print("show_task", context)
    return render(request, "custom/show_task.html", context)


@login_required
def show_log(request):
    context = {}
    context["CMDB_DOMAIN"] = getattr(settings, "CMDB_DOMAIN", "http://127.0.0.1")
    print("==www",context)
    get_params = request.GET
    for key, value in get_params.items():
        context[key]=value

    return render(request, "custom/show_log.html", context)


@login_required
def exec_cmd(request):
    context = {}


    return render(request, "custom/exec_cmd.html", context)



class taskExecSerializer(serializers.Serializer):
    Id = serializers.IntegerField()

    class Meta:
        fields = "__all__"


from django.http import FileResponse, HttpResponseNotFound


class taskExec(GenericAPIView):
    serializer_class = taskExecSerializer

    def post(self, request, *args, **krgs):
        data = {"message": "POST 请求成功"}
        return Response(data, status=status.HTTP_201_CREATED)


def download_local_file(request):
    file = open("templates/task_package/硬盘读写测试模版.zip", "rb")
    response = FileResponse(file)
    response["Content-Disposition"] = 'attachment; filename="硬盘读写测试模版"'
    return response

class Download(GenericAPIView):
    serializer_class = DownloadSerializer

    def post(self, request, *args, **krgs):
        path = request.data.get("path")
        name = request.data.get("name")

        try:
            print("下载",path+"/"+name)
            file = open(path+"/"+name, "rb")
        except:
         
            return Response({"error": "下载文件不存在" })


        response = FileResponse(file)
        response["Content-Disposition"] = 'attachment; filename="%s"' %(name)
        return response



class TaskCreateViewSet(ModelViewSet):
    queryset = TaskCreate.objects.all()
    serializer_class = TaskCreateSerializer


class TaskDeployViewSet(ModelViewSet):
    queryset = TaskDeploy.objects.all()
    serializer_class = TaskDeploySerializer
    # 过滤
    # filter_fields = ("id", "htmlName")
    # # 排序
    # ordering_fields = "id"

    # 自定义方法 渲染模版打包 去调用jenkins 并且传输模版过去

    # @action(methods=["post"], detail=True, url_path="task_exec/(?P<id>[0-9]+)")
    @action(methods=["delete"], detail=True, url_path="task_disable")
    def task_disable(self, request, *args, **kwargs):
        Id = kwargs["pk"]
        Task_disable.delay(Id)

        return Response({"msg": "删除成功,请刷新", "status": True})


    @action(methods=["put"], detail=True, url_path="task_rollback")
    def task_rollback(self, request, *args, **kwargs):
        Id = kwargs["pk"]
        Task_rollback.delay(Id)

        return Response({"msg": "回滚成功,请刷新", "status": True})

    @action(methods=["get"], detail=True, url_path="task_log")
    def task_log(self, request, *args, **kwargs):
        Id = kwargs["pk"]

        print("查看日志", Id)
        task_deploy_obj = TaskDeploy.objects.get(Id=Id)
        task_create_obj = TaskCreate.objects.get(Id=task_deploy_obj.taskdeploy_env.Id)
        job_name = "%s-%s" % (task_deploy_obj.version, task_deploy_obj.taskdeploy_env)
        print("====", job_name, task_deploy_obj.log_id)
        server = Jenkins_server(
            settings.JENKINS_URL,
            username=settings.JENKINS_USER,
            password=settings.JENKINS_PASSWORD,
            timeout=None,
        )
        if server.job_exists(job_name) == None:
            return Response(
                {"log_id": 0, "status": "NotFound", "get_build_info": "任务不存在"}
            )

        lastBuild = server.get_job_info(job_name)["lastBuild"]

        # 获取最新构建的ID
        latest_build_id = lastBuild["number"]

        get_build_info = server.get_build_info(job_name, latest_build_id)
        get_build_console_output = server.get_build_console_output(
            job_name, latest_build_id
        )
        print("Latest build ID:", latest_build_id, latest_build_id)
        if task_deploy_obj.task_type.types == "周期性":
            get_build_info["result"] = None

        dd = {
            "log_id": str(latest_build_id),
            "status": get_build_info["result"],
            "get_build_info": get_build_console_output,
        }

        return Response(dd)

    # @action(methods=["put"], detail=True, url_path="task_update")
    # def task_update(self, request, *args, **kwargs):
    #     Id = kwargs["pk"]
    #     task_deploy_obj = TaskDeploy.objects.get(Id=Id)
    #     task_create_obj = TaskCreate.objects.get(Id=task_deploy_obj.taskdeploy_env.Id)

    #     server = Jenkins_server(
    #         "http://103.63.139.18:30025",
    #         username="admin",
    #         password="admin",
    #         timeout=None,
    #     )
    #     version = int(task_deploy_obj.created_at.timestamp())
    #     j_xml = Template(jenkins_xml)
    #     _j_xml = j_xml.render({"pipeline": task_create_obj.pipeline.templates})

    #     server.reconfig_job(job_name, config_xml=_j_xml)
    #     print("id", server.build_job(job_name))

    #     print("更新jenkins", job_name)

    #     time.sleep(1)

    #     dd = {"msg": "更新配置"}
    #     return Response(dd)
    @action(methods=["put"], detail=True, url_path="task_update")
    def task_update(self, request, *args, **kwargs):
        Id = kwargs["pk"]
        td=TaskDeploy.objects.filter(Id=Id)

        print("tc==",td,Id)
        d = {}

        if len(td) == 0:
            print("更新任务不存在")
            d["error"] = True
            d["msg"] = "更新任务不存在"

            return Response(d)
        version = int(time.time())

       
        build_jenkins_.delay(Id, str(request.user))

        d["error"] = False
        d["msg"] = "执行成功"
        d["version"] = version
        d["task_id"] = Id

        return Response(d)
    

    @action(methods=["put"], detail=True, url_path="task_exec")
    def task_exec(self, request, *args, **kwargs):
        Id = kwargs["pk"]
        tc = TaskCreate.objects.filter(Id=Id)
        print("tc==",tc,Id)
        d = {}
        try:
            task_type_id = request.data["task_type"]
            t = Task_type.objects.filter(Id=task_type_id)

        except KeyError as err:
            d["error"] = True
            d["msg"] = "task_type 传入必选值"
            return Response(d)
        try:
            select_HostGroup = request.data["select_HostGroup"]

            h = HostGroup.objects.filter(Id=select_HostGroup)

            if len(h) == 0:
                print("选择HostGroup  不存在走默认")
            else:
                print("选择HostGroup  存在更新")
                _tc = TaskCreate.objects.get(Id=Id)
                _tc.HostGroup = h[0]
                _tc.save()

        except KeyError as err:
            print("忽略", err)
        try:
            select_k8s_Env = request.data["select_k8s_Env"]

            k = k8s_Env.objects.filter(Id=select_k8s_Env)

            if len(k) == 0:
                print("选择k8s_Env  不存在走默认")
            else:
                print("选择k8s_Env  存在更新", tc[0].k8s_Env, k[0])
                _tc = TaskCreate.objects.get(Id=Id)
                _tc.k8s_Env = k[0]
                _tc.save()

        except KeyError as err:
            print("忽略", err)

        if len(t) == 0:
            print("任务计划不存在")
            d["error"] = True
            d["msg"] = "任务计划不存在"
            return Response(d)
        if len(tc) == 0:
            print("任务不存在")
            d["error"] = True
            d["msg"] = "任务不存在"

            return Response(d)
        version = int(time.time())
        TaskDeploy(
            taskdeploy_env=tc[0], task_type=t[0], User=request.user, version=version
        ).save()
        taskDeploy_obj = TaskDeploy.objects.get(version=version)

        build_jenkins_.delay(taskDeploy_obj.Id, str(request.user))

        d["error"] = False
        d["msg"] = "执行成功"
        d["version"] = version
        d["task_id"] = Id

        return Response(d)


class deployAppSerializer(serializers.Serializer):
    Id = serializers.IntegerField()

    class Meta:
        fields = "__all__"


# Create your views here.
class deployApp(GenericAPIView):
    serializer_class = deployAppSerializer

    def post(self, request, *args, **krgs):
        Id = request.data.get("Id")
        # 处理 POST 请求的逻辑
        data = {"message": "POST 请求成功"}
        a = k8sPm.objects.get(Id=Id).App
        App = HiAppstore.objects.get(name=a)
        h = Helm()
        h.newHelm(App)
        directory = "templates/helm_package/%s" % App
        output_file = "templates/helm_package/%s-0.1.0.tgz" % App
        h.build_helm(str(App), directory, output_file)

        h.push_helm(output_file)

        # acd = Aargo(user=user, password=password,
        #         server=argocd_url)
        # acd.create(values=u'name : khadgar\r\nport : 8060\r\ngit : http://git.doumob.club/service/khadgar.git\r\npath: khadgar*.jar\r\nlog : /data/logs/app\r\nconfig : dev\r\nversion: "20220301181504"\r\ndescribe : \u517b\u6210\u6e38\u620f')

        return Response(data, status=status.HTTP_201_CREATED)
