from rest_framework import status  # type: ignore
from rest_framework.exceptions import APIException  # type: ignore


class UserAlreadyExistsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A user already exists."
    default_code = "user_already_exists"


class UserNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "User does not exist."
    default_code = "user_not_found"


class InvalidCredentialsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid phone number or password."
    default_code = "invalid_credentials"


class ObjectNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "No object found"
    default_code = "object_not_found"


class DeletionPermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You do not have permission to delete this file."
    default_code = "permission_denied"


class DatabaseSaveError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Could not save the changes to the database."
    default_code = "database_error"


class NoQueryParameterError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "No query parameter provided"
    default_code = "no_query_parameter"
