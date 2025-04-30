import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import hmac
import hashlib

import json

from django.http import HttpResponse

from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status

from ConfCen.models import *
from utils.helm_enc import *
from rest_framework.viewsets import ModelViewSet

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
import requests
from ConfCen.views import *
from ConfCen.models import Webhook as webhook_m
import markdown
import io
import zipfile
from django.urls import reverse
from django.conf import settings  # noqa

# SECRET = "q5smMgRhHnQ/SZbwm5qxPsdljoMmC75cwKI/kTaSrfE="
##
# http://127.0.0.1:9091/Webhook/?task_id=16&task_type=1&select_k8s_Env=2

#   "taskdeploy_env": 0,
#   "task_type": 0,
#   "select_HostGroup": 0,
#   "select_k8s_Env": 0
# task_id
 
@csrf_exempt
def Webhook(request):
    status = False
    taskdeploy_env = request.GET.get("taskdeploy_env")
    task_type = request.GET.get("task_type")
    select_HostGroup = request.GET.get("select_HostGroup")
    select_k8s_Env = request.GET.get("select_k8s_Env")
    select_Custom_Env = request.GET.get("select_Custom_Env")
    print("====taskdeploy_env", taskdeploy_env)
    print("====task_type", task_type)
    print("====select_HostGroup", select_HostGroup)
    print("====select_k8s_Env", select_k8s_Env)
    print("====select_Custom_Env", select_Custom_Env)

    # 读取请求头中的签名
    signature = request.headers.get("X-Hub-Signature")

    url = request.build_absolute_uri()

    # 读取请求体中的原始数据
    body = request.body
    try:
        SECRET_list = webhook_m.objects.filter(url=url)

        print("SECRET_list", SECRET_list)
        for secret in SECRET_list:
            s = secret.SECRET
         

            expected_signature = (
                "sha1=" + hmac.new(s.encode(), body, hashlib.sha1).hexdigest()
            )

            if signature == expected_signature:
                print("expected_signature yes ", expected_signature)

                status = True
                break
            print("expected_signature no ", expected_signature)
        time.sleep(1)
        if True:

        # if status:
            print("签名一致")

            tc = TaskCreate.objects.filter(Id=taskdeploy_env)
            d = {}

            try:
                t = Task_type.objects.filter(Id=task_type)

            except KeyError as err:
                d["error"] = True
                d["msg"] = "task_type 传入必选值"
                return Response(d)

            if len(t) == 0:
                print("任务计划不存在")
                d["error"] = True
                d["msg"] = "任务计划不存在"
                return Response(d)
            if len(tc) == 0:
                print("任务不存在")
                d["error"] = True
                d["msg"] = "任务不存在"

            version = int(time.time())
            version = "%s-%s" % (version, tc[0])
            print(version)

            TaskDeploy(
                taskdeploy_env=tc[0], task_type=t[0], User="Webhook", version=version
            ).save()

            try:
                h = HostGroup.objects.filter(Id=select_HostGroup)

                if len(h) == 0:
                    print("选择HostGroup  不存在走默认")
                else:
                    _tc = TaskCreate.objects.get(Id=taskdeploy_env)
                    print("选择HostGroup  存在更新", _tc)
                    ts = TaskDeploy.objects.get(version=version)
                    ts.select_HostGroup = h[0]
                    ts.save()

                    _tc.HostGroup = h[0]
                    _tc.save()

            except KeyError as err:
                print("忽略===", err)
            try:
                k = k8s_Env.objects.filter(Id=select_k8s_Env)

                if len(k) == 0:
                    print("选择k8s_Env  不存在走默认")
                else:
                    print("选择k8s_Env  存在更新", tc[0].k8s_Env, k[0])
                    _tc = TaskCreate.objects.get(Id=select_k8s_Env)
                    ts = TaskDeploy.objects.get(version=version)
                    ts.select_HostGroup = k[0]
                    ts.save()

                    _tc.k8s_Env = k[0]
                    _tc.save()

            except KeyError as err:
                print("忽略", err)

                return Response(d)


            # build_jenkins.delay(Id)
            taskDeploy_obj = TaskDeploy.objects.get(version=version)
            try:
                payload = json.loads(request.body.decode("utf-8"))
                head_commit = payload.get("head_commit")
                if head_commit:
                    commit_id = head_commit.get("id")
                    author_username = head_commit.get("author").get("username")
                    commit_message = head_commit.get("message")
                    commit_timestamp = head_commit.get("timestamp")
                    print("commit_id", commit_id)
                    print("author_username", author_username)
                    print("commit_message", commit_message)
                    print("commit_timestamp", commit_timestamp)
                    taskDeploy_obj.User = "Webhook-" + author_username
                    taskDeploy_obj.save()

            except:
                print("error bod")

            print("开始更新")
            build_jenkins_.delay(taskDeploy_obj.Id, str(taskDeploy_obj.User))

    except Exception as e :
        return HttpResponse("%s" % e)

    return HttpResponse("执行成功")
