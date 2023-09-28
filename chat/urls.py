from django.urls import re_path
from .chatView import GetMessages, GetChatList, ChatView


urlpatterns = [
    re_path(r"chats/(?P<pk>[\w+-]+)", GetMessages.as_view(), name="chats"),
    re_path(r"list", GetChatList.as_view(), name = "lists"),
    re_path(r"chat", ChatView.as_view())
]