"""
ASGI config for dws_cmdb project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application
# import django
# from channels.routing import get_default_application
# import TaskCen.routing

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dws_cmdb.settings")
# django.setup()

# # application = get_asgi_application()
# application = get_default_application()


import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import TaskCen.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

application = ProtocolTypeRouter(
    {
        # http请求使用这个
        "http": get_asgi_application(),
        # websocket请求使用这个
        "websocket": AuthMiddlewareStack(
            URLRouter(TaskCen.routing.websocket_urlpatterns)
        ),
    }
)
