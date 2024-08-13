from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Contact

@receiver(post_delete, sender=Contact)
def delete_user_when_contact_deleted(sender, instance, **kwargs):
    if instance.active_user:
        instance.active_user.delete()