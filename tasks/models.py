from django.db import models

class Task(models.Model):
    """
    Task Model
    Defines the attributes of a task
    """
    PRIORITY_CHOICES = [
        (1, 'Urgent'),
        (2, 'Medium'),
        (3, 'Low'),
    ]
    
    CATEGORY_CHOICES = [
        ('Technical Task', 'Technical Task'),
        ('User Story', 'User Story'),
    ]
    
    STATUS_CHOICES = [
        ('to-do', 'To Do'),
        ('in-progress', 'In Progress'),
        ('await-feedback', 'Await Feedback'),
        ('done', 'Done'),
    ]
    
    status = models.CharField(choices=STATUS_CHOICES, default='to-do', max_length=20)
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    due_date = models.DateField()
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    assigned_to = models.JSONField(default=list)
    subtasks = models.JSONField(default=list)
    
