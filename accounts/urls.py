from django.urls import re_path, path
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from django.conf import settings
from accounts.graphql.schema import schema
from accounts.graphql.graphql import GraphAuthorizedView
from .views.AuthViews import (
    LoginView,
    ProfileView,
    ActivationCode,
    PasswordResetAPIView,
    GoogleLoginApi
)
from .views.FollowViews import(
    FollowersAPIView,
    FollowingsListAPIView,
    FollowersListAPIView,
    FollowingsAPIView,
    FollowRQListAPIView,
)


urlpatterns = [
    re_path(r"^login", LoginView.as_view(), name = "login"),
    re_path(r"profile/forgot_password/", PasswordResetAPIView.as_view({"post" : "forgot_reset_pass"})),
    re_path(r"profile/confirm_password/(?P<email>.*)", PasswordResetAPIView.as_view({"post" : "confirm_reset_pass_otp"})),
    re_path(r"profile/reset_password/", PasswordResetAPIView.as_view({"post" : "reset_pass"})),
    re_path(r"^profile/(?P<pk>[0-9]+)", ProfileView.as_view({"get" : "retrieve", "patch" : "update", "delete" : "destroy"}), name = "profile"),
    re_path(r"profile/activation/(?P<pk>[0-9]+)", ActivationCode.as_view()),
    re_path(r"profile/image/(?P<pk>[0-9]+)", ProfileView.as_view({"patch" : "update_profile_image"})),
    re_path(r"profile", ProfileView.as_view({"post" : "create"})),
    re_path(r"^follower/requests", FollowRQListAPIView.as_view(), name="followers"),
    re_path(r"^follower/followers", FollowersListAPIView.as_view(), name="followers"),
    re_path(r"^follower/(?P<pk>[\w+-]+)$", FollowersAPIView.as_view({"get" : "accept_or_reject", "delete" : "destroy"}), name="followers"),
    re_path(r"^following/followings", FollowingsListAPIView.as_view()),
    re_path(r"^following/(?P<pk>[\w+-]+)", FollowingsAPIView.as_view({"get" : "create", "delete" : "destroy"})),
    re_path(r"^google", GoogleLoginApi.as_view()),
    path("graphql", GraphAuthorizedView.as_view(graphiql = True, schema = schema))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
