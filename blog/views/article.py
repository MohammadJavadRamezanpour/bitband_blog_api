from django.db.models import Q

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from blog.serializers import ArticleReadSerializer, ArticleWriteSerializer
from blog.models import Article
from user.permissions import IsUserManager


class ArticleViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, )

    def get_serializer_context(self):
        return {
            "user": self.request.user
        }

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ArticleReadSerializer
        else:
            return ArticleWriteSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Article.objects.all()
        # TODO: store these strings some where
        elif user.has_perm('user.article_management'):
            return Article.objects.filter(category=user.category)
        elif user.has_perm('user.is_gold'):
            return Article.objects.filter(status=Article.VERIFIED)
        elif user.has_perm('user.is_silver'):
            return Article.objects.filter(status=Article.VERIFIED, scope__in=[Article.BRONZE, Article.SILVER])
        elif user.has_perm('user.is_bronze'):
            return Article.objects.filter(status=Article.VERIFIED, scope=Article.BRONZE)
        elif user.is_author:
            # TODO: a user can be an author too
            return Article.objects.filter(author=user)
