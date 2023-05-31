from django.urls import re_path
from .views.asyncView import get_post_image



urlpatterns = [
    re_path(r"^photo$", get_post_image ,name="post_image")
]