from django.conf import settings

from rest_framework import viewsets

from blog.serializers import CategorySerializer
from blog.models import Category


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user

        if user.has_perm(settings.ARTICLE_MANAGEMENT):
            return user.categories.all()
        else:
            return Category.objects.all()
