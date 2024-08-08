from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=False)
    # first_name = models.CharField(max_length=100, blank=True, null=True)
    # last_name = models.CharField(max_length=100, blank=True, null=True)
    initials = models.CharField(max_length=5, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    # contacts = models.ManyToManyField(Contact, blank=True)
    email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()