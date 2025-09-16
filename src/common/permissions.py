from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    Read-only permissions are allowed for any request (authenticated or not).
    """

    def has_permission(self, request, view):
        # Allow read-only methods (GET, HEAD, OPTIONS) for everyone.
        if request.method in SAFE_METHODS:
            return True

        # For write methods, check if the user is a staff member.
        # This works safely for AnonymousUser, as request.user.is_staff will be False.
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to staff members.
        return request.user and request.user.is_staff
