from django.conf import settings

from rest_framework import serializers

from blog.models import Article
from .category import CategorySerializer


class ArticleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    author = serializers.SerializerMethodField()
    scope = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_author(self, obj):
        from user.serializers import ReadUserSerializer

        return ReadUserSerializer(obj.author, context=self.context).data

    get_scope = lambda self, obj: obj.get_scope_display()
    get_status = lambda self, obj: obj.get_status_display()

    class Meta:
        model = Article
        fields = (
            "pk",
            "title",
            "body",
            "author",
            "status",
            "scope",
            "category",
            "created_at",
            "updated_at",
        )


class ArticleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = (
            "title",
            "body",
            "status",
            "scope",
            "category",
        )

    def get_fields(self):
        fields = super().get_fields()
        allowd_fields = ("title", "body", "scope", "category")
        user = self.context["user"]

        if not user.is_article_manager:
            for field in fields.copy():
                if not field in allowd_fields:
                    fields.pop(field)

        return fields

    def validate_category(self, category):
        user = self.context.get("user")

        if category in user.categories.all():
            return category
        raise serializers.ValidationError("create article in your own category")

    def validate_status(self, status):
        user = self.context.get("user")

        if user.has_perm(settings.ARTICLE_MANAGEMENT):
            return status
        raise serializers.ValidationError("you can't change the status")
