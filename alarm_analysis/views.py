 
from rest_framework.generics import GenericAPIView
from rest_framework import serializers,status
 
from rest_framework.response import Response
 
from utils.helm_enc import *
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from rest_framework.decorators import action
from jinja2 import Template
 
 
from django.http import HttpResponseForbidden, FileResponse
import os
from rest_framework.authtoken.models import Token
 
from django.shortcuts import redirect,render
from urllib.parse import quote
from django.conf import settings  # noqa
from dws_cmdb.tasks import Task_disable
 
import markdown
import io
import zipfile
from django.urls import reverse
 
from django.contrib.auth.decorators import login_required

import requests
import json
import time
from docx import Document

# 发送消息并返回消息ID
def do_task_send_text(token, payload):
    url = "https://t.hitosea.com/api/dialog/msg/sendtext"
    headers = {
        "Content-Type": "application/json",
        "Token": token
    }
    
    response = requests.post(url, headers=headers, json=payload)
  
    if response.status_code != 200:
        print("Error sending HTTP request:", response.text)
        return None

    res_map = response.json()
    print(res_map)
    dialog_id =  11
    return dialog_id

# 获取单会话消息
def do_task_one(token, payload):
    url = "https://t.hitosea.com/api/dialog/one"
    headers = {
        "Content-Type": "application/json",
        "Token": token
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code != 200:
        print("Error sending HTTP request:", response.text)
        return ""

    res_map = response.json()
    return res_map["data"]["last_msg"]["msg"]["text"]

# 登录
def do_task_login(payload):
    url = "https://t.hitosea.com/api/users/login"
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
        print("Error sending HTTP request:", response.text)
        return ""

    res_map = response.json()
    return res_map["data"]["token"]

# 转换为 Markdown
def convert_md(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Markdown file written successfully.")

# 导出 DOCX
def export_docx():
    doc = Document("word/测试表格.docx")
    for para in doc.paragraphs:
        print(para.text)


    
# Create your views here.
class  AlertGroupViewSet(ModelViewSet):
    queryset = AlertGroup.objects.all()
    serializer_class = AlertGroupSerializer
    @action(methods=["put"], detail=True, url_path="AlertGroup_run")
    def TaskEnc_exec(self, request, *args, **kwargs):
        # Id = kwargs["pk"]
        # action = request.data["action"]
        # version = int(time.time())
        print("分析日志")
 
      

        login_payload = {
            "email": "17710136904@163.com",
            "password": "Qq751164212.",
        }


        token = do_task_login(login_payload)
        print(token)
        sendtext_payload = {
            "dialog_id": "9146",
            "text": "你好GPT你是什么时候诞生的",
        }
   
        content = do_task_send_text(token, sendtext_payload)

        # convert_md("example.md", content)

        return Response({"msg": "执行成功,请刷新", "status": True})
