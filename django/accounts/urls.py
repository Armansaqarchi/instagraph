from django.urls import re_path
from .views import SingleProfileView, LoginView


urlpatterns = [
    re_path(r"^login/", LoginView.as_view(), name = "login"),
    re_path(r"^Profile/<str:pk>", SingleProfileView.as_view(), name = "profile")
]