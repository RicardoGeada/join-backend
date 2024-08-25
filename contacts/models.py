from typing import Any
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser
from users.utils import generate_initials
import random

# Create your models here.
class Contact(models.Model):
    """
    Represents a contact with personal information, including name, email, phone number, 
    badge color, and a relationship to an active user.

    Attributes:
        name (str): The name of the contact.
        initials (str): The initials of the contact, automatically generated based on the name.
        email (str): The email address of the contact.
        phone (str): The phone number of the contact.
        badge_color (int): An integer representing the badge color, randomly assigned at creation.
        active_user (CustomUser): A one-to-one relationship with the active user associated with this contact.
    """
    
    name = models.CharField(max_length=100)
    initials = models.CharField(max_length=2, blank=True, null=True)
    email = models.EmailField() 
    phone = models.CharField(max_length=15, blank=True, null=True)
    badge_color = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(14)], blank=True)
    active_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='contact') 
    
    
    def __str__(self):
        """
        Returns the string representation of the contact, which is the contact's name.

        Returns:
            str: The name of the contact.
        """
        return self.name
    
    
    def save(self, *args, **kwargs) -> None:
        """
        Overrides the save method to automatically generate initials based on the name 
        and randomly assign a badge color upon the creation of a new contact.
        """
        if not self.pk:  # only for creation
            self.badge_color = random.randint(0, 14) # Assign a random badge color between 0 and 14
        self.initials = generate_initials(self.name) # Generate initials based on the contact's name
        super().save(*args, **kwargs)
    
    
    def delete(self, *args, **kwargs) -> None:
        """
        Overrides the delete method to ensure that the associated active user is also deleted 
        when a contact is removed.
        """
        if self.active_user:
            self.active_user.delete() # Delete the associated active user
        return super(self.__class__, self).delete(*args, **kwargs)
    