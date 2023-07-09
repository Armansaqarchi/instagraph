from typing import Any
from django import http
from django.http.response import HttpResponse
from rest_framework.permissions import BasePermission
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import ListAPIView
from ..api.serializer import (
    FollowingSerializer,
    FollowerSerializer
)
from django.db import transaction
from rest_framework.exceptions import PermissionDenied
from django.db import IntegrityError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.db.models import Q
from ..models import Follows, FollowRQ
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from ..models import Account
from rest_framework.response import Response
import logging
from ..api.serializer import FollowingSerializer, FollowRequestSerializer
from django.shortcuts import get_object_or_404
from rest_framework.status import(
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_208_ALREADY_REPORTED,
    HTTP_403_FORBIDDEN
)
import traceback
from django.conf import settings
from rest_framework.request import Request


logger = logging.getLogger(__name__)


class IsFollowerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        account_id = request.user.account.id
        if obj.following_set.filter(follower = account_id).exists():
            return True
        
        return False
    
class OwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return True if obj.id == request.user.account.id else False



class FollowersView(LoginRequiredMixin, ListAPIView):

    permission_classes = [IsFollowerPermission]
    login_url = "accounts/login"
    paginate_by = 20

        
    def get_queryset(self, id):
        account = get_object_or_404(Account, id=id)
        followings_id = account.following_set.values_list('follower', flat = True)
        return Account.objects.filter(id__in = followings_id)
       
    def get_paginator(self, request, id):
        try:
            items = self.get_queryset(self, id)
            paginator = Paginator(items, self.paginate_by)
            #getting page num from url params
            page_num = request.GET["page"]
        except (PageNotAnInteger, EmptyPage):
            page_num = 1

        page_obj = paginator.get_page(page_num)
        return page_obj
        

    def get(self, request, id):
        try:
            account = get_object_or_404(Account, id=id)
            self.check_object_permissions(request, account)
            page_objs = self.get_page(request, self.get_queryset(id=id)).object_list
            serializer = FollowerSerializer(page_objs, many=True)


            followers_count = account.following_set.count()


            return Response({"page_obj" : serializer.data, "followers_number" : followers_count, "status" : "success"}, status=HTTP_200_OK)
        except PermissionDenied as e:
            return Response({"message" : "access denied", "status" : "error"}, status=HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"status" : "error", "message" : str(e)}, HTTP_400_BAD_REQUEST)


class FollowingList(LoginRequiredMixin, ListAPIView):

    permission_classes = [IsFollowerPermission]
    paginate_by = 20
    login_url = settings.LOGIN_REDIRECT_URL


    def get_page(self, request, object_list):
        try:
            paginator = Paginator(object_list, self.paginate_by)
            page_num = request.GET.get('page')
        except Exception as e:
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

            return Response({"page_obj" : serializer.data, "followings_number" : following_count, "status" : "success"}, status=HTTP_200_OK)
        except PermissionDenied:
            return Response({"message" : "access denied", "status" : "error"}, status=HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"status" : "error", "message" : str(e)}, HTTP_400_BAD_REQUEST)
        

    
class FriendFollowRQ(LoginRequiredMixin, APIView):
        

    def get(self, request, following_id) -> Response:


        following_user = Account.objects.filter(id = following_id).first()

        if following_user is None:
            return Response({"message" : f"no user id : {following_id}"}, status=HTTP_400_BAD_REQUEST)
        
        has_requested = following_user.received_set.filter(sender = request.user.account.id).exists()
        if has_requested:
            message = f"user {following_user.id} is already being followed"
            return Response({"message" : message, "status" : "false"}, status=HTTP_403_FORBIDDEN)

        sender = request.user.account
        is_following = sender.follower_set.filter(following = following_id)

        if is_following:
            message = f"user {following_user.id} is already being followed"
            return Response({"message" : message, "status" : "error"}, status=HTTP_208_ALREADY_REPORTED)
        try:

            recipient = get_object_or_404(Account, id = following_id)

            if following_user.is_private:
                FollowRQ.objects.create(
                    sender = sender,
                    recipient = recipient,
                    is_read = False,
                    accepted = False
                )

                logger.info("sent friendly request to user : %s".format(following_user.user.username))
                message = "successfully sent friendly request"
                return Response({"message" : message, "status" : "success"}, status = HTTP_200_OK)
            else:
                following_acc = Account.objects.get(id = following_id)
                Follows.objects.create(
                    follower = request.user.account,
                    following = following_acc
                )
                message = "strated following %s".format(following_user.user.username)
                logger.info("user %s started following user %s".format(request.user.id, following_id))
                return Response({'message' : message, 'status' : "success"}, status = HTTP_200_OK)
        except IntegrityError as e:
            message = f"error has occured during the process : {e}"
            return Response({"message" : message, "status" : "error"}, status=HTTP_400_BAD_REQUEST)

class AcceptRQ(LoginRequiredMixin, APIView):
    

    permission_classes = [OwnerPermission]
    login_url = settings.LOGIN_URL

    
    def get(self, request, RQ_id) -> Response:
        """
        given RQ_id, accepts the friend reqeust corresponding to the RQ_id
        """
        is_requested = FollowRQ.objects.filter(id = RQ_id).first()
       
        if is_requested is not None:

            has_followed = Follows.objects.filter(Q(follower = is_requested.sender) & Q(following = is_requested.recipient)).exists()
            if not has_followed:
                with transaction.atomic():
                    follower_user = is_requested.sender
                    following_user = is_requested.recipient
                    Follows.objects.get_or_create(
                        follower = follower_user,
                        following = following_user
                    )
                    is_requested.delete()
                return Response({"message" : f"accepted {follower_user} request", "status" : "success"}, status=HTTP_200_OK)

            return Response({"message" : "sender is already following you", "status" : "error"}, status=HTTP_403_FORBIDDEN)
        
        return Response({"message" : "no friend request with these details to accept", "status" : "error"}, status=HTTP_403_FORBIDDEN)
    

class RQList(LoginRequiredMixin, ListAPIView):
    permission_classes = [OwnerPermission]
    paginate_by = 20
    login_url = settings.LOGIN_REDIRECT_URL


    def get(self, request, id) -> Response:
        """
        returns list of friend requset
        """
        try:
            RQ_list = FollowRQ.objects.filter(recipient = id)
            serialized = FollowRequestSerializer(RQ_list, many = True)

            return Response({"message" : "requests are retrieved successfully", "status" : "success", "requests" : serialized.data}, status = HTTP_200_OK)
        except ValueError:
            return Response({"status" : "error"}, status = HTTP_400_BAD_REQUEST)

