from django.urls import re_path
from .consumers import ChatConsumer

ws_urlpatterns = [
    re_path(r'^ws/(?P<conversation_id>[0-9a-f-]{36})/send_message/$', ChatConsumer.as_asgi())
]