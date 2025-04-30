from rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers



class ProjdepSerializer(ModelSerializer):
    class Meta:
        model = Projdep
        fields = '__all__'
