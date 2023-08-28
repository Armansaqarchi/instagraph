from rest_framework.exceptions import APIException
from django.http import Http404
from rest_framework import exceptions
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import set_rollback
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import InvalidToken


def handle_exception(exc, context):
    print("ddddddddddd", exc)
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, AuthenticationFailed):
        exc.detail = "failed to Authenticate user"
    elif isinstance(exc, InvalidToken):
        exc.detail = "Token is invalid or maybe expired"


    detail = getattr(exc, "detail", None)
    code = getattr(exc, "default_code", None)
    status_code = getattr(exc, "status_code", None)
    data = {"Message" : detail, "Code" : code, "Status" : "Error"}
    errors = context.get("kwargs")
    if errors:
        data.update(errors)
    # rolling back all the changes made before the exception occured
    # this might work if ATORMIC_REQUESTS is set in inner database configuration
    set_rollback()
    return Response(data, status=status_code, exception=True)



class UnauthorizedException(APIException):
    status_code = 401
    def __init__(self, message = "you are refused to access this page", code="not_authorized"):
        self.default_code = code
        super().__init__(message, "ACCESS DENIED")

class BadRequestException(APIException):
    status_code = 400

    def __init__(self, message = "BAD REQUEST", code="bad_request"):
        self.default_code = code
        super().__init__(message, "400 BAD REQUEST")


class NotFoundException(APIException):
    status_code = 404

    def __init__(self, message = "page not found", code="not_found"):
        self.default_code = code
        super().__init__(message, "404 NOT FOUND")

class AlreadyExistsException(APIException):
    status_code = 409

    def __init__(self, message = "the object already exists", code="already_exists"):
        self.default_code = code
        super().__init__(message, "409 CONFLICT ERROR")

class ForibiddenException(APIException):
    status_code = 403

    def __init__(self, message = "this page is forbidden", code="forbidden"):
        self.default_code = code
        super().__init__(message, "403 FORBIDDEN")