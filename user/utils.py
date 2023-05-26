from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from user.models import User


def create_permissions():
    content_type = ContentType.objects.get_for_model(User)

    for permission_key in settings.PERMISSIONS:
        for perm_key, perm_value in settings.PERMISSIONS[permission_key].items():
            Permission.objects.get_or_create(
                codename=perm_key, name=perm_value, content_type=content_type)
