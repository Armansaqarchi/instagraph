from django.urls import re_path, path
from django.conf.urls.static import static
from django.conf import settings
from .views.AuthViews import (
    UserProfileView,
    LoginView,
    ProfileView,
    Activate,
)
from .views.FollowViews import(
    FollowersView,
    FriendFollowRQ,
    AcceptRQ,
    FollowingList,
    RQList
)
from django.views.generic import TemplateView


urlpatterns = [
    re_path(r"^login", LoginView.as_view(), name = "login"),
    re_path(r"^profile/(?P<pk>[0-9]+)", UserProfileView.as_view(), name = "profile"),
    re_path(r"^signup", ProfileView.as_view(), name="register"),
    re_path(r"^followers/(?P<id>[0-9]+)$", FollowersView.as_view(), name="followers"),
    re_path(r"^activate/(?P<id>.+)[0-9]+/$", Activate.as_view(), name="activate"),
    re_path(r"^follow_req/(?P<following_id>[0-9]+)$", FriendFollowRQ.as_view(), name= "follow_req"),
    re_path(r"^accept_req/(?P<RQ_id>[\w+-]+)", AcceptRQ.as_view(), name="accept_req"),
    re_path(r"^followings/(?P<id>\d+)", FollowingList.as_view(), name = "followings"),
    re_path(r"^reqList/(?P<id>\d+)$", RQList.as_view(), name="req_list"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
