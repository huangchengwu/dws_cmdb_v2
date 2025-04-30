
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from .serializers import *
from django.conf.urls import url

schema_view = get_swagger_view(title="API")
router = DefaultRouter()
router.register(r"Projdep", ProjdepViewSet)
urlpatterns = []
urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中

