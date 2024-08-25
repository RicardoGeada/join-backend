from django.db import models
from tasks.models import Task

# Create your models here.
class Subtask(models.Model):
    """
    Represents a subtask associated with a Task.

    Attributes:
        is_done (bool): Indicates whether the subtask is completed. Defaults to False.
        description (str): A brief description of the subtask, with a maximum length of 200 characters.
        task (Task): The task to which this subtask is linked. Deleting the task will delete all its subtasks.
    """
    
    is_done = models.BooleanField(default=False)
    description = models.TextField(max_length=200)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')