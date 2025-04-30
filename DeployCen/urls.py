from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from .serializers import *
from django.conf.urls import url

schema_view = get_swagger_view(title="API")
router = DefaultRouter()
router.register(r"TaskDeploy", TaskDeployViewSet)

router.register(r"TaskCreate", TaskCreateViewSet)

urlpatterns = [
    # path("deploy_app/", deployApp.as_view()),
    # path("taskExec/", taskExec.as_view()),
    # path("show_task/", show_task, name="show_task"),

        path("show_task/", show_task, name="show_task"),
      
     path("show_log/", show_log, name="show_log"),

        path("exec_cmd/", exec_cmd, name="exec_cmd"),

    path("show_work_dir/", show_work_dir, name="show_work_dir"),

    
    path("show_work_dir/<path:path>/", file_detail, name="file_detail"),

    # path("download/", download_local_file, name="download"),
       path("Download/", Download.as_view()),

]




urlpatterns += router.urls  # 将路由器中的所以路由信息追到到django的路由列表中
