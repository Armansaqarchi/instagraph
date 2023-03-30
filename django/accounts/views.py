from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from .models import Account
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.conf import settings
from api.serializer import AccountSerializer
from rest_framework.status import(
    HTTP_200_OK,
    HTTP_404_NOT_FOUND
)



class SingleProfileView(LoginRequiredMixin, DetailView, APIView):

    model = Account
    login_url = "accounts/login"
    template_name = '/singleProfile.html'


    def has_owner_permission

    
    def get(self, request) -> Response:
        query_set = self.get_queryset()
        try:
            account = self.get_object(queryset=query_set)
            serializer = AccountSerializer(data=request.data)
            #sending json response containing the Account info, use 'Account' to access it
            return Response({"Account" : serializer}, status=HTTP_200_OK)
        except Account.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)


class LoginView()