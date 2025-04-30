from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.http.response import HttpResponse
from utils.helm_enc import *
from rest_framework import status
from rest_framework.generics import GenericAPIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth.models import User

class HelmImportSerializer(serializers.Serializer):
    git = serializers.CharField()

    class Meta:
        fields = "__all__"


# 变量仓库接口查询
# 获取主机  组  生成字典
# 任务计划模版 生成字典
# 获取集群配置 生成字典
# 获取项目配置 生成字典
# 渲染变量


class sharedVariableSerializer(serializers.Serializer):
    Id = serializers.IntegerField()

    class Meta:
        fields = "__all__"
def get_env_info():
        data = {}
        data["HostGroup"]={}
        for group in HostGroup.objects.all():
            data["HostGroup"][group.name] = list(group.Host.all().values().values())
        k8s_env={}
        for i in k8s_Env.objects.all().values():
            k8s_env[i["name"]]=i
      
        data["k8s_Env"] =k8s_env


        return data

class sharedVariable(GenericAPIView):
    serializer_class = sharedVariableSerializer

    def get(self, request, *args, **krgs):
        

        return Response(get_env_info(), status=status.HTTP_201_CREATED)


class helm_import(GenericAPIView):
    serializer_class = HelmImportSerializer

    def post(self, request, *args, **krgs):
        git = request.data.get("git")
        # 处理 POST 请求的逻辑
        data = {"message": "POST 请求成功"}
        h = Helm()
        data = h.up_helm_dir()

        for d in data:
            for k, v in d.items():
                try:
                    # 判断 HiAppstore 对象是否存在，如果存在则更新，如果不存在则创建
                    appstore, created = HiAppstore.objects.get_or_create(name=k)

                    if not created:
                        print("更新Chart", k)
                        # 如果对象已存在，则更新对应的属性值
                        appstore.chart = v["Chart.yaml"]
                        appstore.values = v["values.yaml"]
                        appstore.save()
                    else:
                        print("创建配置Chart", k)
                        appstore = HiAppstore.objects.create(
                            name=k, chart=v["Chart.yaml"], values=v["values.yaml"]
                        )

                except Exception as e:
                    print(k, e)

                for tk, tv in v["templates"].items():
                    try:
                        # 判断 HiAppstoreTemplates 对象是否存在，如果不存在则创建
                        template, created = HiAppstoreTemplates.objects.get_or_create(
                            name="%s-%s" % (k, tk)
                        )

                        if not created:
                            print("更新templates", "%s-%s" % (k, tk))
                            # 如果对象已存在，则更新对应的属性值
                            template.templates = tv
                            template.save()
                            appstore.templates.add(template)

                        else:
                            # 将创建的 HiAppstoreTemplates 对象关联到 HiAppstore 对象的多对多关系中

                            print("创建templates", "%s-%s" % (k, tk))
                            template = HiAppstoreTemplates.objects.create(
                                name="%s-%s" % (k, tk), templates=tv
                            )
                            appstore.templates.add(template)

                    except Exception as e:
                        print("error", tk, e)

        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        git = request.data.get("git")
        print("===", git, request.data, args, kwargs)
        data = {"message": "GET 请求成功"}
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        # 处理 PUT 请求的逻辑
        print(request.data, request)
        data = {"message": "PUT 请求成功"}
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="page", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING
            )
        ]
    )
    def delete(self, request, *args, **kwargs):
        # 处理 DELETE 请求的逻辑
        git = request.data.get("git")
        print("===", git, request.data)
        data = {"message": "DELETE 请求成功"}
        return Response(data, status=status.HTTP_204_NO_CONTENT)



class WebhookViewSet(ModelViewSet):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer

class  TaskEncViewSet(ModelViewSet):
    queryset = TaskEnc.objects.all()
    serializer_class = TaskEncSerializer
 




class Custom_EnvViewSet(ModelViewSet):
    queryset = Custom_Env.objects.all()
    serializer_class = Custom_EnvSerializer


class HostGroupViewSet(ModelViewSet):
    queryset = HostGroup.objects.all()
    serializer_class = HostGroupSerializer

class HostConfigViewSet(ModelViewSet):
    queryset = HostConfig.objects.all()
    serializer_class = HostConfigSerializer

    # 自定义方法
    @action(methods=["post"], detail=True, url_path="show_password")
    def show_password(self, request, *args, **kwargs):
        # 检查密码是否正确
        user = User.objects.get(username=request.user)
        password=request.data["password"]

        print("输入密码",password)
        # 检查密码是否正确
        password_correct = user.check_password(password)
        Id = kwargs["pk"]
       

        if password_correct:
            print("密码正确")
          
            h=HostConfig.objects.get(Id=Id)
            return Response({"msg":h.password,"status": True})

        else:
            print("密码错误")
            
            return Response({"msg":"密码错误","status": False})

 

class web_monitorViewSet(ModelViewSet):
    queryset = web_monitor.objects.all()
    serializer_class = web_monitorSerializer


class PipelineViewSet(ModelViewSet):
    queryset = Pipeline.objects.all()
    serializer_class = PipelineSerializer
    
    @action(methods=["put"], detail=True, url_path="upload_package")
    def upload_package(self, request, *args, **kwargs):
        Id = kwargs["pk"]
        file = request.data.get('file')  # 获取上传的文件
        
        # 处理文件保存逻辑，这里简单示例将文件保存在静态目录中
        
        filename=f'pipeline/uploads/{file.name}'
        with open(f'uploads/'+filename, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        h=Pipeline.objects.get(Id=Id)
        print("上传pipeline 文件 名字 %s  上传的文件 %s" % (h.name,filename))
        h.pacakge=filename
        h.save()

        return Response({"msg": "上传成功", "status": True})



class k8s_EnvViewSet(ModelViewSet):
    queryset = k8s_Env.objects.all()
    serializer_class = k8s_EnvSerializer
    # 过滤
    filter_fields = ("id", "htmlName")
    # 排序
    ordering_fields = "id"

    # 自定义方法
    # @action(methods=["post"], detail=False, url_path="exec_task")
    # def exec_task(self, request, *args, **kwargs):
    #     print(request.method, args, kwargs, request.data)
    #     dd = {"w": "ww", "ee": "ttt"}

    #     return Response(dd)
