from rest_framework.permissions import BasePermission
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView
from ..api.serializer import (
    FollowerSerializer,
)
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from ..models import Account
from rest_framework.decorators import renderer_classes
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.generics import GenericAPIView
import logging
from rest_framework.status import(
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_208_ALREADY_REPORTED
)

from rest_framework.request import Request


logger = logging.getLogger(__name__)


class IsFollowerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        
        account_id = request.user.account.id
        if obj.following_set.filter(follower_set = account_id).exists():
            return True
        
        return False
    



class FollowersView(LoginRequiredMixin, ListAPIView):


    def dispatch(self, request, *args, **kwargs):
        
        return super().dispatch(request, *args, **kwargs)

    permission_classes = [IsFollowerPermission]
    serializer_class = FollowerSerializer
    login_url = "accounts/login"
    paginate_by = 20

    def get_queryset(self):
        account = Account.objects.get(pk=self.kwargs['pk'])
        return account.following_set.all()

    def get(self, request) -> Response:
        try:

            
            followers_list = self.get_object()
            serializer = FollowerSerializer(followers_list, many=True)
        except Exception:
            return Response({"status" : "error"}, HTTP_400_BAD_REQUEST)
        return Response({"followers" : serializer.data}, status=HTTP_200_OK)
    

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@api_view(['GET'])
@renderer_classes((JSONRenderer,))
@login_required(login_url="login")
def test(request):
    print(request.user.is_authenticated)
    return HttpResponse({"username" : request.user.is_authenticated})




class FollowRQ(APIView):


    def dispatch(self, request, following_id) -> HttpResponse:
        print(type(request))
        return super().dispatch(request, following_id = following_id)


    # login_url = "accounts/login"

    def get(self, request, following_id) -> Response:
        print(type(request))
        following_user = Account.objects.filter(id = following_id).first()
        
        is_following = following_user.received_set.filter(sender = request.user.account.id).exists()

        if is_following:
            message = f"user {following_user.id} is already being followed"
            return Response({"message" : message, "status" : "error"}, status=HTTP_208_ALREADY_REPORTED)

        if following_user.is_private:
            FollowRQ.objects.create(
                sender = request.user.account.id,
                recipient = following_id,
                is_read = False,
                acceepted = False
            )
            

            logger.info("sent friendly request to user : %s".format(following_user.user.username))
            message = "successfully sent friendly request"
            return Response({"message" : message, "status" : "success"}, status = HTTP_200_OK)
        else:
            message = "strated following %s".format(following_user.user.username)
            logger.info("user %s started following user %s".format(request.user.id, following_id))
            return Response({'message' : message, 'status' : "success"}, status = HTTP_200_OK)