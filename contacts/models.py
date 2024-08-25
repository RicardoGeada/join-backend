from typing import Any
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser
from users.utils import generate_initials
import random

# Create your models here.
class Contact(models.Model):
    
    name = models.CharField(max_length=100)
    initials = models.CharField(max_length=2, blank=True, null=True)
    email = models.EmailField() 
    phone = models.CharField(max_length=15, blank=True, null=True)
    badge_color = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(14)], blank=True)
    active_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='contact') 
    
    
    def __str__(self):
        return self.name
    
    
    def save(self, *args, **kwargs):
        if not self.pk:  # only for creation
            self.badge_color = random.randint(0, 14)
        self.initials = generate_initials(self.name)
        super().save(*args, **kwargs)
    
    
    def delete(self, *args, **kwargs):
        if self.active_user:
            self.active_user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)
    