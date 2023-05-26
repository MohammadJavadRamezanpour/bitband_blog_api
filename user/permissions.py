from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Allows access only to admin users. or read-only
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and request.user.is_staff)


class IsUserManager(BasePermission):
    """
    Allows access only to user managers.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.has_perm('user.user_management'))


class IsArticleManager(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.has_perm('poai.article_management'))


class IsArticleManagerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and request.user.has_perm('poai.article_management'))


class IsAuthorOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and request.user.is_author)


class CanWriteOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        is_author_or_readonly = IsAuthorOrReadOnly()
        is_article_manager_or_readonly = IsArticleManagerOrReadOnly()
        if request.method in SAFE_METHODS:
            return True

        return bool(is_author_or_readonly.has_permission(request, view) or is_article_manager_or_readonly.has_permission(request, view))
