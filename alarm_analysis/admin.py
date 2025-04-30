from django.contrib import admin
from django import forms
from django.shortcuts import render, HttpResponse, redirect
from jinja2 import Template
from django.utils.html import format_html
from django_ace import AceWidget
import string
import secrets
import urllib.parse
import time
from django.http import HttpResponseRedirect
import base64
import re
from dws_cmdb.tasks import *
import requests
from alarm_analysis.models import * 
class AlertGroupForm(forms.ModelForm):
    message = forms.CharField(
        widget=AceWidget(mode="sh", theme="twilight", width="1000px", height="500px"),
        label="ai分析内容"   

    )

    class Meta:
        model = AlertGroup
        exclude = []

# Register your models here.
@admin.register(AlertGroup)
class AlertGroupAdmin(admin.ModelAdmin):


    form = AlertGroupForm

 
@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
     
    # list_display = (
    #     "Id",
    #     "message",
    #     "timestamp"
    # )  
    
    def changelist_view(self, request, extra_context=None):
        context = {}
        # froms = ProjdepForm
        if request.method == "POST":
            print("报警信息")

            return render(request, "custom/alarm_analysis.html", context=context)

        return render(request, "custom/alarm_analysis.html", context=context)
