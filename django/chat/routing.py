from django.urls import path
from .consumers import *


websocket_urlpatterns = [
    path("chat/", ChatConsumer.as_asgi())
]