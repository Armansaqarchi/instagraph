from typing import Any
from django import http
from django.http.response import HttpResponse
from rest_framework.generics import ListAPIView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.views.FollowViews import OwnerPermission
from datetime import datetime
from ..models import Post
from django.db.models.query import QuerySet
from rest_framework.response import Response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.views.decorators.cache import cache_page
from ..serializer.post_serializer import PostSerializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN
)

class HomeView(LoginRequiredMixin, ListAPIView):
    permission_classes = [OwnerPermission]
    login_url = settings.LOGIN_URL
    paginate_by = 7


    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get_posts(self, request, followings : list):
        posts = QuerySet(model=Post)
        for following in followings:
            print(following.user_posts)
            posts = posts | following.user_posts

        return posts.order_by("created_at")
    
    # def get_stories(self, request, followings : list):
    #     stories = QuerySet()
    #     for following in followings:


    

    def get_paginator(self, request, posts):
        try:
            # url params
            page_num = request.GET.get('page')
            paginator = Paginator(posts, self.paginate_by)
        except (PageNotAnInteger,EmptyPage):
            page_num = 1

        pages = paginator.get_page(page_num)
        pages_serialized = PostSerializer(pages, many = True)
        return pages_serialized



    def get(self, request):
        account = request.user.account
        following_set = account.follower_set.values_list('following', flat = True)
        
        posts = self.get_posts(request, followings=following_set)
        new_posts = self.get_paginator(request, posts)

        last_seen_post = account.last_seen_posts
        account.last_seen_posts = datetime.now()
        account.save() 
        return Response({"status" : "success", "posts" : new_posts.data, "last_seen" : last_seen_post}, status = HTTP_200_OK)

        



