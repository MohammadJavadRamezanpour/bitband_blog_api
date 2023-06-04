from rest_framework import serializers
from blog.models import Article
from .category import CategorySerializer


class ArticleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    author = serializers.SerializerMethodField()
    scope = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_author(self, obj):
        from user.serializers import SimpleUserSerializer, UserSerializer

        user = self.context["user"]

        if user.is_staff:
            return UserSerializer(obj.author).data

        return SimpleUserSerializer(obj.author).data

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
    def validate_category(self, obj):
        user = self.context.get("user")

        if obj in user.categories.all():
            return obj
        raise serializers.ValidationError("create article in your own category")

    class Meta:
        model = Article
        fields = (
            "title",
            "body",
            "status",
            "scope",
            "category",
        )
