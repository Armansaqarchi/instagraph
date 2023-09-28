import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from ..models import Account
from ..permissions import *
import pyotp
import re
from django.contrib.auth.models import User
from time import time
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from base64 import b32encode
from posts.permissions import IsFollowerOrPublicPermission
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ViewSet
from django.conf import settings
from ..email_sender import send_email
from ..api.serializer import (
    UserSerializer,
    ProfileViewSerializer,
    profileEditSerializer,
    EmailExistsException,
    UsernameExistsException,
    ProfilePictureEditSerializer
)
from rest_framework.permissions import (
    SAFE_METHODS,
    )
from rest_framework.status import(
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_206_PARTIAL_CONTENT
)


from exceptions.exceptions import *

logger = logging.getLogger(__name__)


class OTPManager:
    @staticmethod
    def generate_otp_key(user):
        """
        secret key generator based on user details
        """

        return f"{settings.SECRET_KEY}{user.email}{user.username}".encode()

    @staticmethod
    def send_otp(user, subject= None, template = "email_verification.html"):
        """
        makes an otp and then sends it to user's email
        """
        secret = b32encode(OTPManager.generate_otp_key(user=user))
        otp = pyotp.TOTP(secret, interval=settings.ACTIVATION_TIMEOUT)
        act_code = otp.now()
        send_email({"activation" : act_code}, user, subject = subject, template=template)

    @staticmethod
    def verify_otp(user, otp, exc_message = "invalid_otp"):
        """
        defined customized method to verify otp codes
        """
        key = b32encode(OTPManager.generate_otp_key(user=user))
        real_otp = pyotp.TOTP(key, interval=settings.ACTIVATION_TIMEOUT)
        if not real_otp.verify(otp, for_time= int(time())):
            raise UnauthorizedException(exc_message, code="invalid_code")

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

        if not user:
            raise UnauthorizedException("Username or password may be incorrect", "incorrect_credentials")
        
        if user.is_active:
            login(request=request, user=user)
            message = "successfully logged in"
            referesh_token = user.account.token
            return Response({"Message" : message, "Status" : "success", "Code" : "login_successful",
                              "Token" : {"refresh" : str(referesh_token),
                             "access" : str(referesh_token.access_token)}}, HTTP_200_OK)
        else:
            OTPManager.send_otp(user = user)

            return Response({"Message" : f"Activation Code has been sent to {user.email}",\
                          "Status" : "Success", "Code" : "activation_code"}, status=HTTP_200_OK)


class ProfileView(ModelViewSet):

    PERMISSION_CASES = {
        "get": IsFollowerOrPublicPermission,
        "patch": IsOwnerPermission,
        "post": IsOwnerPermission
    }

    errors = {
        "invalid": "Invalid format for the request body",
        "email_exists": "The Email has already been taken by another user",
        "username_exists": "The Username has already been taken by another user"
    }

    class ProfilePaginator(PageNumberPagination):
        page_size_query_param = 20
        page_query_param = "page"
        page_size = 20

    parser_classes = [MultiPartParser, JSONParser]
    serializer_class = profileEditSerializer
    queryset = Account.objects.all()
    pagination_class = ProfilePaginator


    def get_permissions(self):
        """
        permissions differ according to request http method.
        some actions might require patch method which can be profile update or info update,
        and that leads to different models
        """

        return [self.PERMISSION_CASES[self.request.method.lower()]()]


    def create(self, request) -> Response:
        
        user = UserSerializer(data=request.data)
        try:
            user.is_valid(raise_exception=True)
            user = user.save()
            if not settings.EMAIL_ACTIVATION:
                return self.perform_activation(user=user, request=request)
            
            OTPManager.send_otp(user)

        except ValidationError as e:
            self.kwargs["Fields"] = {field : str(e.detail[field][0]) for field in e.detail}
            raise BadRequestException(self.errors["invalid"], "signup_fields_error")
                
        except EmailExistsException:
            raise AlreadyExistsException(self.errors["email_exists"], code="email_exists")
        
        except UsernameExistsException:
            raise AlreadyExistsException(self.errors["username_exists"], code="username_exists")
        
        
        return Response({"Message" : f"Activation Code has been sent to {user.email}",\
                          "Status" : "Success", "Code" : "activation_code"}, status=HTTP_200_OK)

    @staticmethod
    def perform_activation(user, request):

        user.is_active = True
        login(request=request, user=user)
        token = user.account.token
        
        return Response({"Status" : "success", "Message" : "user created", "Code" : "user_created",
                        "Token" : {"refresh" : str(token), "access" : str(token.access_token)}},
                            HTTP_201_CREATED)


    def update_profile_image(self, request, pk):
        account = self.get_object()
        serializer = ProfilePictureEditSerializer(instance= account.mediaprofile, data=request.data, partial = True)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
        return Response({"data" : serializer.data, "Message" : "profile picture updated", "Code" : "profile_update", "Status" : "success"},
                         status=HTTP_206_PARTIAL_CONTENT)
    
    def update(self, request, pk):
        try:
            return super().update(request, partial = True)
        except ValidationError as exc:
            self.kwargs["Fields"] = {field : str(exc.detail[field][0]) for field in exc.detail}
            raise BadRequestException("invalid request body format", code = "invalid_account_format")
            
    
    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        response.data = {"Message" : "user successfully deleted", "Status" : "Success", "Code" : "user_deleted"}
        return response
    
    def perform_destroy(self, instance):
        """
        delete the user so the account will automatically be deleted
        """
        instance.user.delete()

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ProfileViewSerializer
        response = super().retrieve(request, *args, **kwargs)
        response.data = {"Profile" : response.data, "Message" : "user detail",
                               "Status" : "success", "Code" : "user_profile"}
        
        return response
    

