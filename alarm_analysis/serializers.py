from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers

 
class AlertGroupSerializer(ModelSerializer):
    class Meta:
        model = AlertGroup
        fields = '__all__'
