from django.conf import settings
from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from .views.asyncView import async_post_get
from .views.homeView import HomeView

TTL = settings.DEFAULT_CACHE_TIMEOUT

urlpatterns = [
    re_path(r"^post_photo", async_post_get, name="post_image"),
    path("home", cache_page(TTL)(HomeView.as_view()), name="home")
]