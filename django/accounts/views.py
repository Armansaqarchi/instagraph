import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import GenericAPIView
from .models import Account, Follows
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.db import IntegrityError
from django.core.exceptions import FieldDoesNotExist
from django.contrib.auth import authenticate, login, logout
from rest_framework.validators import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import BasePermission
from django.contrib.auth.hashers import make_password
from .api.serializer import (
    AccountSerializer,
    UserCreationSerializer,
    FollowerSerializer,
    EmailExistsException,
    UsernameExistsException
)
from rest_framework.permissions import (
    SAFE_METHODS,
    AllowAny
    )
from rest_framework.status import(
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT
)


logger = logging.getLogger(__name__)



class IsFollowerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        
        account_id = request.user.account.id
        if obj.following_set.filter(follower_set = account_id).exists():
            return True
        
        return False


class SingleProfileView(LoginRequiredMixin, GenericAPIView):

    model = Account
    login_url = "accounts/login"
    renderer_classes = [JSONRenderer]


    def has_object_permission(self, request, obj):
        if request.method in SAFE_METHODS: #read access
            logger.info(f"user %s has read only permission to object profile : %s".format(request.user.id, obj.id))
            return True, "SAFE"
    
        try:
            if request.user == obj.user:
                logger.info(f"%s is owner of profile %s : %s-%s".format(request.user.id, obj.id, obj.firstname, obj.lastname))
                return True, "OWNER"
        
        except FieldDoesNotExist:
            return False, "BAD REQUEST"
        
        return False, "PERMISSION DENIED"
    

    def get_queryset(self, request):
        return Account.objects.filter(kwargs=self.kwargs['pk'])
    
    
    def get(self, request) -> Response:
        query_set = self.get_queryset()

        try:
            account = self.get_object(queryset=query_set)
            is_allowed, message = self.has_object_permission(self, request=request, obj=account)
            if is_allowed:
                serializer = AccountSerializer(data=request.data)
                #sending json response containing the Account info, use 'Account' to access it
                logger.info(f"access allowed for user : %s profile : %s".format(request.user.id, serializer.get_attribute("id")))
                return Response({"Account" : serializer, "Message" : message}, status=HTTP_200_OK)
            else:
                return Response ({"message": "You are refused to access this page", "status": "error"}, status=HTTP_401_UNAUTHORIZED)
        except Account.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        
    
        

class LoginView(APIView):


    

    permission_classes = [AllowAny]


    # no method 'get' since it will be handled from client side
    
    def post(self, request) -> Response:


        

        # if request.user.is_authenticated:
        #     return redirect("profile")




        username = request.data["username"]
        password = request.data["password"]

        

        user = authenticate(username = username, password = password)



        if user is not None:
            logger.info(f"user %s successfully authenticated".format(request.user.id))
            #give user the token 
            login(request=request, user=user)
            message = "successfully logged in"
            return Response({"message" : message, "status" : "success"}, HTTP_200_OK)
        else:
            logger.info(f"failed to authenticate user %s".format(request.user.id))
            message = "username or password is incorrect"
            return Response({"message" : message, "status" : "error"}, HTTP_401_UNAUTHORIZED)
        

        



class SignUpView(APIView):

    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        
        user = UserCreationSerializer(data=request.data)
        try:
            if user.is_valid(raise_exception=True):
                    user.save()
                    logger.info(f"a new user signed up : %s".format(request.user.id))
                    return Response({"status" : "success", "message" : "user created"}, HTTP_201_CREATED)
            
        except ValidationError:
            return Response({"status": "error", "errors" : user.errors}, status=HTTP_400_BAD_REQUEST)
        except EmailExistsException:
            return Response({"message": "email is already taken, try a different email", "status": "error"}, status=HTTP_409_CONFLICT)
        except UsernameExistsException:
            return Response({"message": "username is already taken, try a different username", "status": "error"}, status=HTTP_409_CONFLICT)
        




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
            queryset = self.get_queryset()
            followers_list = self.get_object()
            serializer = FollowerSerializer(followers_list, many=True)
        except Exception:
            return Response({"status" : "error"}, HTTP_400_BAD_REQUEST)
        return Response({"followers" : serializer.data}, status=HTTP_200_OK)
    
    


