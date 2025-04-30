from django.urls import re_path

from TaskCen import   views


websocket_urlpatterns = [
    re_path(r"ws/TaskCen/(?P<Id>\w+)/$", views.ChatConsumer),
       
    # re_path(r'ws/TaskCen/(?P<Id>\w+)/$', views.AsyncConsumer),  # 异步
]


# http://127.0.0.1/DeployCen/show_log/?job_name=1699582268-%E6%89%93%E5%8D%B0%E5%BD%93%E5%89%8D%E6%97%B6%E9%97%B4&job_id=18