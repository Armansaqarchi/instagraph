from django.urls import re_path, path, include



urlpatterns = [
    path("accounts/", include("accounts.urls"))
    path("posts/", include("posts.urls"))
]