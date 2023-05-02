from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Allows access only to admin users. or read-only
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
    

class IsUserManager(BasePermission):
    """
    Allows access only to user managers.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.has_perm('user.user_management'))