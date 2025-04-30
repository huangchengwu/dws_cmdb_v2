from django.conf.urls import url
from .views import *
from .serializers import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="API")


router = DefaultRouter()
router.register(r"k8s_Env", k8s_EnvViewSet)
router.register(r"HostConfig", HostConfigViewSet)
router.register(r"HostGroup", HostGroupViewSet)

router.register(r"TaskEnc", TaskEncViewSet)


router.register(r"Webhook", WebhookViewSet)
router.register(r"Custom_Env", Custom_EnvViewSet)
router.register(r"web_monitor", web_monitorViewSet)

router.register(r"Pipeline", PipelineViewSet)


 


urlpatterns = [
    #   path('helm_import/', helm_import.as_view()),
    path("sharedVariable/", sharedVariable.as_view()),
]
urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中
