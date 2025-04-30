from django.db import models
from django.utils import timezone
from Doc.models import HelpDocuments
# Create your models here.


class Host(models.Model):
    # 主机名
    hostname = models.CharField(max_length=255, unique=True, verbose_name="主机名")
    # 内网 IP 地址
    internal_ip_address = models.GenericIPAddressField(
        unique=True, verbose_name="内网 IP 地址", null=True, blank=True
    )
    # 外网 IP 地址
    external_ip_address = models.GenericIPAddressField(
        unique=True, verbose_name="外网 IP 地址", null=True, blank=True
    )
    # SSH 用户名
    ssh_username = models.CharField(max_length=255, verbose_name="SSH 用户名")
    # SSH 密码
    ssh_password = models.CharField(max_length=255, verbose_name="SSH 密码")
    # 操作系统版本
    os_version = models.CharField(
        max_length=255, verbose_name="操作系统版本", null=True, blank=True
    )
    # 内核版本
    # kernel_version = models.CharField(max_length=255, verbose_name="内核版本")

    class Meta:
        verbose_name = "主机配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hostname

class Custom(models.Model):
    # 集群名字
    name = models.CharField(max_length=255, verbose_name="配置名")
    config = models.TextField(verbose_name="配置内容", default="")

    class Meta:
        verbose_name = "自定义变量"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name





docker_env = """
#####env config
###cloud7
APP_NAME=Cloud7
APP_ENV=local
APP_KEY=
APP_DEBUG=true
APP_SCHEME=auto

APP_URL=https://cloud7.keli.vip

VITE_APP_DEBUG=

APP_PORT=3355

LOG_CHANNEL=stack
# LOG_DEPRECATIONS_CHANNEL=null
LOG_LEVEL=debug

DB_CONNECTION=mysql
DB_HOST=mariadb-svc
DB_PORT=3306
DB_DATABASE=cloud7
DB_USERNAME=root
DB_PASSWORD=root

DB_ROOT_PASSWORD=root
DB_PREFIX=pre_

BROADCAST_DRIVER=log
CACHE_DRIVER=redis
# FILESYSTEM_DISK=local
QUEUE_CONNECTION=redis
SESSION_DRIVER=redis
SESSION_LIFETIME=120

MEMCACHED_HOST=127.0.0.1

REDIS_HOST=redis-svc
REDIS_PASSWORD=null
REDIS_PORT=6379

MAIL_MAILER=smtp
MAIL_HOST=mailhog
MAIL_PORT=1025
MAIL_USERNAME=null
MAIL_PASSWORD=null
MAIL_ENCRYPTION=null
MAIL_FROM_ADDRESS=null
MAIL_FROM_NAME="${APP_NAME}"

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=us-east-1
AWS_BUCKET=
# AWS_USE_PATH_STYLE_ENDPOINT=false

PUSHER_APP_ID=
PUSHER_APP_KEY=
PUSHER_APP_SECRET=
PUSHER_APP_CLUSTER=mt1

MIX_PUSHER_APP_KEY="${PUSHER_APP_KEY}"
MIX_PUSHER_APP_CLUSTER="${PUSHER_APP_CLUSTER}"

LARAVELS_LISTEN_IP=0.0.0.0
LARAVELS_LISTEN_PORT=30000
LARAVELS_DISPATCH_MODE=2
LARAVELS_TASK_WORKER_NUM=60
LARAVELS_WORKER_NUM=15

DOCKER_ID=

PUBLISH_DEVICE_KEY=

ROUTE_URL=https://hicloud.keli.vip
NETWORK_URL=https://hicloud.keli.vip

APP_SERVICE_URL=http://nginx-svc.cloud7
NETWORK_SERVICE_URL=http://nginx-svc.hicloud
ROUTE_SERVICE_URL=http://nginx-svc.hicloud

AUTHENTIK_ENABLED=
AUTHENTIK_APP_NAME=
AUTHENTIK_API_TOKEN=
AUTHENTIK_API_URL=

# 控制中心和网络中心的秘钥
ADMIN_SECRET=


"""
dockerfile = """
FROM  kuaifan/php:swoole-8.0.rc9
COPY ./co /var/www
"""


