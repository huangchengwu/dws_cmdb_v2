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
c="""
#导入镜像使用的storageclass
ImagesStorageClassName=csi-cephrbd-sc1

#DIYLINK各服务使用的storageclass
ServerStorageClassName=csi-cephfs-sc

#CAC
##lsbIP地址
lsbip=103.63.136.109
##默认域名
defaultDomain=keli.vip

#OVS
##flow-metric-service的服务IP
Ovs-service=
##pushgateway服务IP
Report-pro-ip=

##vdpa-register-config(节点IP和节点主机名)
ovsUrl=103.63.136.110,103.63.136.120
nodeName=k8s-1,k8s-2

# Neutron
##ovn、ovs数据库连接IP和keyston认证服务IP
nodeIP=103.63.136.110


#插件服务
##Neutron连接信息
Neutron_keyston=http://103.63.136.110:32751
Neutron_network=http://103.63.136.110:32750
Neutron_username=neutron
Neutron_password=Dxqu6%WkK5HvDt%!
Neutron_domainID=default
Neutron_projectName=service
Neutron_projectID=
Diylink_pubnetworkID=

#flow插件配置
influxDBAuthToken=inflixdbtoken
influxDBBucketName=diylink
influxDBOrgName=diylink

###ceph-csi配置
##集群ID(查询命令:ceph -s |grep id |awk '{print $2}')
Cluster_ID=a5fd1964-4c93-11ee-a025-bf5504d93fa2
##rbd池(查询命令:ceph osd pool autoscale-status)
Ceph_pool=kubernetes
##fs名称(查询命令:ceph  fs ls |awk -F ',' '{print $1}')
Ceph_fsName=k8s-fs

#kubevirt
##版本
RELEASE=v1.0.0


#=====k8s集群部署

#k8s集群初始化参数,多个IP使用逗号 "," 隔开
##master0ip 为执行脚本master服务IP
master0ip=66.66.0.1
##masterip为，加入集群当master的服务IP
master1ip=66.66.0.2,66.66.0.3
nodeip=66.66.0.4,66.66.0.5

##多master开启功能、 true / false
masters=true
##k8s版本
kubernetes_version=1.27.3
##apiserver地址
apiserver_advertise_address=66.66.0.10
##pod网段
pod_network_cidr=10.11.0.0/16
##service网段
service_cidr=10.20.0.0/16

##集群多master高可用配置
##使用nginx代理时，需要把代理服务器IP加上和其他master的Ip加上
control_plane_endpoint=66.66.0.10:6443
apiserver_cert_extra_sans=66.66.0.10,66.66.0.2,66.66.0.3,66.66.0.1
"""


class Custom_EnvForm(forms.ModelForm):
    config = forms.CharField(
        widget=AceWidget(mode="yaml", theme="twilight", width="1000px", height="500px"),
        initial=c,
    )
    custom_button = forms.CharField(widget=forms.HiddenInput(), initial='')

    class Meta:
        model = k8s_node
        exclude = []


@admin.register(k8s_node)
class Custom_EnvAdmin(admin.ModelAdmin):
    list_display = ("Id", "config")  # list

    search_fields = ("Id", "config")  # list

    exclude = []
    form = Custom_EnvForm

@admin.register(k8s_cluster_create)
class k8s_cluster_createAdmin(admin.ModelAdmin):
    pass




