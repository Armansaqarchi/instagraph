from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...accounts.views.FollowViews import OwnerPermission
from datetime import datetime
from ...accounts.models import Account
from ..models import Post
from django.db.models.query import QuerySet
from rest_framework.response import Response
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.conf import settings
from django.views.decorators.cache import cache_page
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN
)

TTL = settings.DEFAULT_CACHE_TIMEOUT
TTL = TTL if TTL else 300

@cache_page(TTL)
class HomeVIew(LoginRequiredMixin, ListAPIView):
    permission_classes = [OwnerPermission]
    login_url = settings.REDIRECT_LOGIN_URL
    paginate_by = 7

    def get_posts(self, request, followings : list):
        posts = QuerySet(model=Post)

        for following in followings:
            posts = posts | following.user_id_set

        return posts.order_by("posted_at")
    

    def get_paginator(self, request, posts):
        try:
            # url params
            page_num = request.GET.get('page')
            paginator = Paginator(posts, self.paginate_by)
        except (PageNotAnInteger,EmptyPage):
            page_num = 1

        return paginator.get_page(page_num)


    def get(self, request, *args, **kwargs):
        account = request.user.account
        # getting the 'follows' instance in which the user is follower
        following_set = account.follower_set.values_list('following')
        posts = self.get_posts(request, followings=following_set)
        new_posts = self.get_paginator(self, request, posts=posts)

        last_seen_post = account.last_seen_post
        account.last_seen_posts = datetime.now()
        account.save() 
        return Response({"status" : "success", "posts" : new_posts, "last_seen" : last_seen_post}, status = HTTP_200_OK)

        

