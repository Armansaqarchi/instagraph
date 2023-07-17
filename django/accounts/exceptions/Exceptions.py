from rest_framework.exceptions import APIException


class UnauthorizedException(APIException):
    status_code = 401
    def __init__(self, message = "you are refused to access this page"):
        super().__init__(message, "ACCESS DENIED")


class BadRequestException(APIException):
    status_code = 400

    def __init__(self, message = "BAD REQUEST"):
        super().__init__(message, "400 BAD REQUEST")


class NotFoundException(APIException):
    status_code = 404

    def __init__(self, message = "page not found"):
        super().__init__(message, "404 NOT FOUND")

class AlreadyExistsException(APIException):
    status_code = 409

    def __init__(self, message = "the object already exists"):
        super().__init__(message, "409 CONFLICT ERROR")

class ForibiddenException(APIException):
    status_code = 403

    def __init__(self, message = "this page is forbidden"):
        super().__init__(message, "403 FORBIDDEN")