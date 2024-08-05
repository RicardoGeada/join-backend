from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Task

class TaskModelTest(TestCase):
    
    def test_task_model_exists(self):
        tasks = Task.objects.count()
        self.assertEqual(tasks, 0)
        
        
class TaskTests(APITestCase):
    
    @staticmethod
    def data(title):
        data = {
            'status' : 'to-do',
            'title' : title,
            'description' : 'Test Description',
            'priority': 1,
            'due_date': '2030-07-22',
            'category': 'Technical Task',
            'assigned_to': [],
            'subtasks': []
        } 
        return data
    
    
    def test_create_task(self):
        """
        Ensure we can create a new task object.
        """
        url = reverse('task-list')
        data = self.data('Test Create') 
        response = self.client.post(url, data, format='json')
    
        resp_data_without_id = response.data
        del resp_data_without_id['id']
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, 'Test Create')
        self.assertEqual(resp_data_without_id, data)
       
        
    def test_get_tasks(self):
        """
        Ensure we receive all task objects.
        """
        data = self.data('Test Get All')
        Task.objects.create(**data)
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Test Get All')
       
        
    def test_get_task_detail(self):
        """
        Ensure we can retrieve a task by id.
        """
        data = self.data('Test Get Detail')
        task = Task.objects.create(**data)
        url = reverse('task-detail', args=[task.id])
        response = self.client.get(url, format='json')
        
        resp_data_without_id = response.data
        del resp_data_without_id['id']
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_data_without_id, data)
        
        
    def test_update_task(self):
        """
        Ensure we can update a task.
        """
        data = self.data('Test Update')
        task = Task.objects.create(**data)
        url = reverse('task-detail', args=[task.id])
        updated_data = {
            'status' : 'done',
            'title' : 'Title Updated',
            'description' : 'Description Updated',
            'priority': 2,
            'due_date': '2099-09-01',
            'category': 'User Story',
            'assigned_to': [],
            'subtasks': []
        }
        response = self.client.put(url, updated_data, format='json')
        
        resp_data_without_id = response.data
        del resp_data_without_id['id']
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_data_without_id, updated_data)
        
        
    def test_partial_update_task(self):
        """
        Ensure we can partially update a task.
        """
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
        

    def test_delete_task(self):
        """
        Ensure we can delete a task.
        """
        data = self.data('Task Delete')
        task = Task.objects.create(**data)
        url = reverse('task-detail', args=[task.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)