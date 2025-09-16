from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from apps.core.schemas import login_schema, register_schema
from apps.core.serializers import LoginSerializer, RegisterSerializer
from apps.core.service.auth_serivce import AuthService as _service
from common.exceptions import (
    DatabaseSaveError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from common.responses import APIResponse


class AuthViewSet(ViewSet):
    @extend_schema(**register_schema)
    @action(methods=["post"], detail=False, url_path="register")
    def register(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            response = _service.signup(
                username=data["username"],
                email=data["email"],
                password=data["password"],
            )
            return response
        except UserAlreadyExistsError as e:
            return APIResponse.error(
                message=str(e.detail),
                status_code=e.status_code,
                code=e.default_code,
            )
        except DatabaseSaveError as e:
            return APIResponse.internal_error(
                message=str(e.detail),
                code=e.default_code,
            )
        except Exception as e:
            return APIResponse.internal_error(message=str(e))

    @extend_schema(**login_schema)
    @action(methods=["post"], detail=False, url_path="login")
    def login(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            response = _service.login(
                username=data["username"],
                password=data["password"],
            )
            return response
        except DatabaseSaveError as e:
            return APIResponse.internal_error(
                message=str(e.detail),
                code=e.default_code,
            )
        except InvalidCredentialsError as e:
            return APIResponse.error(
                message=str(e.detail),
                status_code=e.status_code,
                code=e.default_code,
            )
        except UserAlreadyExistsError as e:
            return APIResponse.error(
                message=str(e.detail),
                status_code=e.status_code,
                code=e.default_code,
            )
        except Exception as e:
            return APIResponse.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
