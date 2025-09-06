from django.db import models

# Create your models here.
from django.contrib.auth.base_user import *
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth import get_user_model

# User=get_user_model()

class CustomUserManager(BaseUserManager):
    def create_user(self,username,password=None,**extra_fields):
        if not username:
            return  ValueError('User kiritish shart!')
        user=self.model(username=username,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,password,**extra_fields):
        extra_fields.setdefault('is_admin',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_admin') is not True:
            return ValueError("Sizda is_admin==True b'olishi kerak")
        if extra_fields.get('is_active') is not True:
            return ValueError()

        return  self.create_user(username,password,**extra_fields)
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    @property
    def is_superuser(self):
        return self.is_admin