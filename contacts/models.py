from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser

# Create your models here.
class Contact(models.Model):
    
    name = models.CharField(max_length=100)
    initials = models.CharField(max_length=2)
    email = models.EmailField() 
    phone = models.CharField(max_length=15, blank=True, null=True)
    badge_color = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(15)], default=1)
    active_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='contact') 
    