kube_config = """
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUMvakNDQWVhZ0F3SUJBZ0lCQURBTkJna3Foa2lHOXcwQkFRc0ZBREFWTVJNd0VRWURWUVFERXdwcmRXSmwKY201bGRHVnpNQjRYRFRJek1EWXdOVEEyTXprek5Wb1hEVE16TURZd01qQTJNemt6TlZvd0ZURVRNQkVHQTFVRQpBeE1LYTNWaVpYSnVaWFJsY3pDQ0FTSXdEUVlKS29aSWh2Y05BUUVCQlFBRGdnRVBBRENDQVFvQ2dnRUJBTkhGCnlEclBSWkRjcHR5Y3hwZ1BPLzh4T1NzY3IyN0NtODVHRjduRWRYc3A4TE1kRHF0WFBHU1NGOEF0WUJ3M3hGSE0KcHErMnB1TVhTSXZuaDZobXFBUnBxREpOOWxFb0d3ckxlUzVBL2V2clhKcmZxejRHVnEweGNqZjZ1ODB1d3A1TQpaWEJERFhwKzh5Q3Q2NllhUDlQeWR1RHJOWnBoekd3V0k2OFlnU1hhTVFWajM2ODFpNE9KUVVRd3ByeHpGNG8zCmRvbEVuWk4ya2MwbzFCanYwQm4vd1dLNm1hQnNaOGxBNzRtVGVkVGlxRXltdFNKWEJ4WkthNDVTcGg4dVR2SHIKbkpVaHM2bktXQ2NNb3R4OVRNMVl5blBLZmx0UjJ4YjlNNzFWdkpFdW9JVm1vR2c0RVA0WG9rU2lsMDFMRkNOcgpYemZkVm15VkJqVnAzaWREUHcwQ0F3RUFBYU5aTUZjd0RnWURWUjBQQVFIL0JBUURBZ0trTUE4R0ExVWRFd0VCCi93UUZNQU1CQWY4d0hRWURWUjBPQkJZRUZGSFcxQ1lwdGo0VjBEcmFnWHN5RHY5clFKRFVNQlVHQTFVZEVRUU8KTUF5Q0NtdDFZbVZ5Ym1WMFpYTXdEUVlKS29aSWh2Y05BUUVMQlFBRGdnRUJBS0RxVUxaOHNnNGdUMGlQVmYwZgpQekdhdlhDMjRjYVUyeURoOGlJTDBRMVlCVXhManl3V2tmQ2tSazlqalJWWllZcXpvMi9uTGZHR1JSdUh0ai9LCk9ES1V6b01rSENzVTB5TmdtWURGM0x3QXNjUnFlcFUrOU50UXcxTlhQcDFkWDNoS0tFSzdrdzNyeFdpMktxdDIKWDJ5eGhyTWYyMEtFVHNaTDE3eEt3b1JQWTZIK2srenIwTFJHMmlkeTQwa0VsWmZ6VzVpak5zY1JDVGEwUnVYRAprLzB6cUYyRUZBbnQxcEoza3BtQ2JSZk91dWdvdGI4WUMrV0Exb25mcE9IMmkrT1N2RmRORERHSHRKZ0h5TTBwCjdyeWlCMmlhRnBmSlR4R2VaYmQzeFNja0NNZUEyY01vN0Z1eHNnWTFLTWs3ei9qYXY2YXN2VDl2WWhIVzNWaVgKTlVnPQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    server: https://43.229.28.92:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
current-context: kubernetes-admin@kubernetes
kind: Config
preferences: {}
users:
- name: kubernetes-admin
  user:
    client-certificate-data: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSURJVENDQWdtZ0F3SUJBZ0lJVFBCZ3ZwSi9PV0l3RFFZSktvWklodmNOQVFFTEJRQXdGVEVUTUJFR0ExVUUKQXhNS2EzVmlaWEp1WlhSbGN6QWVGdzB5TXpBMk1EVXdOak01TXpWYUZ3MHlOREEyTURRd05qTTVOREJhTURReApGekFWQmdOVkJBb1REbk41YzNSbGJUcHRZWE4wWlhKek1Sa3dGd1lEVlFRREV4QnJkV0psY201bGRHVnpMV0ZrCmJXbHVNSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQTYrNENnN2hZTTVaMU45aXYKWGc2SEhhWFYxd1k2bFhJWS9rZ0dCZnczZ2xVQ2JpWmt4SU9ESEx1M2FTQkVIZGxJV3ZqU0dYWWJrUEI2ZHp1VQpMOVhENlNQRHFsaXRjVjBqUHpYcG0zL0RhVmQrRHc3UURUZ0RlaUhjdkpWV2hid2tOTFVFQ3B6OTNNT2V3WGhhCnBoV3ZQL0paRlZoUVJYRjJFZlpCeFBUTVA0RTRlNUxaa1BUL3UyZnE3VUhhTXFoVXdMdzhKdTZZOTBheVZjODYKdCtZVk1tNnhSZ1RhN1pvZVV4OURUdzRDb1dxNldwRW8yS0IyeXk3SjIwQTZEN1pKTnJRalJMK1c4c21KMmdhNQpnck90a3Jqbk9YQmc4WERqSDdMS0JERUxvN0VBNXFYMW5TVDdNQlJMbDFpR0poTEt1OTdEa1VEeDBDTGp6WDJ3CnB5NjFVd0lEQVFBQm8xWXdWREFPQmdOVkhROEJBZjhFQkFNQ0JhQXdFd1lEVlIwbEJBd3dDZ1lJS3dZQkJRVUgKQXdJd0RBWURWUjBUQVFIL0JBSXdBREFmQmdOVkhTTUVHREFXZ0JSUjF0UW1LYlkrRmRBNjJvRjdNZzcvYTBDUQoxREFOQmdrcWhraUc5dzBCQVFzRkFBT0NBUUVBcDhKajhuQzhTblVTcTgrdThFd05UUzFXN0NHcW5aNnIxOS91CmVvYmJhd3Z0azhNdktzZ21tRytLUjBER090b1cvNE9KeTAzWGtmRFM3KzgzMWpLYUhJTHMrZVlUUzc3WXRQQzcKRXdDT2lIeGo3bENrQzAwSEUzY3BoTmR3UUxaSFk2Y0l5cWdmZW1VOVJXRW5pR2hTd0JYYUV2RlQxQVVKL0pFZgpyNmZ5MUVCeGhkWTI5UU1WWEpkNHorejNld2dEZDhFSzlwR1Y3ZXBFQVcxVEVacmdESHdVSzB0VUNLMkZDRm0wCkQxMmFWbERqL0Rmd2FWZjdyekFvN3dWVVFtU2hiYzZ0SEcxZy85VCtJZDluKys1VWdUZnE3L2dkdVhxMzVMdFQKMXhUN1pHbmNSeXAyMkhsa2tiR1hCdUJacmpYZm56c2tGZzd1OW93bWlYcXlWOExIZVE9PQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tCg==
    client-key-data: LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlFb2dJQkFBS0NBUUVBNis0Q2c3aFlNNVoxTjlpdlhnNkhIYVhWMXdZNmxYSVkva2dHQmZ3M2dsVUNiaVprCnhJT0RITHUzYVNCRUhkbElXdmpTR1hZYmtQQjZkenVVTDlYRDZTUERxbGl0Y1YwalB6WHBtMy9EYVZkK0R3N1EKRFRnRGVpSGN2SlZXaGJ3a05MVUVDcHo5M01PZXdYaGFwaFd2UC9KWkZWaFFSWEYyRWZaQnhQVE1QNEU0ZTVMWgprUFQvdTJmcTdVSGFNcWhVd0x3OEp1Nlk5MGF5VmM4NnQrWVZNbTZ4UmdUYTdab2VVeDlEVHc0Q29XcTZXcEVvCjJLQjJ5eTdKMjBBNkQ3WkpOclFqUkwrVzhzbUoyZ2E1Z3JPdGtyam5PWEJnOFhEakg3TEtCREVMbzdFQTVxWDEKblNUN01CUkxsMWlHSmhMS3U5N0RrVUR4MENManpYMndweTYxVXdJREFRQUJBb0lCQUNGaXl1Uk0zOTVjK2pWdQo2bElMQ0QrL3llVGxzc0NYSnNaRTl1VTk3YlQ1eHFCRHVwcThhWDlWYVB6dFhmWkRXeVBVZGhhNFNlcFd2VjNHCkJwQkdWYlRXSk1na1NGYjBjUnB1ektIK2tHNkZ2UWJ3ZDZ5SE1xYkR4L0sveDBDaGdSWWNUM2daQXl1TVd4alIKcVRJN2UxTTNQamZ4Q1ZycVZXVHhUaGxLOHVSQlpXaWcxcThIMm1mV1NsMlZvcTBVaCtSY2djY0xNY1JXL0xYNgo5N1hHTWR1cXBhVll6SEJSSGFvYWtZL1lhM0JWd2hWenZGdVcwMy91MXkwQTEzQTdLQlN1czd3YmtaaFBmQkVnCm51aGNKTkZSd2pmZ2c1L21LcXRSanJFYkM1YmxJVDRKVXlGZ2l4UUl3aVFIY3ZKMTFTQXVWemIwb3o3YzVCblYKa0ZCMEFuRUNnWUVBOW0waUtxU3QxakRvbVNEOUNMUGVjdWZxYU56YWJyNXJjbGZ6OFdob0xyL2djSUNWcEo3dQpBNG4xT2tzejk0Y2ppSjROUDBnY1JTNUI0dWJRWndnZVIwTGZqZDRySzZzTllYdWE5Zzg0dm9RT09aOVVnOTVNCmJac0NKOU1FV0l3Rm5adDBYc2tWQ28zT2ZLUWZobXNrU2pIS1BsYWhMWVBkSitoU1ZDRWlFTmNDZ1lFQTlSaDcKTVJ0M1ViMjJGSk5aWjEyVFFTcXVwMmxNdXhuZEp6dFA1UG9XWlNkblM0bDNWV24xRnh1L3hOSlVvQWlGOUUvQwpvazg2UzVoVmI0dER6N0FFYllDVzU1Vk9GNWFLMksvSFdrN0xBaDV3dU80QlJGdVV5cmY0MkhGLzB1VGJzUEI0Cm5CdmxvMU9iQzMzY2picGJxUE9LMlJ3SytiS3QvdGUxTmtPUjQrVUNnWUFLZnBWUTZaaDVvYldXSitCK3lXSTAKMUltWUU2ZTl4YUEveTEwWkw5QVlCWlhpVktlS3pqWG1zcTVkNEN3RFk1N3d4NEphNnBCQnBmbXFWeGdTK3phRwo1R011NElKSUpzMjRGQktDWGgyVmgzd3ZtZ2g0WVRReUNzTHB2VVBYSFlkenNkWWYzMEpsSTZyaWhmN05zNnhrCitIL2JiY2NKY0M4djd1WHFyVXFOR3dLQmdGUWRuc252dnplU2dGYjNhd3VLbGVzYmx1MWx1aXZNYUpYNlNTVXcKbjFiLyt2ZDFxanJxTG05TDJyalY1cTAxdjZObGJFc0FIZVdyMWtaOTZUdnlFTkx6K3RabjYzRTAvVm40bWRabwpqRXVoM3RYWStSNVl2K3dDejZpWTYyR1pvYnhNQzFpb1NsdVBhZnE3cTJJSXYwUndzUXBxRVdvNDVIWTkyYmRSCjRWUHhBb0dBQlVEOExXcGVHcEE3MkVmU2ZSeDQyMW9CQlVYUDJpSzNzVXZ6OGFkN2ZjTTgzVzNrWUgxOURqR0IKU0hXOWFvRGRRUThqd1IxVng3VlA2SkwxM3lUMXh3bUF2NWtjcmlEcGJJTmRUbVVmdUFsYzhiNk1sV2lMV21LZgpqNzBZZ01GbTZiWGFtU1RRUE5zUWJOckw5VWt3Y1MrU1dDNWlMaW1MeFdvMXN0NElYckU9Ci0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0tCg==
"""
# 部署环境


