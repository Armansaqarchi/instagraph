from django.contrib import admin
from .models import Comment, Post, Like, MediaPost, UUIDBasedTag
# Register your models here.



admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(UUIDBasedTag)
admin.site.register(MediaPost)