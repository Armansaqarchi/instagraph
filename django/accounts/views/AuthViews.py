import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Account
from ..permissions import *
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.core.exceptions import FieldDoesNotExist
from django.contrib.auth import login, authenticate
from rest_framework.exceptions import ValidationError
from ..models import Activation
from rest_framework.viewsets import ModelViewSet
from django.db import transaction
from ..api.serializer import (
    UserSerializer,
    ProfileViewSerializer,
    EmailExistsException,
    UsernameExistsException
)
from rest_framework.permissions import (
    SAFE_METHODS,
    )
from rest_framework.status import(
    HTTP_200_OK,
    HTTP_201_CREATED,
)


from exceptions.exceptions import *

logger = logging.getLogger(__name__)


class UserProfileView(APIView):

    model = Account
    login_url = "accounts/login"
    permission_classes = [IsAuthenticated]

    def has_object_permission(self, request, obj):
        if request.method in SAFE_METHODS: # read access
            return True, "SAFE"
        try: 
            if request.user == obj.user:
                return True, "OWNER"
        except FieldDoesNotExist:
            return False, "BAD REQUEST"
        return False, "PERMISSION DENIED"
    
    
    def get(self, request, pk) -> Response:
        try:
            account = Account.objects.get(id = pk)
            self.has_object_permission(request, obj=account)    
            serializer = ProfileViewSerializer(account)
            #sending json response containing the Account info, use 'Account' to access it
            return Response({"Account" : serializer.data, "Message" : "user details sent", "Status" : "success"}, status=HTTP_200_OK)

        except Account.DoesNotExist:
            raise NotFoundException("Account id %s does not exist" % pk, code="profile_not_found")


class LoginView(APIView):
    def post(self, request) -> Response:
        if request.user.is_authenticated:
            raise AlreadyExistsException("user have already authenticated", code= "already_authenticated")
        try:
            username = request.data["username"]
            password = request.data["password"]
        except KeyError:
            user = authenticate(request=request)
        else:
            user = authenticate(username = username, password = password)
        if user is not None:
            login(request=request, user=user)
            message = "successfully logged in"
            referesh_token = user.account.token
            return Response({"Message" : message, "Status" : "success", "Code" : "login_successful",
                              "Token" : {"refresh" : str(referesh_token),
                             "access" : str(referesh_token.access_token)}}, HTTP_200_OK)
        else: 
            raise UnauthorizedException("Username or password may be incorrect", "incorrect_credentials")


class ProfileView(ModelViewSet):

    parser_classes = [MultiPartParser]
    permission_classes = [OwnerPermission]
    def create(self, request) -> Response:
        user = UserSerializer(data=request.data)
        try:
            user.is_valid(raise_exception=True)
            user = user.save()
            token = user.account.token
            return Response({"Status" : "success", "Message" : "user created", "Code" : "user_created",
                                    "Token" : {"refresh" : str(token), "access" : str(token.access_token)}},
                                        HTTP_201_CREATED)
        except ValidationError as e:
            self.kwargs["Fields"] = {field : str(e.detail[field][0]) for field in e.detail}
            print(e.detail)
            raise BadRequestException("invalid format for the request body", "signup_fields_error")
        except EmailExistsException:
            raise AlreadyExistsException("The Email has already been taken by another user", code="email_exists")
        except UsernameExistsException:
            raise AlreadyExistsException("The username has already been taken by another user", "username_exists")
    

    def update(self, request, pk):
        print(request.data)
        return Response(status=HTTP_200_OK)
        
    
    
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    
    
class Activate(APIView):

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, code):

        code = request.data["verification_code"]
        email = request.data["email"]
        act = Activation.objects.filter(code = code, email = email).first()
        if act:
            user = act.user
            user.is_active = True
            user.save()

            act.delete()
            authenticate(username = user.username, password = user.password)
            login(request=request, user=user)
            return Response({"Message" : "logged in successfully", "Status" : "success"}, status=HTTP_200_OK)
        raise UnauthorizedException("something went wrong while verifying the code, try again", code = "unable_to_activate")





        


