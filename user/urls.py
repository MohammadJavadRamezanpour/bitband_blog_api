from .views import UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register("", UserViewSet, basename="users")

urlpatterns = router.urls