class Custom_Env(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="配置名",
        max_length=255,
        blank=True,
        default="custom.yaml",
        unique=True,
    )
    config = models.TextField(verbose_name="自定义配置内容", default=kube_config)

    class Meta:
        verbose_name = "自定义配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


    

class k8s_Env(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="环境名",
        max_length=255,
        blank=True,
        default="43.229.28.92[测试环境]",
    )
    kube_config = models.TextField(verbose_name="配置", default=kube_config)

    class Meta:
        verbose_name = "集群配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


init_shell = """#!/bin/bash
"""
deploy_config = """apiVersion: tekton.dev/v1
kind: Task
metadata:
  name: build-php
spec:
  steps:
    - name: git-pull
      image: huangchengwu6904/hi-app:hi-tools-1
      workingDir: /workspace/git-repo
      script: |
            #!/usr/bin/env sh
            git clone  git@github.com:huangchengwu/dws_cmdb.git  .
    - name: build-ci
      image:  docker:dind
      securityContext:
        privileged: true  
      workingDir: /workspace/git-repo
      script: |
            #!/usr/bin/env sh
            nohup dockerd &
            cat >Dockerfile<<EOF
            FROM huangchengwu6904/hi-app:dws_cmdb-base
            COPY . /dws_cmdb
            EOF
            time=`date -u +%s`
            echo "Qq751164212." | docker login --username huangchengwu6904 --password-stdin
            docker build -t huangchengwu6904/hi-app:dws_cmdb-${time} .
            docker push huangchengwu6904/hi-app:dws_cmdb-${time}
            docker rmi  huangchengwu6904/hi-app:dws_cmdb-${time}
            echo "huangchengwu6904/hi-app:dws_cmdb-${time}" >version

            
    - name: helm-deploy-cd
      image: huangchengwu6904/hi-app:hi-tools-1
      workingDir: /workspace/git-repo
      script: |
            #!/usr/bin/env sh
        
            ln -s /etc/k8s_config/43.229.28.92  ~/.kube/config
            helm status my-haitun-cmdb  -n haitun-cmdb &&  helm  upgrade  my-haitun-cmdb  ./helm/dws_cmdb  --set cmdb.image=`cat version`  --namespace  haitun-cmdb  ||  helm install my-haitun-cmdb  ./helm/dws_cmdb --set cmdb.image=`cat version`   --namespace  haitun-cmdb

"""


