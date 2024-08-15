from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Task
from users.models import CustomUser

# Create your tests here.

class SubtaskAPITests(APITestCase):
    
    def setUp(self):
        # setup tasks
        self.task1 = Task.objects.create(title='Task1', status='to-do', description='Description Task1', priority=1, due_date='2030-07-22', category='Technical Task')
        self.task2 = Task.objects.create(title='Task2', status='to-do', description='Description Task2', priority=2, due_date='2030-07-22', category='Technical Task')
        
        # authenticate
        self.user = CustomUser.objects.create_user(email='user@mail.com', username='user', password='password', initials='US')
        self.client.login(email='user@mail.com', password='password')

    # setup
    def test_user_can_create_subtask(self):
        """
        Ensure user can create a subtask for a task.
        """
        url = reverse('subtask-list')
        data = {
            'description' : 'This is a subtask.',
            'task' : self.task1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    
    def test_user_can_get_subtasks(self):
        """
        
        """
        
    # test_user_can_get_subtasks
    # test_user_can_get_subtask_detail
    # test_user_can_edit_subtask
    # test_user_can_delete_subtask
