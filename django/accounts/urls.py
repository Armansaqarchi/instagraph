from django.urls import re_path
from .views import (
    SingleProfileView,
    LoginView,
    SignUpView
)


urlpatterns = [
    re_path(r"^login", LoginView.as_view(), name = "login"),
    re_path(r"^profile/<str:pk>", SingleProfileView.as_view(), name = "profile"),
    re_path(r"^signup", SignUpView.as_view(), name="register")
]