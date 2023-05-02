from django.db.models import Q

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .serializers import UserSerializer
from .models import User
from .permissions import IsUserManager


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return User.object.all()
        elif user.has_perm('user.user_management'):
            return User.object.filter(is_staff=False)
        elif user.has_perm('user.article_management'):
            return User.object.filter(Q(groups__permissions__codename="user.author") | Q(user_permissions__codename="user.author"))
        else:
            return User.objects.filter(id=user.id)
        
    @action(detail=True, methods=['post'], permission_classes=[IsUserManager])
    def toggle_is_author(self, request, pk=None):
        user = self.get_queryset().get(pk=pk)
        user.is_author = not user.is_author
        user.save()
        return Response({"user": pk, "is_author": user.is_author}, status=200)