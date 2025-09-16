from typing import Dict, List, Optional, Type

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.permissions import BasePermission
from rest_framework.serializers import Serializer

from common.exceptions import (
    DatabaseSaveError,
    DeletionPermissionDenied,
    ObjectNotFoundError,
)
from common.permissions import IsAdminOrReadOnly
from common.responses import APIResponse

User = get_user_model()


class ViewSetMixin:
    action_serializer_class: Dict[str, Type[Serializer]] = {
        "list": None,
        "retrieve": None,
        "create": None,
        "update": None,
        "partial_update": None,
    }
    default_serializer_class: Optional[Type[Serializer]] = None
    permission_classes: List[Type[BasePermission]] = [IsAdminOrReadOnly]
    default_serializer_class = None

    def get_user(self) -> User:
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.get_user()
        return context

    def get_serializer_class(self) -> Type[Serializer]:
        return self.action_serializer_class.get(
            self.action, self.default_serializer_class
        )

    def destroy(self, request, *args, **kwargs):
        """Implements a soft delete by setting the `deleted_at` field."""
        try:
            instance = self.get_object()
            instance.deleted_at = timezone.now()
            instance.save()
            return APIResponse.no_content()
        except (DeletionPermissionDenied, DatabaseSaveError, ObjectNotFoundError) as e:
            return APIResponse.error(errors=e, code=e.status_code)
