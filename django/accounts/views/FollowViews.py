from typing import Any
from django import http
from django.http.response import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView
from ..api.serializer import (
    FollowingSerializer,
    FollowerSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.exceptions import PermissionDenied
from django.db import IntegrityError
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..models import Follows, FollowRQ
from ..permissions import *
from rest_framework.views import APIView
from ..models import Account
from rest_framework.response import Response
import logging
from ..api.serializer import FollowingSerializer, FollowRequestSerializer
from django.shortcuts import get_object_or_404
from rest_framework.status import(
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)
import traceback
from django.conf import settings
from rest_framework.request import Request
from exceptions.exceptions import *

logger = logging.getLogger(__name__)


class FollowersAPIView(ModelViewSet, GenericAPIView):

    class FollowerPaginator(PageNumberPagination):
        page_query_param = "page"
        page_size = 30


    pagination_class = FollowerPaginator
    errors = {
        "forbidden" : "Access Denied",
        "no_such_fr" : "No such friend request",
        "already_follows" : "The user is already following you"
    }
    
    def get_queryset(self):
        """
        returns queryset based on http method provided in request header
        """
        QUERYSET_CASES = {
            "get" : Account,
            "delete" : Follows,
            "post" : FollowRQ
        }
        return QUERYSET_CASES[self.request.method.lower()]
    

    def filter_queryset(self, id):
        account = self.get_object(self.get_queryset(), id = id)
        followings_id = account.following_list.values_list('follower', flat = True)
        return account, Account.objects.filter(id__in = followings_id)     


    def list(self, id):
        try:
            account, queryset = self.filter_queryset(id)
            page = self.paginate_queryset(queryset=queryset)
            serializer = self.serializer_class(page, many=True)
            followers_count = account.followers_list
            return Response({"Message" : "follower page is ready", "page_obj" : serializer.data, "followers_number" : followers_count,
                              "Status" : "success", "Code" : "page_is_up"}, status=HTTP_200_OK)
        except PermissionDenied:
            raise ForibiddenException(self.errors["forbidden"], code = "permission_denied")
        
    def destroy(self, request, id):
        self.queryset = Follows.objects.all()
        follow = self.get_object()
        self.perform_destroy(follow)
        return Response({"Message" : "follower removed", "Code" : "follower_remove", "Status" : "Success"},
                         status=HTTP_204_NO_CONTENT)

    def create(self, request, id):
        self.queryset = FollowRQ.objects.all()
        try:
            fr = self.get_object()
        except Http404:
            raise NotFoundException(self.errors["no_such_fr"], code="fr_not_found")
        already_follows = Follows.objects.filter(Q(follower__id = fr.sender.id) & Q(following__id = fr.receiver.id)).exists()
        if already_follows:
            raise AlreadyExistsException(self.errors["already_follow"])
        Follows.objects.create(
            follower = fr.sender,
            following = fr.receiver
        )
        return Response({"Message" : "follow request accepted", "Status" : "Success", "Code" : "following_done"},
                         status=HTTP_200_OK)



        


class FollowingList(ListAPIView):

    permission_classes = [IsFollowerPermission]
    paginate_by = 20
    login_url = settings.LOGIN_REDIRECT_URL

    def dispatch(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().dispatch(request, *args, **kwargs)

    def get_page(self, request, object_list):
        paginator = Paginator(object_list, self.paginate_by)
        page_num = request.GET.get('page')
        if not page_num:
            page_num = 1
        return paginator.get_page(page_num)

    def get_queryset(self, id):
        account = get_object_or_404(Account, id=id)
        followings_id = account.follower_set.values_list('following', flat = True)
        return Account.objects.filter(id__in = followings_id)

    def get(self, request, id):
        try:
            account = get_object_or_404(Account, id=id)
            self.check_object_permissions(request, account)
            page_objs = self.get_page(request, self.get_queryset(id=id)).object_list
            serializer = FollowingSerializer(page_objs, many=True)
            following_count = account.follower_set.count()
            return Response({"Message" : "following page is ready", "page_obj" : serializer.data,
                              "followings_number" : following_count, "Status" : "success", "Code": "page_is_up"}, status=HTTP_200_OK)
        except PermissionDenied:
            raise ForibiddenException("Access denied to reach this page")

    
class FriendFollowRQ(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, following_id) -> Response:


        to_user = Account.objects.filter(id = following_id).first()

        if to_user is None:
            raise NotFoundException("user id %s does not exists" %following_id)
        
        has_requested = to_user.received_set.filter(sender = request.user.account.id).exists()
        if has_requested:
            raise AlreadyExistsException("you have already sent follow request to user %s" %to_user.user.username, code= "already_requested")
        sender = request.user.account
        is_following = sender.follower_set.filter(following = following_id)

        if is_following:
            message = f"user {to_user.id} is already being followed"
            raise AlreadyExistsException("You are already following user %s" %to_user.user.username, "already_following")
        try:

            if to_user.is_private:
                FollowRQ.objects.create(
                    sender = sender,
                    recipient = to_user,
                    is_read = False,
                    accepted = False
                )

                logger.info("sent friendly request to user : %s".format(to_user.user.username))

                message = "successfully sent follow request"
                return Response({"Message" : message, "Status" : "success", "Code" : "folliw_req_send"}, status = HTTP_200_OK)
            else:
                following_acc = Account.objects.get(id = following_id)
                Follows.objects.create(
                    follower = request.user.account,
                    following = following_acc
                )
                message = "strated following %s" %to_user.user.username
                logger.info("user %s started following user %s".format(request.user.id, following_id))
                return Response({'Message' : message, 'Status' : "success", "Code": "follow_req"}, status = HTTP_200_OK)
        except IntegrityError as e:
            raise BadRequestException("Bad request", "constraint_violation")

class AcceptRQ(APIView):

    permission_classes = [IsOwnerPermission]
    login_url = settings.LOGIN_URL

    def get(self, request, RQ_id) -> Response:
        """
        given RQ_id, accepts the friend reqeust corresponding to the RQ_id
        """
        try:
            fr_req = FollowRQ.objects.get(id = RQ_id)
        except FollowRQ.DoesNotExist:
            raise NotFoundException("No such request", code="invalid id")
        except ValidationError:
            raise BadRequestException("invalid uuid number or request is not valid", code="invalid format")
        self.check_object_permissions(request=request, obj=fr_req.recipient)
        if fr_req is not None:
            has_followed = Follows.objects.filter(Q(follower = fr_req.sender) & Q(following = fr_req.recipient)).exists()
            if not has_followed:
                with transaction.atomic():
                    follower_user = fr_req.sender
                    following_user = fr_req.recipient
                    Follows.objects.get_or_create(
                        follower = follower_user,
                        following = following_user
                    )
                    fr_req.delete()
                return Response({"Message" : f"accepted {follower_user} request",
                                  "Status" : "success", "Code": "request_accepted"}, status=HTTP_200_OK)

            raise AlreadyExistsException("user is already following you", code= "already_following")
        
        raise BadRequestException("no such following request exists", code= "no_such_user")
    

class RQList(LoginRequiredMixin, ListAPIView):
    permission_classes = [IsOwnerPermission]
    paginate_by = 20
    login_url = settings.LOGIN_REDIRECT_URL


    def get(self, request, id) -> Response:
        """
        returns list of friend requset
        """
        try:
            RQ_list = FollowRQ.objects.filter(recipient = id)
            account = Account.objects.get(id = id)
            self.check_object_permissions(request, obj=account)
            serialized = FollowRequestSerializer(RQ_list, many = True)

            return Response({"Message" : "requests are retrieved successfully", "Status" : "success",
                              "Code" : "follow_req_are_returned", "requests" : serialized.data}, status = HTTP_200_OK)
        except ValueError:
            raise BadRequestException("Bad or incorrect credentials", code= "incorrect_credentials")

