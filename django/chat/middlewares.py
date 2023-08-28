from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from .models.chatModel import Chat
from exceptions.exceptions import *
from .permissions import  *
import urllib.parse as urlparser
from asgiref.sync import sync_to_async



class BaseMiddleware:


    def __init__(self, app):
        self.app = app

    
    def get_permission_classes(self):
        """
        :return:
            list of instances of all the permission classes
        """
        return [permission() for permission in self.permission_class]


    def check_object_permission(self, scope):
        """
        just like wsgi applications, check user authorizations
        :param:
            user: the user
            scope, dict of information including header
        :return:
            True if all the permissions are passed
        """
        for permission in self.get_permission_classes():
            asynced_func =  sync_to_async(permission.check_object_permission)
            if not asynced_func(scope.get("user", None), scope.get("chat", None)):
                return False

    def set_query_params(self, scope):
        if scope.get("query_params", None):
            return

        qs = scope["query_string"]
        qs_dict = urlparser.parse_qs(qs.decode("UTF-8"))
        scope["query_params"] = {k: v[0] for k, v in qs_dict.items()}



class TokenBaseMiddleware(BaseMiddleware):

    permission_class = []


    async def get_user(self, user_id):
        try:
            user = await User.objects.aget(id=user_id)
            return user
        except User.DoesNotExist:
            raise NotFoundException("no such user exists", code= "authentication_failed")

    async def __call__(self, scope, receive, send):
        """
        Token Authentication middleware:
            by default, user is set in scope as "user"
        :param scope:
            client data including header and query params
        :return:
            invokes the related handler application
        """


        self.set_query_params(scope)

        token_settings = settings.SIMPLE_JWT
        header = scope.get("headers")
        try:
            token_type, raw_token = header.get("Authorization").split()
        except AttributeError as e:
            raise PermissionDenied("Failed to authenticated the user", code= "unable_to_authenticated")
        if token_type != "Bearer":
            raise InvalidToken("token type is incorrect", code= "invalid_token")

        if raw_token:
            token = AccessToken(token=raw_token)
            user_id = token.payload.get(token_settings["USER_ID_CLAIM"])
            user = await self.get_user(user_id)
        else:
            user = AnonymousUser()

        scope["user"] = user

        await self.set_chat(scope)

        return await self.app(scope, receive, send)



class ChatRoomMiddleware(BaseMiddleware):

    permission_class = [IsChatMemberPermission]

    async def set_chat(self, thread):


        if not thread:
            return
        try:
            chat_obj = await Chat.objects.aget(thread= thread)
            scope["chat"] = chat_obj
        except Chat.DoesNotExist:
            return

        self.check_object_permission(scope = scope)


    async def __call__(self, scope, receive, send):
        """
        looks for thread id and gets the chat
        this class is also responsible to check permissions required to access the chat
        """
        
        thread = scope["query_params"].get("thread", None)
        self.set_chat(thread=thread)


        self.check_object_permission(scope=scope)

        return await self.app(scope, send, receive)




def tokenBaseMiddlewareStack(inner):
    return ChatRoomMiddleware(TokenBaseMiddleware(inner))
