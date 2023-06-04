from random import choices

from django.db.models import Q
from django.conf import settings

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, ModifyUserSerializer, CreateUserSerializer
from .models import User
from .permissions import IsUserManager


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsUserManager,)

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ModifyUserSerializer
        elif self.request.method == "POST":
            return CreateUserSerializer
        else:
            return UserSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return User.objects.all()
        elif user.has_perm(settings.USER_MANAGEMENT):
            return User.objects.filter(is_staff=False)
        elif user.has_perm(settings.ARTICLE_MANAGEMENT):
            return User.objects.filter(
                Q(groups__permissions__codename="user.author")
                | Q(user_permissions__codename="user.author")
            )
        else:
            return User.objects.filter(id=user.id)

    @action(detail=True, methods=["PUT", "PATCH"], permission_classes=[IsUserManager])
    def make_author(self, request, pk=None):
        user = self.get_object()
        categories = request.data.get("categories", [])

        data = dict(is_author=True, categories=categories)

        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=200)

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def register(self, request):
        request.data["username"] = User.get_random_username()
        request.data["otp"] = self.__generate_otp()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        self.__sms_otp(instance)

        return Response(
            {"msg": "Please send the otp sent to your phone number"}, status=200
        )

    @action(detail=False, methods=["PUT", "PATCH"], permission_classes=[AllowAny])
    def verify_the_user(self, request):
        phone = request.GET.get("phone")
        otp = request.data.get("otp")
        data = dict(is_active=True, otp=None)

        try:
            user = User.objects.get(phone=phone, otp=otp)
            serializer = self.get_serializer(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

            return Response(
                {
                    "msg": f"user with phone number {instance.phone} activated, you can login now"
                },
                status=200,
            )
        except User.DoesNotExist:
            return Response({"error": "wrong otp or phone number"}, status=400)

    @action(detail=False, methods=["GET"], permission_classes=[AllowAny])
    def get_otp(self, request):
        phone = request.GET.get("phone")
        data = dict(otp=self.__generate_otp())
        try:
            user = User.objects.get(phone=phone, is_active=True)
            serializer = self.get_serializer(user, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            self.__sms_otp(user)
            return Response({"msg": "otp sent"}, status=200)
        except User.DoesNotExist:
            return Response({"error": "user not found"}, status=400)

        return Response(
            {"msg": "Please send the otp sent to your phone number"}, status=200
        )

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def send_otp(self, request):
        phone = request.GET.get("phone")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(phone=phone, otp=otp, is_active=True)
            tokens = self.__get_tokens_for_user(user)
            self.__flush_otp(user)
            return Response(tokens, status=200)
        except User.DoesNotExist:
            return Response({"error": "wrong otp or phone number"}, status=400)

    def __generate_otp(self, k=5):
        chars = "0123456789"
        lst_opt = choices(chars, k=k)
        return "".join(lst_opt)

    def __sms_otp(self, user):
        print("otp:", user.otp)

    def __get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def __flush_otp(self, user):
        data = dict(otp=None)
        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
