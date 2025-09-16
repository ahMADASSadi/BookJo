from drf_spectacular.utils import OpenApiResponse

from apps.core.serializers import LoginSerializer, RegisterSerializer

register_schema = {
    "summary": "Register a new user",
    "description": "Creates a new user account with the provided username, email, and password.",
    "request": RegisterSerializer,
    "responses": {
        201: OpenApiResponse(
            description="User registered successfully.",
            response=None,
        ),
        400: OpenApiResponse(description="Validation error or user already exists."),
        500: OpenApiResponse(description="Internal server error."),
    },
    "tags": ["Authentication"],
    "operation_id": "registerUser",
}

login_schema = {
    "summary": "Login a user",
    "description": "Authenticates a user with the provided username and password.",
    "request": LoginSerializer,
    "responses": {
        200: OpenApiResponse(
            description="User logged in successfully.",
            response=None,
        ),
        400: OpenApiResponse(description="Invalid credentials or validation error."),
        500: OpenApiResponse(description="Internal server error."),
    },
    "tags": ["Authentication"],
    "operation_id": "loginUser",
}
