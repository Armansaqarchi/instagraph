from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.




class testView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request) -> Response:
        return Response({"message" : "this is just a test"})