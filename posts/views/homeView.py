from accounts.models import Story 
from accounts.views.FollowViews import IsOwnerPermission
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from ..models import Post
from django.db.models.query import QuerySet
from rest_framework.response import Response
from django.conf import settings
from ..serializer.Homeserializer import PostSerializer, StorySerializer
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.status import (
    HTTP_200_OK,
)
from exceptions.exceptions import *

class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "story_page"
    max_page_size = 1000

class StoryPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "post_page"
    max_page_size = 1000


class HomeView(ListAPIView):
    permission_classes = [IsOwnerPermission, IsAuthenticated]
    login_url = settings.LOGIN_URL
    

    def set_type(self, request):
        if request.GET.get("type") == "post":
            self.pagination_class = PostPagination
            self.serializer_class = PostSerializer
        elif request.GET.get("type") == "story":
            self.pagination_class = StoryPagination
            self.serializer_class = StorySerializer
        else:
            raise BadRequestException("invalid query params format")

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

        self.set_type(request=request)

        account = request.user.account
        following_set = account.follower_set.only("following")

        if self.pagination_class == PostPagination:
            items = self.get_posts(request, followings=following_set)
        else:
            items = self.get_stories(request, followings=following_set)
        items = self.paginate_queryset(items)

        serialized = self.serializer_class(items, many=True).data

        last_seen_post = account.last_seen_posts
        account.last_seen_posts = datetime.now()
        account.save() 

        return Response({"data" : serialized, "status" : "success", "last_seen" : last_seen_post}, status=HTTP_200_OK)
    



        



