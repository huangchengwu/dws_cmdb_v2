import json
from asgiref.sync import async_to_sync

import datetime
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import time
from django.shortcuts import render
from channels.layers import get_channel_layer
from utils.jenkins_server import Jenkins_server
from django.conf import settings  # noqa


def get_jenkins_log(job_name):
    server = Jenkins_server(
        settings.JENKINS_URL,
        username=settings.JENKINS_USER,
        password=settings.JENKINS_PASSWORD,
        timeout=None,
    )

    get_build_info = server.get_job_info(job_name)
    job_id = get_build_info["lastBuild"]["number"]

    log = server.get_build_console_output(job_name, job_id)
    status = server.get_build_info(job_name, job_id)

    return log, status["result"] 

def get_jenkins_log_id(job_name,job_id):
    server = Jenkins_server(
        settings.JENKINS_URL,
        username=settings.JENKINS_USER,
        password=settings.JENKINS_PASSWORD,
        timeout=None,
    )
    print("===任务==",job_name,job_id)

    log = server.get_build_console_output(job_name,job_id)
    status = server.get_build_info(job_name,job_id)

   
    return log, status["result"]

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["Id"]
        # 直接从用户指定的房间名称构造 Channels 组名称，不进行任何引用或转义
        self.room_group_name = "room_%s" % self.room_name
        self.user = self.scope["user"]  # 获取用户信息
        self.is_closed = False
        print(
            self.room_group_name,
            self.user,
        )
        # 将新的连接加入到群组
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # 接受连接
        await self.accept()

    async def disconnect(self, close_code):  # 断开时触发
        self.is_closed = True
        # 将关闭的连接从群组中移除
        print("移除disconnect", self.room_name, self.room_group_name, self.user)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):  # 接收消息时触发
        ds = json.loads(text_data)
        try:
            job_id = ds["job_id"]
            print(ds)
            log, status = get_jenkins_log_id(ds["job_name"], job_id)
            await self.send(
                text_data=json.dumps(
                    {
                        "status": status,
                        "log": log,
                    },
                    indent=4,
                )
            )

        except KeyError as err:
            
            log, status = get_jenkins_log(ds["job_name"])

            await self.send(
                text_data=json.dumps(
                    {
                        "status": status,
                        "log": log,
                    },
                    indent=4,
                )
            )


class AsyncConsumer(AsyncWebsocketConsumer):
    async def connect(self):  # 连接时触发
        self.room_name = self.scope["url_route"]["kwargs"]["Id"]
        # 直接从用户指定的房间名称构造 Channels 组名称，不进行任何引用或转义
        self.room_group_name = "room_%s" % self.room_name
        self.user = self.scope["user"]  # 获取用户信息

        # print(self.user)
        print(
            self.room_group_name,
            self.user,
        )
        # 将新的连接加入到群组
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # 接受连接
        await self.accept()

        # 欢迎语
        msg = {"content": "👏👏：您来了，随便聊聊", "level": 2}
        await self.send(text_data=json.dumps({"message": msg["content"]}))

    async def disconnect(self, close_code):  # 断开时触发
        # 将关闭的连接从群组中移除
        print("移除", self.room_name, self.room_group_name, self.user)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):  # 接收消息时触发
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print("接收消息", message)
        # 信息群发
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "system_message",
                "message": message,
            },
        )

    # Receive message from room group
    async def system_message(self, event):
        message = event["message"]

        print(self.room_group_name, self.user, message)

        # Send message to WebSocket单发消息
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                }
            )
        )
