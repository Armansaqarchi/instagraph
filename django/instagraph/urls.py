"""instagraph URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path
from django.urls import include

from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView

)

token = [
    re_path(r'^token$', TokenObtainPairView.as_view(), name = "token_obtain_pair"),
    re_path(r'^token/refresh$', TokenRefreshView.as_view(), name = "token_refresh"),
    re_path(r'^token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include(token)),
    re_path(r'test', include('posts.urls')),
    re_path(r'accounts/', include('accounts.urls'))
    
]


