from django.urls import re_path, path
from .views.asyncView import get_post_image
from .views.homeView import HomeView


urlpatterns = [
    re_path(r"^photo$", get_post_image, name="post_image"),
    path("home", HomeView.as_view(), name="main_page")
]