# 项目模板
class pTemp(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="模版名字", max_length=255, blank=True, default="php项目"
    )
    init_shell = models.TextField(verbose_name="初始化脚本", default=init_shell)
    deploy_config = models.TextField(verbose_name="部署配置", default=deploy_config)

    deploy_env = models.ForeignKey(
        k8s_Env,
        on_delete=models.CASCADE,
        verbose_name="部署环境",
        related_name="pk_env",
        null=True,
    )

    class Meta:
        verbose_name = "项目模版"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


chart = """
apiVersion: v2
name: redis
description: A Helm chart for Kubernetes
type: application
version: 0.1.0
appVersion: "1.16.0"
"""

values = """
storageClassName:   csi-cephfs-sc
redis:
  image: redis:alpine
  storage: 8Gi
  password: idc123456
"""

templates = """
apiVersion: v1
kind: Service
metadata:
  name: redis-svc
  namespace:  {{ .Release.Namespace }}

spec:
  selector:
    app: redis
  ports:
    - protocol: TCP
      port: 6379
      targetPort: 6379
"""


class Templates(models.Model):
    Id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=255, verbose_name="模版名", default="hosts", unique=True
    )
    templates = models.TextField(verbose_name="templates内容", default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "模版配置"
        verbose_name_plural = verbose_name


class HiAppstoreTemplates(models.Model):
    Id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=255, verbose_name="模版名", default="redis-svc.yaml", unique=True
    )
    templates = models.TextField(verbose_name="templates内容", default=templates)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商店模版"
        verbose_name_plural = verbose_name

