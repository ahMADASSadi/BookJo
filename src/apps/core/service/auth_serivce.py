from typing import Any

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from common.exceptions import (
    DatabaseSaveError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from common.responses import APIResponse

User = get_user_model()


class AuthService:
    refresh_token_expiry = settings.SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME")
    access_token_expiry = settings.SIMPLE_JWT.get("ACCESS_TOKEN_LIFETIME")

    @classmethod
    def set_http_cookies(cls: "AuthService", tokens: tuple[str, str]) -> Response:
        access, refresh = tokens[0], tokens[1]

        response = APIResponse.success(
            message="OTP verified successfully.",
            data={
                "access": access,
                "refresh": refresh,
            },
        )

        response.set_cookie(
            key="refresh",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=cls.refresh_token_expiry,
        )
        response.set_cookie(
            key="access",
            value=access,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=cls.access_token_expiry,
        )
        return response

    @classmethod
    def generate_tokens(cls: "AuthService", user: User) -> tuple[str, str]:
        """generate_tokesn take the user and returns the refresh and access tokens

        Args:
            user (User): request user

        Returns:
            tuple[str, str]: access and refresh token
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token), str(refresh)

    @classmethod
    def signup(
        cls: "AuthService",
        username: str,
        email: str,
        password: str,
        **extra_fields: Any,
    ) -> Response:
        """signup takes the user credentials and sign the user up if not exists

        Args:
            username (str): username
            email (str): email
            password (str): password

        Raises:
            ValidationError: if the user already exists

        Returns:
            Response(HttpResponse): sets the cookies if the user and tokens are created
        """
        if User.objects.filter(username=username).exists():
            raise UserAlreadyExistsError

        try:
            user = User.objects.create_user(
                username=username, email=email, password=password, **extra_fields
            )
        except Exception as exc:
            raise DatabaseSaveError from exc

        return cls.set_http_cookies(cls.generate_tokens(user))

    @classmethod
    def login(cls: "AuthService", username: str, password: str) -> Response:
        try:
            user = authenticate(username=username, password=password)
            if user is None:
                raise InvalidCredentialsError("Invalid phone number or password.")
            try:
                cls.update_user_login(user)
            except DatabaseSaveError:
                raise

        except InvalidCredentialsError:
            raise

        except Exception as exc:
            raise DatabaseSaveError from exc

        return cls.set_http_cookies(cls.generate_tokens(user))

    @classmethod
    def update_user_login(cls: "AuthService", user: User):
        try:
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])

        except Exception as exc:
            raise DatabaseSaveError("Could not update user's last login.") from exc
