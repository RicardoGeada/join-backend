from django.db import models
from tasks.models import Task

# Create your models here.
class Subtask(models.Model):
    
    is_done = models.BooleanField(default=False)
    description = models.TextField(max_length=200)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')