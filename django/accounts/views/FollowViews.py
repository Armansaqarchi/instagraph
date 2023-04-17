from rest_framework.permissions import BasePermission
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView
from ..api.serializer import (
    FollowerSerializer,
)
from ..models import Account
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
import logging
from rest_framework.status import(
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_208_ALREADY_REPORTED
)


logger = logging.getLogger(__name__)


class IsFollowerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        
        account_id = request.user.account.id
        if obj.following_set.filter(follower_set = account_id).exists():
            return True
        
        return False
    



class FollowersView(LoginRequiredMixin, ListAPIView):

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
    


class FollowRQ(LoginRequiredMixin, GenericAPIView):
    login_url = "accounts/login"

    def post(self, request, following_id) -> Response:
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$", request.user.is_authenticated)
        following_user = Account.objects.filter(id = following_id).first()

        is_following = following_user.received_set.filter(sender = request.user.account.id)

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