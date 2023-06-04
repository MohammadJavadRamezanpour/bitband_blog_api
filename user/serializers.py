from rest_framework import serializers
from .models import User
from blog.serializers import CategorySerializer


class UserSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    otp = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "categories",
            "otp",
        )


class CreateUserSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "first_name",
            "last_name",
            "is_active",
            "is_author",
            "categories",
            "otp",
        )


class ModifyUserSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True, required=False, allow_null=True)
    username = serializers.CharField(required=False)

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
            raise serializers.ValidationError("this username already exists")
        except User.DoesNotExist:
            return username

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "is_author",
            "is_active",
            "categories",
            "otp",
            "groups",
        )


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "phone", "first_name", "last_name")
