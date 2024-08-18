from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser, PermissionsMixin
from .utils import generate_initials

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password=None, username=None, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        if not username:
            raise ValueError("The given username must be set")
        initials = generate_initials(username=username)
        user = self.model(email=self.normalize_email(email), username=username, initials=initials, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, username=None, **extra_fields):
        user = self.create_user(email=email, password=password, username=username, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=False)
    initials = models.CharField(max_length=5, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        self.initials = generate_initials(self.username)
        super().save(*args, **kwargs)
        