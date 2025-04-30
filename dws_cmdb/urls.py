"""dws_cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url

from rest_framework import permissions
 
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.permissions import IsAuthenticated
from .views import Webhook
from django.contrib.auth.decorators import login_required
 
desc = """

# 登陆相关
```bash
#方法 1
curl -X 'GET' 'http://127.0.0.1:9091/ConfCen/HostConfig/' -H 'accept: application/json' -u "admin:admin"

#方法 2  token有效7天
curl -X 'POST' 'http://127.0.0.1:9091/api-jwt-auth/' -H 'accept: application/json'  -H 'Content-Type: application/json'  -H 'X-CSRFToken: UqJlSYn29YCTy5kGyDQNmIVpj3WxVeopYQUq47vyTvfSfEPQXpPCAYh2jcgDd3Xj' -d '{ "username": "admin", "password": "admin"}'


#登陆后使用
curl -X 'GET'   'http://127.0.0.1:9091/ConfCen/HostConfig/'  -H 'accept: application/json' -H "Authorization: jwt  $token"

 

curl -X 'POST' 'http://127.0.0.1:9091/DeployCen/Download/' -H 'accept: application/json'-H 'Content-Type: application/json' -u "admin:XEFCJ9DeR7tZIMJy64" -d '{"name": "1697769333-执行迁移k8s.zip"}' --output  test.zip

```


"""
schema_view = get_schema_view(
    openapi.Info(
        title="海豚有海运维系统 API",  # 名称
        default_version="版本 v1.0.0",  # 版本
        description=desc,  # 项目描述
    ),
    public=True,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    url("^$", admin.site.urls),
    path("ConfCen/", include("ConfCen.urls")),
    path("TaskCen/", include("TaskCen.urls")),
        path("ProjManage/", include("ProjManage.urls")),

    # path("alarm_analysis/", include("alarm_analysis.urls")),



    path("Doc/", include(("Doc.urls", "Doc"))),
    path("DeployCen/", include(("DeployCen.urls", "DeployCen"))),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # path("api/token/", obtain_auth_token, name="api_token_auth"),
    path("api-jwt-auth/", obtain_jwt_token),
    url(
        r"^uploads/(?P<path>.*)",
        login_required(serve),
        {"document_root": settings.MEDIA_ROOT},
    ),
    path("Webhook/", Webhook),
    

  
]
