from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Subtask
from tasks.models import Task
from users.models import CustomUser
from rest_framework.authtoken.models import Token

# Create your tests here.

class SubtaskAPITests(APITestCase):
    
    def setUp(self):
        # setup tasks
        self.task1 = Task.objects.create(title='Task1', status='to-do', description='Description Task1', priority=1, due_date='2030-07-22', category='Technical Task')
        self.task2 = Task.objects.create(title='Task2', status='to-do', description='Description Task2', priority=2, due_date='2030-07-22', category='Technical Task')
        
        # authenticate
        self.user = CustomUser.objects.create_user(email='user@mail.com', username='user', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    
    def test_user_can_create_subtask(self):
        """
        Ensure user can create a subtask for a task.
        """
        url = reverse('subtask-list')
        data = {
            'description' : 'This is a subtask.',
            'task' : self.task1.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    
    def test_user_can_get_subtasks(self):
        """
        Ensure user can get all subtasks.
        """
        subtask1 = Subtask.objects.create(task=self.task1,description='Subtask1')
        subtask2 = Subtask.objects.create(task=self.task2,description='Subtask2')
        
        url = reverse('subtask-list')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subtask.objects.count(), 2)
        subtask_ids = [subtask['id'] for subtask in response.data]
        self.assertIn(subtask1.id, subtask_ids)
        self.assertIn(subtask2.id, subtask_ids)
        
    
    def test_user_can_get_subtask_detail(self):
        """
        Ensure user can get specific subtask.
        """
        subtask1 = Subtask.objects.create(task=self.task1,description='Subtask1')   
        url = reverse('subtask-detail', kwargs={'pk' : subtask1.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], subtask1.description)
        self.assertEqual(response.data['is_done'], subtask1.is_done)
        self.assertEqual(response.data['task'], subtask1.task.pk)
        
    
    def test_user_can_edit_subtask(self):
        """
        Ensure user can edit subtask.
        """
        subtask1 = Subtask.objects.create(task=self.task1,description='Subtask1')   
        url = reverse('subtask-detail', kwargs={'pk' : subtask1.pk})
        updated_data = {
            'description' : 'Updated Description',
            'is_done' : True,
            'task' : self.task2.pk 
        }
        
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        subtask1.refresh_from_db()
        
        self.assertEqual(subtask1.description, updated_data['description'])
        self.assertEqual(subtask1.is_done, updated_data['is_done'])
        self.assertNotEqual(subtask1.task.pk, updated_data['task']) # can't change the assigned task
        self.assertEqual(subtask1.task.pk, self.task1.pk)
        

    def test_user_can_delete_subtask(self):
        """
        Ensure user can delete a subtask.
        """
        subtask1 = Subtask.objects.create(task=self.task1, description='Subtask1')
        url = reverse('subtask-detail', kwargs={'pk' : subtask1.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subtask.objects.count(), 0)
        
    
    def test_subtasks_get_deleted_when_task_gets_deleted(self):
        """
        Ensure subtasks get deleted when task gets deleted.
        """
        subtask1 = Subtask.objects.create(task=self.task1, description='Subtask1')
        subtask2 = Subtask.objects.create(task=self.task1, description='Subtask2')
        self.assertIn(subtask1 ,self.task1.subtasks.all())
        self.assertIn(subtask2 ,self.task1.subtasks.all())
        
        self.task1.delete()
        
        self.assertEqual(Subtask.objects.filter(id=subtask1.pk).first(), None)
        self.assertEqual(Subtask.objects.filter(id=subtask2.pk).first(), None)
        self.assertEqual(Subtask.objects.filter(task=self.task1.pk).first(), None)
        self.assertEqual(Task.objects.filter(pk=self.task1.pk).first(), None)
        
