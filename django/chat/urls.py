from django.urls import re_path
from .ChatView import GetMessages


urlpatterns = [
    re_path(r"/chats/(?P<id>[0-9]+)", GetMessages.as_view(), name="chats")
]