from .views import ArticleViewset, CategoryViewset
from rest_framework import routers

router = routers.DefaultRouter()

router.register('category', CategoryViewset, basename='category')
router.register('', ArticleViewset, basename='articles')

urlpatterns = router.urls
