from django.db import models
from contacts.models import Contact

class Task(models.Model):
    """
    Represents a task with various attributes.

    Attributes:
        status (str): Current status of the task (choices: 'to-do', 'in-progress', 'await-feedback', 'done').
        title (str): Title of the task.
        description (str): Detailed description of the task.
        priority (int): Priority level (choices: 1 for Urgent, 2 for Medium, 3 for Low).
        due_date (date): Due date for task completion.
        category (str): Category of the task (choices: 'Technical Task', 'User Story').
        assigned_to (ManyToManyField): Contacts assigned to the task.
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
    assigned_to = models.ManyToManyField(Contact, related_name='tasks', blank=True)
    
