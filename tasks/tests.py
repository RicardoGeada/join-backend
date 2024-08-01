from django.test import TestCase
from .models import Task

class TaskModelTest(TestCase):
    
    def test_task_model_exists(self):
        tasks_count = Task.objects.count()
        self.assertEqual(tasks_count, 0)