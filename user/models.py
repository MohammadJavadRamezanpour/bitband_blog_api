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
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    otp = models.CharField(max_length=5, blank=True, null=True)
    is_author = models.BooleanField(default=False)
    category = models.ManyToManyField("blog.Category")
    
    REQUIRED_FIELDS = ['phone']
    object = UserManager()