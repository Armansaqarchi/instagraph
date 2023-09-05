from django.contrib import admin
from chat.models.messageModel import PostMessage, TextMessage
from chat.models.chatModel import PrivateChat, GroupChat, Chat

# Register your models here.

admin.site.register(TextMessage)
admin.site.register(PostMessage)
admin.site.register(PrivateChat)
admin.site.register(GroupChat)
admin.site.register(Chat)
