import os
from django.conf.urls import url
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trunk_player.settings")
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from radio.consumers import RadioConsumer

channel_layer = ProtocolTypeRouter({
    "http": django_asgi_app,

    # WebSocket chat handler
    "websocket": AuthMiddlewareStack(
        URLRouter([
            url(r"^ws-calls/(?P<tg_type>[^/]+)/(?P<label>[^/]+)", RadioConsumer.as_asgi()),
            url(r"^ws-calls/(?P<tg_type>[^/]+)/$", RadioConsumer.as_asgi()),
            url(r"^ws-calls/$", RadioConsumer.as_asgi())
        ])
    ),
})