from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings
from django.contrib.auth.models import User, AnonymousUser
from exceptions.exceptions import *
from asgiref.sync import sync_to_async, async_to_sync

class TokenBaseMiddleware:

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
        return await self.app(scope, receive, send)


def tokenBaseMiddlewareStack(inner):
    return TokenBaseMiddleware(inner)
