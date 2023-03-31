from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.generics import GenericAPIView
from .models import Account
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.shortcuts import redirect
from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.contrib.auth import authenticate, login, logout
from rest_framework.validators import ValidationError
from .api.serializer import (
    AccountSerializer,
    UserCreationSerializer
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
    HTTP_400_BAD_REQUEST
)



class SingleProfileView(LoginRequiredMixin, GenericAPIView):

    model = Account
    login_url = "accounts/login"
    renderer_classes = [JSONRenderer]


    def has_object_permission(self, request, obj):
        if request.method in SAFE_METHODS: #read access
            return True, "SAFE"
    
        try:
            if request.user == obj.user:
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
            
            serializer = AccountSerializer(data=request.data)
            #sending json response containing the Account info, use 'Account' to access it
            return Response({"Account" : serializer, "Message" : message}, status=HTTP_200_OK)
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
            #give user the token 
            login(request=request, user=user)
            message = "successfully logged in"
            return Response({"message" : message}, HTTP_200_OK)
        else:
            message = "username or password is incorrect"
            return Response({"message" : message}, HTTP_401_UNAUTHORIZED)



class SignUpView(APIView):

    permission_classes = [AllowAny]

    def post(self, request) -> Response:
        
        user = UserCreationSerializer(data=request.data)
        try:
            if user.is_valid(raise_exception=True):
                user.save()
                return Response({"status" : "success", "message" : "user created"}, HTTP_201_CREATED)
        except ValidationError:
            return Response({"status" : "error", "errors" : user.errors}, status=HTTP_400_BAD_REQUEST)

