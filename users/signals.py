from django.db.models.signals import post_save
from django.dispatch import receiver
from contacts.models import Contact
from .models import CustomUser
import random

@receiver(post_save, sender=CustomUser)
def create_user_contact(sender, instance, created, **kwargs):
    if created:
        Contact.objects.create(name=instance.username, email=instance.email, initials=instance.initials, badge_color=random.randint(1,15), active_user=instance)
        
