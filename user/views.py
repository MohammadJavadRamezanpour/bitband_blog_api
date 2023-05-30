from random import randint

from django.db.models import Q
from django.conf import settings

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
        elif user.has_perm(settings.USER_MANAGEMENT):
            return User.object.filter(is_staff=False)
        elif user.has_perm(settings.ARTICLE_MANAGEMENT):
            return User.object.filter(Q(groups__permissions__codename="user.author") | Q(user_permissions__codename="user.author"))
        else:
            return User.objects.filter(id=user.id)
        
    @action(detail=True, methods=['post'], permission_classes=[IsUserManager])
    def toggle_is_author(self, request, pk=None):
        user = self.get_queryset().get(pk=pk)
        user.is_author = not user.is_author
        user.save()
        return Response({"user": pk, "is_author": user.is_author}, status=200)


    @action(detail=False, methods=['post'])
    def get_otp(self, request):
        # HERE
        data = request.data
        phone = data.get("phone")

        try:
            user = User.object.get(phone=phone)
            user.otp = self.__generate_otp()
            self.__sms_otp(user)
            return Response({"msg": "otp sent"}, status=200)
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=200)
    
    def __generate_otp(self, k=5):
        chars = "0123456789"
        lst_opt = [chars[randint(0, len(chars)] for i in range(k)]
        return "".join(lst_opt)

    def __sms_otp(self, user):
        print("otp:", user.otp)
