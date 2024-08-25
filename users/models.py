from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser, PermissionsMixin
from .utils import generate_initials

class CustomUserManager(BaseUserManager):
    """
    Manager for the CustomUser model, handling user creation and management.

    Methods:
        create_user(email, password=None, username=None, **extra_fields):
            Creates and returns a regular user with an email, password and username.

        create_superuser(email, password=None, username=None, **extra_fields):
            Creates and returns a superuser with the given email, password and username.
    """
    
    def create_user(self, email, password=None, username=None, **extra_fields):
        """
        Create and return a regular user with an email, username, and password.

        Returns:
            CustomUser: The created user instance.
        """
        if not email:
            raise ValueError("The given email must be set")
        if not username:
            raise ValueError("The given username must be set")
        if not password:
            raise ValueError("The given password must be set")
        initials = generate_initials(username=username)
        user = self.model(email=self.normalize_email(email), username=username, initials=initials, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, username=None, **extra_fields):
        """
        Create and return a superuser with the given email, username, and password.

        Returns:
            CustomUser: The created superuser instance.
        """
        user = self.create_user(email=email, password=password, username=username, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for authentication.

    Attributes:
        username (str): The username of the user.
        initials (str): Initials derived from the username.
        phone (str): The phone number of the user.
        email (str): The email address of the user.
        is_active (bool): Indicates whether the user account is active.
        is_staff (bool): Indicates whether the user can access the admin site.
    
    Methods:
        save(*args, **kwargs):
            Updates the initials based on the username before saving the user.
    """
    
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
        """
        Override save method to update the user's initials based on their username.
        """
        self.initials = generate_initials(self.username)
        super().save(*args, **kwargs)
        