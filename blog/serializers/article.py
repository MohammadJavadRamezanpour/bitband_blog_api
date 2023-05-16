from rest_framework import serializers
from blog.models import Article
from .category import CategorySerializer
from user.serializers import SimpleUserSerializer, UserSerializer


class ArticleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    author = serializers.SerializerMethodField()

    def get_author(self, obj):
        user = self.context['user']

        if user.is_staff:
            return UserSerializer(obj.author).data
        
        return SimpleUserSerializer(obj.author).data
        

    class Meta:
        model = Article
        fields = ("title", "body", "author",
                  "status", "scope", "category",
                  "created_at", "updated_at")

class ArticleWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("title", "body", "author",
                  "scope", "category",)
