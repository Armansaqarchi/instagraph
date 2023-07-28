from django.urls import path
from .consumers import *


websocket_urlpatterns = [
    path("/ws", ChatConsumer.as_asgi())
]