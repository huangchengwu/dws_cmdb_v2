from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers

class k8s_EnvSerializer(ModelSerializer):
    class Meta:
        model = k8s_Env
        fields = '__all__'



class web_monitorSerializer(ModelSerializer):
    class Meta:
        model = web_monitor
        fields = '__all__'


class PipelineSerializer(ModelSerializer):
    class Meta:
        model = Pipeline
        fields = '__all__'



class  TaskEncSerializer(ModelSerializer):
    class Meta:
        model = TaskEnc
        fields = '__all__'




class HostConfigSerializer(ModelSerializer):
    class Meta:
        model = HostConfig
        fields = '__all__'




class WebhookSerializer(ModelSerializer):
    class Meta:
        model = Webhook
        fields = '__all__'


class HostGroupSerializer(ModelSerializer):
    class Meta:
        model = HostGroup
        fields = '__all__'


class Custom_EnvSerializer(ModelSerializer):
    class Meta:
        model = Custom_Env
        fields = '__all__'