consule_config="""#以下是prometheus例子port外部端口   server内部主机对应的nodePort端口
- name : "prometheus"
  port: "30682"
  server:
  - "10.255.100.1:30682"
  - "10.255.100.3:30682"
"""
class consuleManger(models.Model):
    Id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=255, verbose_name="配置名", default="115-ingress-wan", unique=True
    )
    templates = models.TextField(verbose_name="consule_config配置内容", default=consule_config)
    wlan = models.CharField(
        max_length=255, verbose_name="外网ip", default="43.229.28.252", unique=True
    )
    describe= models.TextField(verbose_name="描述", default="ingress-wan 外网配置请部署到服务器")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "consul配置管理"
        verbose_name_plural = verbose_name



configmap = """
apiVersion: v1
kind: ConfigMap
metadata:
      name: conf
      namespace: {{ namespace }} 

"""


class TaskLog(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.TextField(verbose_name="日志名字", default="")

    def __str__(self):
        return self.name


class Task(models.Model):
    Id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=255, verbose_name="任务名", default="helm-deploy", unique=True
    )
    task_log = models.ManyToManyField(TaskLog)

    pipeline = models.TextField(verbose_name="pipeline", default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "任务配置"
        verbose_name_plural = verbose_name


class HiAppstore(models.Model):
    Id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=255, verbose_name="应用名字", default="cloud7", unique=True
    )
    templates = models.ManyToManyField(HiAppstoreTemplates)
    chart = models.TextField(verbose_name="chart", default=chart)
    values = models.TextField(verbose_name="values", default=values)
    configmap = models.TextField(verbose_name="configmap", default=configmap)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "应用商店"
        verbose_name_plural = verbose_name


