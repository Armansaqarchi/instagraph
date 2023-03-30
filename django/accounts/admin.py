from django.contrib import admin
from .models import Post, Story, Comment, Like
# Register your models here.


admin.site.register(Post)
admin.site.register(Story)
admin.site.register(Comment)
admin.site.register(Like)