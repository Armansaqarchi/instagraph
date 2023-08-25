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
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
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

    errors = {
        "invalid" : "Invalid format for the request body" ,
        "email_exists" : "The Email has already been taken by another user",
        "username_exists" : "The Username has already been taken by another user"
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

        PERMISSION_CASES = {
            "get" : IsFollowerPermission,
            "patch" : IsOwnerPermission,
            "post" : IsOwnerPermission
        }

        return [PERMISSION_CASES[self.request.method.lower()]()]


    def create(self, request) -> Response:
        
        user = UserSerializer(data=request.data)
        try:
            user.is_valid(raise_exception=True)
            user = user.save()
            token = user.account.token

        except ValidationError as e:
            self.kwargs["Fields"] = {field : str(e.detail[field][0]) for field in e.detail}
            raise BadRequestException(self.errors["invalid"], "signup_fields_error")
        
        except EmailExistsException:
            raise AlreadyExistsException(self.errors["email_exists"], code="email_exists")
        
        except UsernameExistsException:
            raise AlreadyExistsException(self.errors["username_exists"], code="username_exists")
        
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





        


