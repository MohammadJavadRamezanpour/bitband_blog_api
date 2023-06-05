from rest_framework import serializers
from .models import User
from blog.serializers import CategorySerializer


class ReadUserSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

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
            "groups",
        )

    def get_fields(self):
        fields = super().get_fields()
        user = self.context["user"]
        exclude = ["groups"]

        if not user.is_manager:
            for exclude_this in exclude:
                fields.pop(exclude_this)
        
        return fields


class CreateUserSerializer(serializers.ModelSerializer):
    otp = serializers.CharField(write_only=True, allow_null=True)

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
            "groups",
        )




class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "phone", "first_name", "last_name")
