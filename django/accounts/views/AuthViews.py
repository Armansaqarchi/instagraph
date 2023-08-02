import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Account
from ..permissions.accountPermissions import (
    OwnerPermission
)
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.core.exceptions import FieldDoesNotExist
from django.contrib.auth import login, authenticate
from django.utils.http import url_has_allowed_host_and_scheme as is_url_safe
from rest_framework.exceptions import ValidationError
from ..models import Activation
from django.http import Http404
from django.conf import settings
from django.db import transaction
from ..utils import digit_random6, signup_verification
from ..api.serializer import (
    UserSerializer,
    ProfileSerializer,
    EmailExistsException,
    UsernameExistsException
)
from rest_framework.permissions import (
    SAFE_METHODS,
    )
from rest_framework.status import(
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_208_ALREADY_REPORTED,
)
from exceptions.exceptions import *


logger = logging.getLogger(__name__)


class SingleProfileView(APIView):

    model = Account
    login_url = "accounts/login"
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    def has_object_permission(self, request, obj):
        if request.method in SAFE_METHODS: # read access
            logger.info(f"user %s has read only permission to object profile : %s".format(request.user.id, obj.id))
            return True, "SAFE"
        try: 
            if request.user == obj.user:
                logger.info(f"%s is owner of profile %s : %s-%s".format(request.user.id, obj.id, obj.firstname, obj.lastname))
                return True, "OWNER"
        except FieldDoesNotExist:
            return False, "BAD REQUEST"
        return False, "PERMISSION DENIED"
    

    def get_queryset(self):
        return Account.objects.filter(id = self.kwargs.get("pk"))
        
    
    def get(self, request, pk) -> Response:
        self.kwargs["pk"] = pk
        try:
            account = self.get_object()
            is_allowed, message = self.has_object_permission(request, obj=account)
            if is_allowed:
                
                serializer = ProfileSerializer(account)
                #sending json response containing the Account info, use 'Account' to access it
                # logger.info(f"access allowed for user : %s profile : %s".format(request.user.id, serializer.data.get("username")))
                return Response({"Account" : serializer.data, "Message" : message, "Status" : "success"}, status=HTTP_200_OK)
            else:
                raise UnauthorizedException("You are refused to access this page", "insufficient_permissions")
        except (Account.DoesNotExist, Http404):
            raise NotFoundException("Account id %s does not exist", self.kwargs.get("pk"), code="profile_not_found")
        except IndexError:
            raise BadRequestException("400 BAD REQUEST", "bad_request")


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
            logger.info(f"user %s successfully authenticated".format(user.account.id))
            login(request=request, user=user)
            message = "successfully logged in"
            redirect_to = request.META.get("next")
            if settings.CHECK_URLS:
                if redirect_to is not None:
                    url_is_safe = is_url_safe(url=redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())
                    if not url_is_safe:
                        redirect_to = settings.LOGIN_REDIRECT_URL
                else:
                    redirect_to = settings.LOGIN_REDIRECT_URL
                    url_is_safe = True
            else: url_is_safe = None
            referesh_token = user.account.token
            return Response({"Message" : message, "Status" : "success", "Code" : "login_successful",
                              "Token" : {"refresh" : str(referesh_token),
                             "access" : str(referesh_token.access_token)}}, HTTP_200_OK)
        else: 
            raise UnauthorizedException("Username or password may be incorrect", "incorrect_credentials")


class ProfileView(APIView):
    permission_classes = [OwnerPermission]
    def post(self, request) -> Response:
        user = UserSerializer(data=request.data)
        try:
            if user.is_valid(raise_exception=True):
                user = user.save()
                token = user.account.token
                return Response({"Status" : "success", "Message" : "user created", "Code" : "user_created",
                                  "Token" : {"refresh" : str(token), "access" : str(token.access_token)}},
                                        HTTP_201_CREATED)
        except ValidationError as e:
            self.kwargs["Fields"] = {field : str(e.detail[field][0]) for field in e.detail}
            raise BadRequestException("invalid format", "invalid_format")
        except EmailExistsException:
            raise AlreadyExistsException("The Email has already been taken by another user", code="email_exists")
        except UsernameExistsException:
            raise AlreadyExistsException("The username has already been taken by another user", "username_exists")
        
    def put(self, request):
        new_profile = request.data
        try:
            id = request.GET.get("id")
        except AttributeError:
            pass
        if id:
            account = Account.objects.get(id = id)
        else:
            account = request.user.account
        user = account.user
        account.update(
            bio = new_profile.get("bio", default = ""),
            gender = new_profile.get("gender", default = account.gender),
            is_price = new_profile.get("is_private", default = account.is_private)
        )
        user.update(
            username = new_profile.get("username", user.username),
            firstname = new_profile.get("first_name",user.firstname),
            lastname = new_profile.get("last_name", user.lastname)
        )


        

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





        


