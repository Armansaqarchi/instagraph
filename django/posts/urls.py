from django.conf import settings
from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views.asyncView import AsyncPostGet
from .views.homeView import HomeView

TTL = settings.DEFAULT_CACHE_TIMEOUT

urlpatterns = [
    re_path(r"^post_photo", AsyncPostGet.as_view(), name="post_image"),
    path("home", (HomeView.as_view()), name="home")
]