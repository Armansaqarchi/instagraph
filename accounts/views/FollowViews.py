from rest_framework.generics import ListAPIView
from ..api.serializer import (
    FollowingSerializer,
    FollowerSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.db import transaction
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from ..models import Follows, FollowRQ
from ..permissions import *
from ..models import Account
from rest_framework.response import Response
import logging
from ..api.serializer import FollowingSerializer, FollowRequestSerializer
from rest_framework.status import(
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_204_NO_CONTENT
)
from exceptions.exceptions import *

logger = logging.getLogger(__name__)


class FollowersAPIView(ModelViewSet):

    class FollowerPaginator(PageNumberPagination):
        page_query_param = "page"
        page_size = 30

    pagination_class = FollowerPaginator
    errors = {
        "forbidden" : "Access Denied",
        "no_such_fr" : "No such follow request",
        "already_follows" : "The user is already following you"
    }
    
    def get_queryset(self):
        """
        returns queryset based on http method provided in request header
        """
        QUERYSET_CASES = {
            "get" : FollowRQ,
            "delete" : Follows,
            "post" : FollowRQ
        }
        return QUERYSET_CASES[self.request.method.lower()]
    

    def get_followers(self):
        account = self.get_object()
        followings_id = account.following_list.values_list('follower', flat = True)
        return account, Account.objects.filter(id__in = followings_id)     


    def list(self, id):
        """
        lists all the followers for specific account
        @params:
            -id: account id for some account
        @returns:
            -ForbiddenException: when user is not authorized to access the data.
            this happends when user is not the follower or account nor owner

            -- Response on Ok
        """
        try:
            account, queryset = self.filter_queryset(id)
            page = self.paginate_queryset(queryset=queryset)
            serializer = self.serializer_class(page, many=True)
            followers_count = account.followers_list
            return Response({"Message" : "follower page is ready", "page_obj" : serializer.data, "followers_number" : followers_count,
                              "Status" : "success", "Code" : "follower_list_done"}, status=HTTP_200_OK)
        except PermissionDenied:
            raise ForibiddenException(self.errors["forbidden"], code = "permission_denied")
        
    def destroy(self, request, pk): # tested
        """
        performs delete on specific follow
        @params:
            -id for follow object
        @returns:
            -NotFoundException: when such id not found

            --Response on Ok
        """

        self.queryset = Follows.objects.all()
        follow = self.get_object()
        self.perform_destroy(follow)
        return Response({"Message" : "follower removed", "Code" : "follower_remove", "Status" : "Success"},
                         status=HTTP_204_NO_CONTENT)

    @transaction.atomic
    def accept_or_reject(self, request, pk): # tested
        """
        acccepts the following requests or rejects them
        @param:
            -pk : follow request object id (UUID format)
        @query_params:
            -accepted: whether request is accepted 
        @returns:
            -AlreadyExistsException: when user is already following the same account
            -NotFoundException: when there is no such id corresponding to some fr

            --Response on Ok
        """

        try:
            fr = self.get_object()
        except Http404:
            raise NotFoundException(self.errors["no_such_fr"], code="fr_not_found")
        isAccepted = request.GET.get("accepted") or "True"

        if isAccepted == "True":
            already_follows = Follows.objects.filter(Q(follower__id = fr.sender.id) & Q(following__id = fr.recipient.id)).exists()
            if already_follows:
                raise AlreadyExistsException(self.errors["already_follows"])
            Follows.objects.create(
                follower = fr.sender,
                following = fr.recipient
            )
            message =  "follow request accepted"
            code = "following_accepted"
        else:
            message = "follow request rejected"
            code = "following_rejected"
        
        fr.delete()
        return Response({"Message" : message, "Status" : "Success", "Code" : code},
                         status = HTTP_200_OK)


class FollowingsAPIView(ModelViewSet):
    """
    viewset for manipulating follow apis
    """

    errors = {
        "create_not_found" : "No such user or account",
        "has_req" : "has already pending request",
        "has_follow" : "already following"
    }


    def get_queryset(self):
        QUERYSET_CASES = {
            "get" : Account,
            "delete" : Follows
        }

        return QUERYSET_CASES[self.request.method.lower()]



    def create(self, request, pk): # tested
        try:
            target = self.get_object()
        except Http404:
            raise NotFoundException(self.errors["create_not_found"], code = "no_such_user_id")
        requested = FollowRQ.objects.filter(Q(sender = self.request.user.account) & Q(recipient = target)).exists()
        if requested : raise AlreadyExistsException(self.errors["has_req"], code = "has_requested")

        following = Follows.objects.filter(Q(follower = self.request.user.account) & Q(following = target)).exists()
        if following : raise AlreadyExistsException(self.errors["has_follow"], code = "has_follow")

        if target.is_private:
            self.perform_follow_req(target=target)
            message = f"follow request sent to {target.user.username}"
            code = "follow_req_done"
        else:
            self.perform_follow(target = target)
            message = f"started following {target.user.username}"
            code = "following_done"
        return Response({"Message" : message, "Status" : "Success", "Code" : code}, status= HTTP_200_OK)

        
    def perform_follow(self, target): # tested
        Follows.objects.create(
            follower = self.request.user.account,
            following = target
        )


    def perform_follow_req(self, target): # tested
        FollowRQ.objects.create(
            sender = self.request.user.account,
            recipient = target
        )

        
    def destroy(self, request, pk): # tested
        follow_obj = self.get_object()
        self.perform_destroy(follow_obj)
        return Response({"Message" : "the following successfully deleted from list", "Status" : "Success", "Code" : "following_deleted"},
                        status=HTTP_204_NO_CONTENT)



class FollowersListAPIView(ListAPIView):

    class FollowersListPaginator(PageNumberPagination):
        page_query_param = "page"
        max_page_size = 20
        page_size = 30


    serializer_class = FollowerSerializer
    pagination_class = FollowersListPaginator
    
    def get_queryset(self): # tested
        """
        returns list of followers for a user
        """
        return self.request.user.account.followers_list


    def filter_queryset(self): # tested
        """
        this method can be customized to filter objects in later updates
        """
        return self.get_queryset()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset()
        page = self.paginate_queryset(queryset=queryset)
        f_serializers = self.serializer_class(instance = page, many=True)
        return Response({"Followers" : f_serializers.data, "Message" : "followers list returned as \"Followers\" ",
                          "Status" : "Success", "Code" : "followers_list"})

class FollowingsListAPIView(ListAPIView):

    class FollowingListPaginator(PageNumberPagination):
        page_query_param = "page"
        page_size = 30
        max_page_size = 30


    serializer_class = FollowingSerializer
    pagination_class = FollowingListPaginator

    def get_queryset(self): # tested
        return self.request.user.account.followings_list
    
    def filter_queryset(self): # tested
        """
        any filtering logic would be added in this section
        """
        return self.get_queryset()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset()
        page = self.paginate_queryset(queryset=queryset)
        f_serializers = self.serializer_class(page, many=True)
        return Response({"Followings" : f_serializers.data, "Message" : "followings list returned as \"Followings\" ",
                          "Status" : "Success", "Code" : "followings_list"})
    

class FollowRQListAPIView(ListAPIView):

    class FollowRQListPaginator(PageNumberPagination):
        page_query_param = "page"
        page_size = 30

    queryset = FollowRQ.objects.all()
    permission_classes = [IsOwnerPermission]
    serializer_class = FollowRequestSerializer

    def list(self, request, *args, **kwargs):
        response =  super().list(request, *args, **kwargs) 
        response.data = {"Requests" : response.data, "Message" : "requests are ready", "Code" : "follow_requests", "Status" : "Success"}
        return response
        

    
# class FriendFollowRQ(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request, following_id) -> Response:
#         to_user = Account.objects.filter(id = following_id).first()
#         if to_user is None:
#             raise NotFoundException("user id %s does not exists" %following_id)
#         has_requested = to_user.received_set.filter(sender = request.user.account.id).exists()
#         if has_requested:
#             raise AlreadyExistsException("you have already sent follow request to user %s" %to_user.user.username, code= "already_requested")
#         sender = request.user.account
#         is_following = sender.follower_set.filter(following = following_id)

#         if is_following:
#             message = f"user {to_user.id} is already being followed"
#             raise AlreadyExistsException("You are already following user %s" %to_user.user.username, "already_following")
#         try:

#             if to_user.is_private:
#                 FollowRQ.objects.create(
#                     sender = sender,
#                     recipient = to_user,
#                     is_read = False,
#                     accepted = False
#                 )

#                 logger.info("sent friendly request to user : %s".format(to_user.user.username))

#                 message = "successfully sent follow request"
#                 return Response({"Message" : message, "Status" : "success", "Code" : "folliw_req_send"}, status = HTTP_200_OK)
#             else:
#                 following_acc = Account.objects.get(id = following_id)
#                 Follows.objects.create(
#                     follower = request.user.account,
#                     following = following_acc
#                 )
#                 message = "strated following %s" %to_user.user.username
#                 logger.info("user %s started following user %s".format(request.user.id, following_id))
#                 return Response({'Message' : message, 'Status' : "success", "Code": "follow_req"}, status = HTTP_200_OK)
#         except IntegrityError as e:
#             raise BadRequestException("Bad request", "constraint_violation")

# class AcceptRQ(APIView):

#     permission_classes = [IsOwnerPermission]
#     login_url = settings.LOGIN_URL

#     def get(self, request, RQ_id) -> Response:
#         """
#         given RQ_id, accepts the friend reqeust corresponding to the RQ_id
#         """
#         try:
#             fr_req = FollowRQ.objects.get(id = RQ_id)
#         except FollowRQ.DoesNotExist:
#             raise NotFoundException("No such request", code="invalid id")
#         except ValidationError:
#             raise BadRequestException("invalid uuid number or request is not valid", code="invalid format")
#         self.check_object_permissions(request=request, obj=fr_req.recipient)
#         if fr_req is not None:
#             has_followed = Follows.objects.filter(Q(follower = fr_req.sender) & Q(following = fr_req.recipient)).exists()
#             if not has_followed:
#                 with transaction.atomic():
#                     follower_user = fr_req.sender
#                     following_user = fr_req.recipient
#                     Follows.objects.get_or_create(
#                         follower = follower_user,
#                         following = following_user
#                     )
#                     fr_req.delete()
#                 return Response({"Message" : f"accepted {follower_user} request",
#                                   "Status" : "success", "Code": "request_accepted"}, status=HTTP_200_OK)

#             raise AlreadyExistsException("user is already following you", code= "already_following")
        
#         raise BadRequestException("no such following request exists", code= "no_such_user")
    

# class RQList(LoginRequiredMixin, ListAPIView):
#     permission_classes = [IsOwnerPermission]
#     paginate_by = 20
#     login_url = settings.LOGIN_REDIRECT_URL


#     def get(self, request, id) -> Response:
#         """
#         returns list of friend requset
#         """
#         try:
#             RQ_list = FollowRQ.objects.filter(recipient = id)
#             account = Account.objects.get(id = id)
#             self.check_object_permissions(request, obj=account)
#             serialized = FollowRequestSerializer(RQ_list, many = True)

#             return Response({"Message" : "requests are retrieved successfully", "Status" : "success",
#                               "Code" : "follow_req_are_returned", "requests" : serialized.data}, status = HTTP_200_OK)
#         except ValueError:
#             raise BadRequestException("Bad or incorrect credentials", code= "incorrect_credentials")