host_key = """
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtz
c2gtZWQyNTUxOQAAACAPt7r7LqglSQ/wuxb1A7A1T+QkK3WAgiYX1zsgTfhWeQAA
AIh9yMSsfcjErAAAAAtzc2gtZWQyNTUxOQAAACAPt7r7LqglSQ/wuxb1A7A1T+Qk
K3WAgiYX1zsgTfhWeQAAAEBLUpcmnKqgjubxOsh5TT5hpKkzD/02FJD0csuIzMdF
Gg+3uvsuqCVJD/C7FvUDsDVP5CQrdYCCJhfXOyBN+FZ5AAAAAAECAwQF
-----END OPENSSH PRIVATE KEY-----
"""


class HostConfig(models.Model):
    types = [
        ("密码", "密码"),
        ("密钥", "密钥"),
    ]

    Id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="主机名", default="test")
    user = models.CharField(max_length=255, verbose_name="用户", default="ubuntu")
    port = models.CharField(max_length=255, verbose_name="端口", default="22")
    ip = models.CharField(
        max_length=255, verbose_name="ip地址", default="43.229.28.21", unique=True
    )

    password = models.CharField(
        max_length=255, verbose_name="密码", default="7H2W4EupGqKXbpZR"
    )
    host_key = models.TextField(verbose_name="密钥", default=host_key)

    types = models.CharField(
        choices=types, max_length=255, verbose_name="密码类型", default=0
    )

    def __str__(self):
        # return str(self.Id) + ":" + self.name + ":" + self.user + ":" + self.ip
        return  self.name +   ":" + self.ip

    class Meta:
        verbose_name = "主机配置"
        verbose_name_plural = verbose_name


