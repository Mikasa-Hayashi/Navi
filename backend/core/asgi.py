"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os

from chat.routing import ws_urlpatterns
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django_asgi_application = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_application,
    'websocket': AuthMiddlewareStack(
        URLRouter(ws_urlpatterns)
    )
})
