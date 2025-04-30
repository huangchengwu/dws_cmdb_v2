from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers

class DownloadSerializer(serializers.Serializer):
    name = serializers.CharField()

    class Meta:
        fields = "__all__"


class TaskDeploySerializer(ModelSerializer):
    class Meta:
        model = TaskDeploy
        fields = '__all__'




class TaskCreateSerializer(ModelSerializer):
    class Meta:
        model = TaskCreate
        fields = '__all__'