class web_monitor(models.Model):
    Id = models.AutoField(primary_key=True)
    url = models.CharField(
        verbose_name="网站", max_length=255, blank=True, default="www.baidu.com"
    )
  
    monitor_host = models.ForeignKey(
        HostConfig,
        on_delete=models.CASCADE,
        verbose_name="form_monitor_host",
        related_name="pk_monitor_host",
        null=True,
        blank=True,
    )

    certificate_effective = models.CharField(
        verbose_name="证书有效时间", max_length=255, blank=True, default=0
    )

    certificate_path = models.CharField(
        verbose_name="证书路径", max_length=255, blank=True, default="/etc/nginx/ssl/"
    )


    m_status = [
        ("未启动", "未启动"),
        ("本地模式", "本地模式"),
        ("远程模式", "远程模式"),
    ]

    web_type = [
        ("http", "http"),
        ("https", "https"),
    ]

    web_code = models.CharField(
        verbose_name="web状态码", max_length=255, blank=True, default="0"
    )
    web_type_status = models.CharField(
        choices=web_type, max_length=255, verbose_name="链接类型", default=2
    )
    monitor_status = models.CharField(
        choices=m_status, max_length=255, verbose_name="证书功能", default=1
    )

    describe = models.CharField(
        verbose_name="描述信息", max_length=255, blank=True, default=""
    )

    updated_at = models.DateTimeField(auto_now=True, verbose_name="最后修改时间")

    class Meta:
        verbose_name = "监控配置"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.url


class HostGroup(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="组名", default="内网测试", unique=True
    )

    Host = models.ManyToManyField(HostConfig)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "主机组"
        verbose_name_plural = verbose_name


class Webhook(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255,
        verbose_name="任务名",
        default="",
    )
    url = models.CharField(
        max_length=255,
        verbose_name="url",
        default="http://cmdb.keli.vip/Webhook/?taskdeploy_env=18&task_type=1&select_HostGroup=7",
    )
    SECRET = models.CharField(
        max_length=255,
        verbose_name="SECRET",
        default="q5smMgRhHnQ/SZbwm5qxPsdljoMmC75cwKI/kTaSrfE=",
    )

    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.SECRET

    class Meta:
        verbose_name = "Webhook"
        verbose_name_plural = verbose_name


class Task_type(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="名字", default="", unique=True
    )
    types = [
        ("一次性", "一次性"),
        ("周期性", "周期性"),
    ]
    types = models.CharField(
        choices=types, max_length=255, verbose_name="任务类型", default=0
    )
    templates = models.TextField(verbose_name="templates内容", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "任务计划"
        verbose_name_plural = verbose_name


class TemplatesGroup(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="模版组", default="helm发布", unique=True
    )

    group = models.ManyToManyField(Templates)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "模版组"
        verbose_name_plural = verbose_name


class Project(models.Model):
    Id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=255, verbose_name="项目", default="cloud7", unique=True
    )
    version = models.CharField(
        max_length=255,
        verbose_name="当前版本",
        default="1690610777",
        null=True,
        blank=True,
    )
    env_template = models.ForeignKey(
        TemplatesGroup,
        on_delete=models.CASCADE,
        verbose_name="部署模版",
        related_name="pk_env_template",
        null=True,
    )
    domain = models.CharField(
        max_length=255, verbose_name="部署域名", default="pwf.keli.vip"
    )
    dockerfile = models.TextField(verbose_name="dockerfile", default="")
    cmd = models.TextField(verbose_name="shell", default="")
    configmap = models.TextField(verbose_name="configmap", default=configmap)

    values = models.TextField(verbose_name="values.yaml", default=values)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "项目配置"
        verbose_name_plural = verbose_name


