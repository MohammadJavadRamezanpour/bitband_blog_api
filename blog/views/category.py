from django.db.models import Q

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from blog.serializers import CategorySerializer
from blog.models import Category
from user.permissions import IsUserManager


class CategoryViewset(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        user = self.request.user

        # TODO: store these strings some where
        if user.has_perm('user.article_management'):
            return user.category.all()
        else:
            return Category.objects.all()
