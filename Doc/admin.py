from django.contrib import admin
from .models import *


@admin.register(HelpDocuments)
class HostConfigAdmin(admin.ModelAdmin):
    list_display = ('Id','title') # list
    
    search_fields = ('Id','title') # list


    exclude = []
 



