from typing import Any
from django import http
from accounts.models import Story 
from django.http.response import HttpResponse
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.views.FollowViews import OwnerPermission
from datetime import datetime
from ..models import Post
from django.db.models.query import QuerySet
from rest_framework.response import Response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.views.decorators.cache import cache_page
from ..serializer.Homeserializer import PostSerializer, StorySerializer
from rest_framework.generics import ListAPIView
from rest_framework.pagination import CursorPagination
from rest_framework.status import (
    HTTP_200_OK,
)
from accounts.exceptions.Exceptions import *

class PostPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'
    max_page_size=100

class StoryPagination(CursorPagination):
    page_size = 5
    ordering = '-created_at'
    max_page_size=100

class HomeView(ListAPIView):
    permission_classes = [OwnerPermission]
    login_url = settings.LOGIN_URL
    

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get("post_page"):
            self.pagination_class = PostPagination
            self.serializer_class = PostSerializer
        elif request.GET.get("story_page"):
            self.pagination_class = StoryPagination
            self.serializer_class = StorySerializer
        else:
            raise BadRequestException("invalid query params format")
        return super().dispatch(request, *args, **kwargs)    

    def get_posts(self, request, followings : list):
        posts = QuerySet(model=Post)
        for item in followings:
            posts = posts | item.following.user_posts.all()

        return posts.order_by("created_at")
    
    def get_stories(self, request, followings : list):
        stories = QuerySet(model=Story)
        for item in followings:
            stories = stories | item.following.account_stories.all()
        
        return stories.order_by("created_at")


    def get(self, request):
        account = request.user.account
        following_set = account.follower_set.only("following")

        if self.pagination_class == PostPagination:
            items = self.get_posts(request, followings=following_set)
            cursor_string = request.GET.get("post_page")
        else:
            items = self.get_stories(request, followings=following_set)
            cursor_string = request.GET.get("post_page")
        items = self.paginate_queryset(items)

        serialized = self.serializer_class(items, many=True).data

        last_seen_post = account.last_seen_posts
        account.last_seen_posts = datetime.now()
        account.save() 

        return self.get_paginated_response({"data" : serialized, "status" : "success", "last_seen" : last_seen_post})


        



