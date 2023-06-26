from django.urls import re_path, path
from .views.asyncView import get_post_image
from .views.homeView import HomeView
from django.conf import settings
from django.views.decorators.cache import cache_page

TTL = settings.DEFAULT_CACHE_TIMEOUT

urlpatterns = [
    re_path(r"^photo$", get_post_image, name="post_image"),
    path("home", cache_page(TTL)(HomeView.as_view()), name="main_page")
]