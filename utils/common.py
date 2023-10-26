from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken
from django.conf import settings


class TokenMiddleware:
    @staticmethod
    def verify_token(header):
        token_settings = settings.SIMPLE_JWT
        try:
            token_type, raw_token = header.get("HTTP_AUTHORIZATION").split()
        except AttributeError as e:
            raise PermissionDenied("Failed to authenticated the user", code= "unable_to_authenticated")
        if token_type != "Bearer":
            raise InvalidToken("token type is incorrect", code= "invalid_token")

        if raw_token:
            token = AccessToken(token=raw_token)
            user_id = token.payload.get(token_settings["USER_ID_CLAIM"])
        return user_id or None
