from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser


class UserManager(BaseUserManager):
    def create_user(self, phone, username, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError("Users must have a phone")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            phone=phone,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone, password):
        """
        Creates and saves a superuser with the given phone and password.
        """
        user = self.create_user(phone, username, password)
        user.is_staff = True # to login into dashboard
        user.is_superuser = True # to access models, for has_perm method
        user.save(using=self._db) 
        return user


class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    otp = models.CharField(max_length=5, blank=True, null=True)
    is_author = models.BooleanField(default=False)
    category = models.ManyToManyField("blog.Category", null=True, blank=True)

    REQUIRED_FIELDS = ['phone']
    object = UserManager()

    def has_perm(self, perm, obj=None):
        if super().has_perm(perm, obj):
            return True
        
        return self.groups.filter(permissions__codename=perm).exists()
 
    def __str__(self):
        return str(self.phone)