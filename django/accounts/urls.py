from django.urls import re_path, path
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.conf import settings
from .views.AuthViews import (
    UserProfileView,
    LoginView,
    ProfileView,
    Activate,
)
from .views.FollowViews import(
    FollowersAPIView,
    FollowingListAPIView,
    FollowersListAPIView,
    FollowingAPIView,
    FollowRQListAPIView,
)


urlpatterns = [
    re_path(r"^login", LoginView.as_view(), name = "login"),
    re_path(r"^profile/(?P<pk>[0-9]+)", ProfileView.as_view({"get" : "retrieve", "put" : "update", "delete" : "destroy"}), name = "profile"),
    re_path(r"profile/image/(?P<pk>[0-9]+)", ProfileView.as_view({"patch" : "update_profile_image"})),
    re_path(r"profile", ProfileView.as_view({"get" : "list", "post" : "create"})),
    re_path(r"^follower/requests", FollowRQListAPIView.as_view(), name="followers"),
    re_path(r"^follower/(?P<pk>[\w+-]+)$", FollowersAPIView.as_view({"get" : "accept_or_reject", "delete" : "destroy"}), name="followers"),
    re_path(r"^follower/followers", FollowersListAPIView.as_view(), name="followers"),
    re_path(r"^following/followings", FollowingListAPIView.as_view()),
    re_path(r"^following/(?P<pk>[\w+-]+)", FollowingAPIView.as_view({"get" : "create", "delete" : "destroy"})),
    re_path(r"^activate/(?P<id>.+)[0-9]+/$", Activate.as_view(), name="activate"),
    # re_path(r"^follow_req/(?P<following_id>[0-9]+)$", FriendFollowRQ.as_view(), name= "follow_req"),
    # re_path(r"^accept_req/(?P<RQ_id>[\w+-]+)", AcceptRQ.as_view(), name="accept_req"),
    # re_path(r"^reqList/(?P<id>\d+)$", RQList.as_view(), name="req_list"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
