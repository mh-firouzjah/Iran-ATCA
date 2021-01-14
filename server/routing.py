import apps.forum.routing as forum_routing
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            forum_routing.websocket_urlpatterns
        )
    ),
    "*": get_asgi_application(),

})
