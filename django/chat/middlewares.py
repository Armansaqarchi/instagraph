from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from .models.chatModel import Chat
from exceptions.exceptions import *
from .permissions import  *

class TokenBaseMiddleware:

    permission_class = [IsMemberPermission]

    def __init__(self, app):
        self.app = app

    async def get_user(self, user_id):
        try:
            user = await User.objects.aget(id=user_id)
            return user
        except User.DoesNotExist:
            raise NotFoundException("no such user exists", code= "authentication_failed")

    async def __call__(self, scope, receive, send):
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

        self.check_object_permission(user, scope)
        return await self.app(scope, receive, send)

    def get_permission_classes(self):
        """
        :return:
            list of instances of all the permission classes
        """
        return [permission() for permission in self.permission_class]


    def check_object_permission(self, user, scope):
        """
        just like wsgi applications, check user authorizations
        :param:
            user: the user
            scope, dict of information including header
        :return:
            True if all the permissions are passed
        """

        chat_id = scope.get("chat_id", None)
        if not chat_id:
            return False
        try:
            chat_obj = Chat.objects.get(id = chat_id)
            scope["chat"] = chat_obj
        except Chat.DoesNotExist:
            return False

        for permission in self.get_permission_classes():
            if not permission.check_object_permission(user, chat_obj):
                return False



def tokenBaseMiddlewareStack(inner):
    return TokenBaseMiddleware(inner)
