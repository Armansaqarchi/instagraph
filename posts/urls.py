from django.urls import re_path
from .views import testView



urlpatterns = [
    re_path(r'test', testView.as_view(), name = "test")
]