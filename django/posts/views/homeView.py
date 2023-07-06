from accounts.models import Story 
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
from ..serializer.Homeserializer import PostSerializer, StorySerializer
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN
)

class HomeView(LoginRequiredMixin, ListAPIView):
    permission_classes = [OwnerPermission]
    login_url = settings.LOGIN_URL
    post_paginate_by = 10
    story_paginate_by = 5

    def get_posts(self, request, followings : list):
        posts = QuerySet(model=Post)
        for following in followings:
            posts = posts | following.user_posts.all()

        return posts.order_by("created_at")
    
    def get_stories(self, request, followings : list):
        stories = QuerySet(model=Story)
        for following in followings:
            stories = stories | following.account_story.all()
        
        return stories.order_by("created_at")

    def get_paginator(self, request, items, lookup_propery):
        try:
            # url params
            page_num = int(request.GET.get(lookup_propery))
            if lookup_propery == "posts_slide":
                serializerClass = PostSerializer
                pagiante_by = 10
            else:
                serializerClass = StorySerializer
                pagiante_by = 5

            paginator = Paginator(items, pagiante_by)
        except (PageNotAnInteger,EmptyPage):
            page_num = 1


        items = paginator.get_page(page_num)
        items_serialized = serializerClass(items, many = True)
        return items_serialized


    def get(self, request):
        account = request.user.account
        following_set = account.follower_set.values_list('following', flat = True)

        new_posts, new_stories = None, None
        
        if request.GET.get("posts_slide") is not None:
            posts = self.get_posts(request, followings=following_set)
            new_posts = self.get_paginator(request, posts, "posts_slide").data
            
        if request.GET.get("stories_slide") is not None:
            stories = self.get_stories(request, followings=following_set)
            new_stories = self.get_paginator(request, stories, "stories_slide").data

        last_seen_post = account.last_seen_posts
        account.last_seen_posts = datetime.now()
        account.save() 

        return Response({"status" : "success", "posts" : new_posts, "stories" : new_stories, "last_seen" : last_seen_post}, status = HTTP_200_OK)

        



