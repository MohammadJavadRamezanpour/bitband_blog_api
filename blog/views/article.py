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

        NORMAL_CAN_SEE = [settings.NORMAL]
        BRONZE_CAN_SEE = NORMAL_CAN_SEE + [settings.BRONZE]
        SILVER_CAN_SEE = BRONZE_CAN_SEE + [settings.SILVER]
        GOLDEN_CAN_SEE = SILVER_CAN_SEE + [settings.GOLDEN]

        if is_logged_in and user.is_superuser:
            return Article.objects.all()
        elif is_logged_in and user.has_perm(settings.ARTICLE_MANAGEMENT):
            return Article.objects.filter(category__in=user.categories.all())
        elif is_logged_in and user.has_perm(settings.GOLDEN):
            return Article.objects.filter(
                Q(status=Article.VERIFIED, scope__in=GOLDEN_CAN_SEE) | Q(author=user)
            )
        elif is_logged_in and user.has_perm(settings.SILVER):
            return Article.objects.filter(
                Q(status=Article.VERIFIED, scope__in=SILVER_CAN_SEE) | Q(author=user)
            )
        elif is_logged_in and user.has_perm(settings.BRONZE):
            return Article.objects.filter(
                Q(status=Article.VERIFIED, scope__in=BRONZE_CAN_SEE) | Q(author=user)
            )
        else:
            return Article.objects.filter(
                Q(status=Article.VERIFIED, scope__in=NORMAL_CAN_SEE)
            )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True, methods=["PATCH", "PUT"], permission_classes=(IsArticleManager,)
    )
    def verify(self, request, pk=None):
        article = self.get_object()

        data = dict(status=Article.VERIFIED)

        serializer = self.get_serializer(article, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"msg": "Done"}, status=200)

    @action(
        detail=True, methods=["PATCH", "PUT"], permission_classes=(IsArticleManager,)
    )
    def reject(self, request, pk=None):
        article = self.get_object()

        data = dict(status=Article.REJECTED)

        serializer = self.get_serializer(article, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"msg": "Done"}, status=200)
