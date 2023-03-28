from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.




class Profile(APIView):
    permission_classes = (IsAuthenticated)
    def get(self, request) -> Response:
        self.check_object_permissions