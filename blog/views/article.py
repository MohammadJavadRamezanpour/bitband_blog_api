from django.db.models import Q
from django.conf import settings

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from blog.serializers import ArticleReadSerializer, ArticleWriteSerializer
from blog.models import Article
from user.permissions import IsArticleManager, CanWriteOrReadOnly


class ArticleViewset(viewsets.ModelViewSet):
    permission_classes = (CanWriteOrReadOnly,)

    def get_serializer_context(self):
        return {"user": self.request.user}

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ArticleReadSerializer
        return ArticleWriteSerializer

    def get_queryset(self):
        user = self.request.user
        is_logged_in = user.is_authenticated

        if is_logged_in and user.is_superuser:
            return Article.objects.all()
        elif is_logged_in and user.is_article_manager:
            return Article.objects.filter(category__in=user.categories.all())
        elif is_logged_in and user.is_golden_user:
            return Article.objects.filter(
                Q(status=Article.VERIFIED, scope__in=settings.GOLDEN_CAN_SEE)
                | Q(author=user)
            )
        elif is_logged_in and user.is_silver_user:
            return Article.objects.filter(
                Q(status=Article.VERIFIED, scope__in=settings.SILVER_CAN_SEE)
                | Q(author=user)
            )
        elif is_logged_in and user.is_bronze_user:
            return Article.objects.filter(
                Q(status=Article.VERIFIED, scope__in=settings.BRONZE_CAN_SEE)
                | Q(author=user)
            )
        else:
            return Article.objects.filter(
                Q(status=Article.VERIFIED, scope__in=settings.NORMAL_CAN_SEE)
                | Q(author=user)
            )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