class Pipeline(models.Model):
    Id = models.AutoField(primary_key=True)

    name = models.CharField(
        max_length=255, verbose_name="pipeline名", default="hellowold", unique=True
    )
    pacakge = models.FileField(
        upload_to="pipeline/uploads/", verbose_name="其他压缩包", blank=True, null=True
    )  # 文件上传字段

    templates = models.TextField(verbose_name="pipeline", default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "pipeline"
        verbose_name_plural = verbose_name


class TaskCreate(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="任务名", default="hellowolrd", unique=True
    )

    templateGroup = models.ForeignKey(
        TemplatesGroup,
        on_delete=models.CASCADE,
        verbose_name="form_templateGroup",
        related_name="pk_templateGroup",
        null=True,
        blank=True,
    )
    task_type = models.ForeignKey(
        Task_type,
        on_delete=models.CASCADE,
        verbose_name="任务类型",
        related_name="pks_task_type",
        null=True,
    )
    pipeline = models.ForeignKey(
        Pipeline,
        on_delete=models.CASCADE,
        verbose_name="form_pipeline",
        related_name="pk_pipeline",
        null=True,
    )

    HostGroup = models.ForeignKey(
        HostGroup,
        on_delete=models.CASCADE,
        verbose_name="form_HostGroup",
        related_name="pk_HostGroup",
        null=True,
        blank=True,
    )
    k8s_Env = models.ForeignKey(
        k8s_Env,
        on_delete=models.CASCADE,
        verbose_name="form_k8s_Env",
        related_name="pk_k8s_Env",
        null=True,
        blank=True,
    )
    Custom_Env = models.ForeignKey(
        Custom_Env,
        on_delete=models.CASCADE,
        verbose_name="form_Custom_Env",
        related_name="pk_Custom_Env",
        null=True,
        blank=True,
    )

    help = models.ForeignKey(
        HelpDocuments,
        on_delete=models.CASCADE,
        verbose_name="帮助文档",
        related_name="pk_help",
        null=True,
        blank=True,
    )
    rollBack_type = [
        ("否", "否"),
        ("是", "是"),
    ]
    rollBack = models.CharField(
        choices=rollBack_type, max_length=255, verbose_name="是否支持回滚", default=0
    )

    agent_celery_type = [
        ("否", "否"),
        ("是", "是"),
    ]

    agent_celery = models.CharField(
        choices=agent_celery_type,
        max_length=255,
        verbose_name="是否开启agent_celery",
        default=0,
    )

    # LocalVariable = models.TextField(verbose_name="局部变量配置", default="")
    class Meta:
        verbose_name = "任务创建"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class TaskEnc(models.Model):
    Id = models.AutoField(primary_key=True)

    name = models.CharField(max_length=255, verbose_name="名字")
    TaskEnctaskcreate = models.ForeignKey(
        TaskCreate,
        on_delete=models.CASCADE,
        verbose_name="任务选择",
        related_name="pk_TaskEnctaskcreate",
        null=True,
    )

    TaskButton = models.TextField(verbose_name="任务按钮", default="")
    Custom_Env = models.TextField(verbose_name="配置模版", default="")

    class Meta:
        verbose_name = "任务封装"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
class AutoTaskCreate(models.Model):
    Id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=255, verbose_name="任务名", default="hellowolrd", unique=True
    )

    custom_Task_type = [
        ("否", "否"),
        ("是", "是"),
    ]

    Custom_Task_type = models.CharField(
        choices=custom_Task_type, max_length=255, verbose_name="自定义配置", default=0
    )

    templates = models.TextField(verbose_name="pipeline", default="")

    class Meta:
        verbose_name = "一键新增任务"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
