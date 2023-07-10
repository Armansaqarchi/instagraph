from django.contrib import admin
from chat.models import PostMessage, TextMessage

# Register your models here.

admin.site.register(TextMessage)
admin.site.register(PostMessage)
