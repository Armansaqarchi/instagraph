from django.urls import re_path, path
from django.conf.urls.static import static
from django.conf import settings
from .views.AuthViews import (
    SingleProfileView,
    LoginView,
    SignUpView,
    Activate
)
from .views.FollowViews import(
    FollowersView,
    FollowRQ,
    test
)


urlpatterns = [
    re_path(r"^login", LoginView.as_view(), name = "login"),
    re_path(r"^profile/(?P<pk>[0-9])", SingleProfileView.as_view(), name = "profile"),
    re_path(r"^signup", SignUpView.as_view(), name="register"),
    re_path(r"^followers/(?P<id>.+)/$", FollowersView.as_view(), name="followers"),
    re_path(r"^activate/(?P<id>.+)/$", Activate.as_view(), name="activate"),
    re_path(r"^follow_req/(?P<following_id>[0-9]+)", FollowRQ.as_view(), name= "follow_req"),
    path("test", test, name = "test")
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)