from channels.routing import ProtocolTypeRouter
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import TaskCen.routing

# 设置默认路由在项目创建routing.py文件
application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            TaskCen.routing.websocket_urlpatterns
        )
    ),
})