class PasswordResetAPIView(ViewSet):

    regex = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"

    errors = {
        "invalid_params": "invalid_query_params",
        "password_low_security": "password must include at least 8 characters including numbers and one with capital"
    }

    def get_user(self, **kwargs):

        user = User.objects.filter(**kwargs).first()
        if not user:
            raise NotFoundException(f"No such user found")

        return user
         

    def forgot_reset_pass(self, request):
        to_email = request.data["to_email"]
        user = self.get_user(email = to_email)
        OTPManager.send_otp(user=user, subject= "reset password verification code", template="reset_password_verification.html")
        return Response({"Message" : f"6-digit verification code sent to {to_email}", "Status" : "success",
                          "Code" : "verification_code_sent"}, status=HTTP_200_OK)


    def confirm_reset_pass_otp(self, request, email):
        otp = request.data["otp"]
        user = self.get_user(email = email)
        OTPManager.verify_otp(user=user, otp=otp)
        token = default_token_generator.make_token(user= user)
        return Response({"Message" : "otp confirmed", "Code" : "otp_confirmed", "Status" : "success",\
                          "password_reset_token" : token, "user_pk" : user.pk})
    

    def reset_pass(self, request):
        token = request.GET.get("token", None)
        email_claim = request.GET.get("email", None)
        print(email_claim, token)
        if not token or not email_claim:
            raise BadRequestException(self.errors["invalid_params"], code = "invalid_qeury_params")
        
        user = self.get_user(email = email_claim)
        if default_token_generator.check_token(user = user, token = token):
            return self._reset_password(user=user, new_password=request.data.get("password", None))
        
        raise UnauthorizedException("Token does not match the email or maybe expired", code="invalid_token")


    def _reset_password(self, user, new_password):
        if not new_password:
            raise BadRequestException(self.errors["password_low_security"], code = "invalid_password_type")
        if user.check_password(raw_password = new_password):
            raise PasswordIsEqualException()

        user.set_password(new_password)
        user.save()
        return Response({"Message" : "Your password has been reset successfully", "Code" : "password_reset", "Status" : "Success"},
                        status=HTTP_200_OK)

        
    def _verify_password(self, raw_password):
        return re.match(self.regex, raw_password)


    
class ActivationCode(APIView):
    """
    an activation class works based on otp
    each otp password remains 2 minutes valid.
    this is because component time as an input to opt.verify() method is calculated like : duration_time // interval_time
    which duration time calculated since reference time.
    """

    errors = {
        "activation_invalid" : "activation code is invalid or maybe expired"
    }

    def get_user(self, pk):
        try:
            return Account.objects.get(pk = pk).user
        except Account.DoesNotExist:
            raise NotFoundException(f"No such user {pk}", code="user_not_found")


    def post(self, request, pk):
        user = self.get_user(pk=pk)
        OTPManager.verify_otp(user=user, otp=request.data["otp"], exc_message=self.errors["activation_invalid"])
        return ProfileView.perform_activation(request=request, user=user)





# class UserProfileView(APIView):

#     model = Account
#     login_url = "accounts/login"
#     permission_classes = [IsAuthenticated]

#     def has_object_permission(self, request, obj):
#         if request.method in SAFE_METHODS: # read access
#             return True, "SAFE"
#         try:
#             if request.user == obj.user:
#                 return True, "OWNER"
#         except FieldDoesNotExist:
#             return False, "BAD REQUEST"
#         return False, "PERMISSION DENIED"


#     def get(self, request, pk) -> Response:
#         try:
#             account = Account.objects.get(id = pk)
#             self.has_object_permission(request, obj=account)
#             serializer = ProfileViewSerializer(account)
#             #sending json response containing the Account info, use 'Account' to access it
#             return Response({"Account" : serializer.data, "Message" : "user details sent", "Status" : "success"}, status=HTTP_200_OK)

#         except Account.DoesNotExist:
#             raise NotFoundException("Account id %s does not exist" % pk, code="profile_not_found")





        


