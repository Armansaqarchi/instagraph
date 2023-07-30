import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from ..models import Account
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import FieldDoesNotExist
from django.contrib.auth import login, authenticate
from django.utils.http import url_has_allowed_host_and_scheme as is_url_safe
from django.core.exceptions import ValidationError
from ..models import Activation
from django.http import Http404
from django.conf import settings
from django.db import transaction
from ..utils import digit_random6, signup_verification
from ..api.serializer import (
    AccountSerializer,
    UserCreationSerializer,
    ProfileSerializer,
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
    HTTP_208_ALREADY_REPORTED,
    HTTP_404_NOT_FOUND,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
)
from ..exceptions.Exceptions import *


logger = logging.getLogger(__name__)


class SingleProfileView(GenericAPIView):

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
                return Response({"Account" : serializer.data, "Message" : message}, status=HTTP_200_OK)
            else:
                raise UnauthorizedException("You are refused to access this page")
        except (Account.DoesNotExist, Http404):
            raise NotFoundException("Account id %s does not exist", self.kwargs.get("pk"))
        except IndexError:
            raise BadRequestException("400 BAD REQUEST")





class LoginView(APIView):

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def post(self, request) -> Response:

        if request.user.is_authenticated:
            return Response({"detail" : "already authenticated"}, status=HTTP_208_ALREADY_REPORTED)

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
            
            # there might be a redirect url which user redirect to when login is done
            # this url first needs to be checked to see if allowed to serve as a host
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

            return Response({"message" : message, "status" : "success", "token" : {"refresh" : str(referesh_token),
                             "access" : str(referesh_token.access_token)}}, HTTP_200_OK)
        else: 
            logger.info(f"failed to authenticate user %s".format(request.user.id))

            raise UnauthorizedException("Username or password may be incorrect")
           


    
class SignUpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request) -> Response:
        
        user = UserCreationSerializer(data=request.data)

        try:
            if user.is_valid(raise_exception=True):
                instance = user.save()
                # this feature is temporarily false due to problem with sending emails
                if settings.ENABLE_USER_ACTIVATION:
                    with transaction.atomic():
                        act = Activation.objects.create(
                            user = instance,
                            code = digit_random6(),
                            email = user.validated_data['email']
                        )
                        signup_verification(subject = "verification", message =  "message", email = act.email)
                        return Response({"message" : "activation code has been sent to your email, please check your inbox and submit your verification",
                                        "status" : "success"}, status=HTTP_200_OK)
                else:

                    logger.info(f"a new user signed up : %s".format(request.user.id))

                    return Response({"status" : "success", "message" : "user created"},
                                        HTTP_201_CREATED)
            
        except ValidationError:
            raise BadRequestException("Bad or incorrect informations")
        except EmailExistsException:
            raise AlreadyExistsException("The Email has already been taken by another user")
        except UsernameExistsException:
            raise AlreadyExistsException("The username has already been taken by another user")
        

class Activate(APIView):

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
            return Response({"message" : "logged in successfully", "status" : "success"}, status=HTTP_200_OK)
        raise UnauthorizedException("something went wrong while verifying the code, try again")





        


