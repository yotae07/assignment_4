from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def _create_user(self, name, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        user = self.model(name=name, **extra_fields)
        user.password = make_password(name)
        user.save(using=self._db)
        return user

    def create_user(self, name=None, **extra_fields):
        return self._create_user(name, **extra_fields)


class User(AbstractBaseUser):
    name = models.CharField(max_length=50, unique=True)
    USERNAME_FIELD = 'name'
    objects = CustomUserManager()
