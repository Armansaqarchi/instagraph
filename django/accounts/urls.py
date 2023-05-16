from django.urls import re_path, path
from django.conf.urls.static import static
from django.conf import settings
from .views.AuthViews import (
    SingleProfileView,
    LoginView,
    SignUpView,
    Activate,
)
from .views.FollowViews import(
    FollowersView,
    FollowRQ,
    AcceptRQ,
    FollowingList,
)


urlpatterns = [
    re_path(r"^login", LoginView.as_view(), name = "login"),
    re_path(r"^profile/(?P<pk>[0-9])", SingleProfileView.as_view(), name = "profile"),
    re_path(r"^signup", SignUpView.as_view(), name="register"),
    re_path(r"^followers/(?P<id>[0-9]+)$", FollowersView.as_view(), name="followers"),
    re_path(r"^activate/(?P<id>.+)/$", Activate.as_view(), name="activate"),
    re_path(r"^follow_req/(?P<following_id>[0-9]+)$", FollowRQ.as_view(), name= "follow_req"),
    re_path(r"^accept_req/(?P<follower>)", AcceptRQ.as_view(), name="accept_req"),
    re_path(r"^followings/(?P<id>\d+)", FollowingList.as_view(), name = "followings")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)