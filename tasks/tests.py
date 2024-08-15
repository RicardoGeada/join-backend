from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from .models import Task

class TaskModelTest(TestCase):  
    def test_task_model_exists(self):
        tasks = Task.objects.count()
        self.assertEqual(tasks, 0)
        
class BaseAPITestCase(APITestCase):  
    def setUp(self):
        self.client = APIClient()

    def authenticate(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', email='test@mail.de')
        self.client.login(email='test@mail.de', password='testpassword')
        
class TaskTests(BaseAPITestCase):
    
    
    @staticmethod
    def data(title, status='to-do', description='Test Description', priority=1, due_date='2030-07-22', category='Technical Task', assigned_to=None, subtasks=None):
        # if assigned_to is None:
        #     assigned_to = []
        # if subtasks is None:
        #     subtasks = []
        return {
            'status': status,
            'title': title,
            'description': description,
            'priority': priority,
            'due_date': due_date,
            'category': category,
            # 'assigned_to': assigned_to,
            # 'subtasks': subtasks
        }
        
        
    def assertTaskDataEqual(self, response_data, expected_data):
        resp_data_without_id = response_data.copy()
        if 'id' in resp_data_without_id:
            del resp_data_without_id['id']
        self.assertEqual(resp_data_without_id, expected_data)
    
    
    def test_create_task(self):
        """
        Ensure we can create a new task object.
        """
        # authorized attempt
        self.authenticate()
        url = reverse('task-list')
        data = self.data('Test Create') 
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Create')
        self.assertTaskDataEqual(response.data, data)
        
        # unauthorized attempt
        self.client.logout()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
       
        
    def test_get_tasks(self):
        """
        Ensure we receive all task objects.
        """
        # authorized attempt
        self.authenticate()
        data = self.data('Test Get All')
        Task.objects.create(**data)
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Get All')
        
        # unauthorized attempt
        self.client.logout()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
       
        
    def test_get_task_detail(self):
        """
        Ensure we can retrieve a task by id.
        """
        # authorized attempt
        self.authenticate()
        data = self.data('Test Get Detail')
        task = Task.objects.create(**data)
        url = reverse('task-detail', args=[task.id])
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTaskDataEqual(response.data, data)
        
        # unauthorized attempt
        self.client.logout()
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_update_task(self):
        """
        Ensure we can update a task.
        """
        # authorized attempt
        self.authenticate()  
        data = self.data('Test Update')
        task = Task.objects.create(**data)
        url = reverse('task-detail', args=[task.id])
        updated_data = self.data(title='Title Updated', status='done', description='Description Updated', priority=2, due_date='2099-09-01', category='User Story')
        response = self.client.put(url, updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTaskDataEqual(response.data, updated_data)
        
        # unauthorized attempt
        self.client.logout()
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        
    def test_partial_update_task(self):
        """
        Ensure we can partially update a task.
        """
        # authorized attempt
        self.authenticate()
        data = self.data('Test Update')
        task = Task.objects.create(**data)
        url = reverse('task-detail', args=[task.id])
        partial_updated_data = {
            'status' : 'done',
            'title' : 'Title Updated',
        }
        response = self.client.patch(url, partial_updated_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'done') # updated
        self.assertEqual(response.data['title'], 'Title Updated') # updated
        self.assertEqual(response.data['description'], data['description']) # not updated
        self.assertEqual(response.data['priority'], data['priority']) # not updated
        self.assertEqual(response.data['due_date'], data['due_date']) # not updated
        self.assertEqual(response.data['category'], data['category']) # not updated
        self.assertEqual(response.data['assigned_to'], data['assigned_to']) # not updated
        self.assertEqual(response.data['subtasks'], data['subtasks']) # not updated
        
        # unauthorized attempt
        self.client.logout()
        response = self.client.patch(url, partial_updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        

    def test_delete_task(self):
        """
        Ensure we can delete a task.
        """
        # authorized attempt
        self.authenticate()
        data = self.data('Task Delete')
        task = Task.objects.create(**data)
        url = reverse('task-detail', args=[task.id])
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
        
        # unauthorized attempt
        self.client.logout()
        task = Task.objects.create(**data)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        