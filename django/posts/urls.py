from django.conf import settings
from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views.asyncView import AsyncPostGet
from .views.PostView import LikeAPIView, CommentAPIView
from .views.homeView import HomeView

TTL = settings.DEFAULT_CACHE_TIMEOUT

urlpatterns = [
    re_path(r"^post_photo", AsyncPostGet.as_view(), name="post_image"),
    re_path(r"^comments/create/(?P<pk>[\w+-]+)", CommentAPIView.as_view({"post" : "create"})),
    re_path(r"^comments/delete/(?P<pk>[\w+-]+)", CommentAPIView.as_view({"delete" : "destroy"})),
    re_path(r"^comments/list/(?P<pk>[\w+-]+)", CommentAPIView.as_view({"get" : "list"})),
    re_path(r"^comments/edit/(?P<pk>[\w+-]+)", CommentAPIView.as_view({"patch" : "partial_update"})),
    re_path(r"^likes/create/(?P<pk>[\w+-]+)", LikeAPIView.as_view({"get" : "create"})),
    re_path(r"^likes/delete/(?P<pk>[\w+-]+)", LikeAPIView.as_view({"delete" : "destroy"})),
    re_path(r"^likes/list/(?P<pk>[\w+-]+)", LikeAPIView.as_view({"get" : "list"})),
    re_path(r"^likes/retreive/(?P<pk>[\w+-]+)", LikeAPIView.as_view({"get" : "retreive"})),
    path("home", (HomeView.as_view()), name="home")
]