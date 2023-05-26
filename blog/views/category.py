from rest_framework import viewsets

from blog.serializers import CategorySerializer
from blog.models import Category


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user

        # TODO: store these strings some where
        if user.has_perm('user.article_management'):
            return user.category.all()
        else:
            return Category.objects.all()
