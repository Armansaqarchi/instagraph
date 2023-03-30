from django.contrib import admin
from .models import Comment, Post, Like
# Register your models here.



admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Like)