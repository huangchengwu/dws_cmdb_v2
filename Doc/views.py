from django.shortcuts import render
from ConfCen.models import TaskCreate
from .models import *
import markdown




def show_help(request):
    context = {}
    Id = request.GET.get("Id")

    try:
        title = TaskCreate.objects.get(Id=Id).help.title

        objects = HelpDocuments.objects.get(title=title)
        context["objects"] = objects
        context["content_html"] = markdown.markdown(objects.content)

    except:
        context["objects"] = {}

    print("查看文档", context)

    return render(request, "custom/show_help.html", context)
