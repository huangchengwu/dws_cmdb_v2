from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import * 
from .models import * 
from rest_framework.decorators import action
from dws_cmdb.tasks import *
from rest_framework.response import Response

# Create your views here.
class  ProjdepViewSet(ModelViewSet):
    queryset = Projdep.objects.all()
    serializer_class = ProjdepSerializer
    @action(methods=["put"], detail=True, url_path="TaskEnc_exec")
    def TaskEnc_exec(self, request, *args, **kwargs):
        Id = kwargs["pk"]
        action = request.data["action"]
        version = int(time.time())
        TaskEnc_exec.delay(Id,str(request.user),action,version)
        
        time.sleep(2)
        t=TaskDeploy.objects.get(version=version)
         
        return Response({"msg": "执行成功,请刷新", "status": True,"version" : version,"log_id": t.Id})