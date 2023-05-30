from random import randint

from django.db.models import Q
from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken

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

    @action(detail=False, methods=['POST'])
    def register(self, request):
        phone = request.data.get("phone")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")

        try:
            user = User.object.create(phone=phone, first_name=first_name, last_name=last_name, otp=self.__generate_otp())
            self.__sms_otp(user)
            return Response({"msg": "Please send the otp sent to your phone number"}, status=200)
        except User.DoesNotExist:
            return Response({"error": "wrong otp or phone number"}, status=400)
        
    @action(detail=False, methods=['POST'])
    def verify_the_user(self, request):
        phone = request.GET.get("phone")
        otp = request.data.get("otp")

        try:
            user = User.object.get(phone=phone, otp=otp)
            user.is_active = True
            user.save()
            print("user saved")
            return Response({"msg": f"user with phone number {user.phone} activated, you can login now"}, status=200)
        except User.DoesNotExist:
            return Response({"error": "wrong otp or phone number"}, status=400)
        
    @action(detail=False, methods=['GET'])
    def get_otp(self, request):
        phone = request.GET.get("phone")

        try:
            user = User.object.get(phone=phone, is_active=True)
            user.otp = self.__generate_otp()
            user.save()
            self.__sms_otp(user)
            return Response({"msg": "otp sent"}, status=200)
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=400)
        
    @action(detail=False, methods=['POST'])
    def send_otp(self, request):
        phone = request.GET.get("phone")
        otp = request.data.get("otp")

        try:
            user = User.object.get(phone=phone, otp=otp, is_active=True)
            tokens = self.__get_tokens_for_user(user)
            return Response(tokens, status=200)
        except User.DoesNotExist:
            return Response({"error": "wrong otp or phone number"}, status=400)
    
    def __generate_otp(self, k=5):
        chars = "0123456789"
        lst_opt = [chars[randint(0, len(chars)-1)] for _ in range(k)]
        return "".join(lst_opt)

    def __sms_otp(self, user):
        print("otp:", user.otp)

    def __get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
