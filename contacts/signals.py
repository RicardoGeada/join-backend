from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Contact     
        

@receiver(post_delete, sender=Contact)
def remove_contact_from_tasks(sender, instance, **kwargs):
    """
    Signal handler that is triggered after a Contact instance is deleted.

    This function removes the deleted contact from all tasks to which it was assigned.
    """
    tasks = instance.tasks.all()
    for task in tasks:
        task.assigned_to.remove(instance)