from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import CustomUser
from rest_framework.authtoken.models import Token

# Create your tests here.
class UserModelTest(TestCase):
    def test_user_model_exists(self):
        users = CustomUser.objects.count()
        self.assertEqual(users, 0)
        

class CustomUserViewSetTests(APITestCase): 
    
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', password='password1', email='user1@example.com')
        self.user2 = CustomUser.objects.create_user(username='user2', password='password2', email='user2@example.com')
        self.client.login(email='user1@example.com', password='password1')
    
    def test_cant_create_user(self):
        """
        Ensure we can not create a user via this view.
        """
        url = reverse('user-list')
        data = {
            'username' : 'testuser',
            'password' : 'testpassword',
            'email' : 'testuser@mail.de'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        
    def test_get_users(self):
        """
        Ensure we receive all users as a user.
        """
        url = reverse('user-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['username'], 'user1')
        self.assertEqual(response.data[1]['username'], 'user2')
        
    
    def test_get_user_detail(self):
        """
        Ensure we can retrieve a user by id.
        """
        url = reverse('user-detail', kwargs={'pk': self.user2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'user2')
        
        
    def test_user_can_update_own_profile(self):
        """
        Ensure logged in user can update their own profile.
        """
        url = reverse('user-detail', kwargs={'pk' : self.user1.pk})
        data = {
            'username' : 'testuser',
            'password' : 'testpassword',
            'email' : 'testuser@mail.de'
        }
        response = self.client.put(url, data, fromat='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, 'testuser')
        self.assertTrue(self.user1.check_password('testpassword'))
        self.assertEqual(self.user1.email, 'testuser@mail.de')
     
        
    def test_user_can_partial_update_own_profile(self):
        """
        Ensure logged in user can partial update their own profile.
        """
        url = reverse('user-detail', kwargs={'pk' : self.user1.pk})
        data = {
            'password' : 'testpassword',
        }
        response = self.client.patch(url, data, fromat='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user1.refresh_from_db()
        self.assertTrue(self.user1.check_password('testpassword'))
        
    
    def test_user_cant_update_other_profiles(self):
        """
        Ensure logged in user can't update other user profiles.
        """
        url = reverse('user-detail', kwargs={'pk' : self.user2.pk})
        data = {
            'username' : 'testuser',
            'password' : 'testpassword',
            'email' : 'testuser@mail.de'
        }
        response = self.client.put(url, data, fromat='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.user1.refresh_from_db()
        self.assertEqual(self.user2.username, 'user2')
        self.assertTrue(self.user2.check_password('password2'))
        self.assertEqual(self.user2.email, 'user2@example.com')

 
    def test_user_cant_partial_update_other_profiles(self):
        """
        Ensure logged in user can't partial update other user profiles.
        """
        url = reverse('user-detail', kwargs={'pk' : self.user2.pk})
        data = {
            'password' : 'testpassword',
        }
        response = self.client.patch(url, data, fromat='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.user1.refresh_from_db()
        self.assertTrue(self.user2.check_password('password2'))
        
    
    def test_user_can_delete_own_profile(self):
        """
        Ensure logged in user can delete their own profile.
        """
        url = reverse('user-detail', kwargs={'pk' : self.user1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), 1)
        # self.assertEqual(CustomUser.objects.filter(id=self.user1.pk).first(), None)
        
        
    def test_user_cant_delete_other_profiles(self):
        """
        Ensure logged in user can't delete other profiles.
        """
        url = reverse('user-detail', kwargs={'pk' : self.user2.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(id=2), self.user2)
        
        
class LoginViewTests(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', email='test@mail.de', password='testpassword')
    
    def test_login_success(self):
        url = reverse('login')
        data = {
            'email':'test@mail.de', 'password':'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['email'], self.user.email)
        
        
    def test_cant_login_with_username_password(self):
        url = reverse('login')
        data = {
            'username':'testuser', 'password':'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)    
        
        
    def test_login_failure(self):
        url = reverse('login')
        data = {
            'email':'test@mail.de', 'password':'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)
        
        
    def test_token_creation(self):    
        self.assertEqual(Token.objects.count(), 0)
        url = reverse('login')
        data = {
            'email':'test@mail.de', 'password':'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.count(), 1)
        
        
    def test_existing_token(self):  
        token = Token.objects.create(user=self.user)  
        url = reverse('login')
        data = {
            'email':'test@mail.de', 'password':'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], token.key)
        self.assertEqual(Token.objects.count(), 1)
        

class RegisterViewTests(APITestCase):
    pass
    # create a user
    def test_register_new_user(self):
        url = reverse('register')
        data = {
            'email': 'user1@mail.de',
            'password' : 'password1',
            'username' : 'user1'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = CustomUser.objects.filter(email=data['email']).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, data['username'])
        self.assertTrue(user.check_password(data['password']))
        
    # cant create a user with the same email
    def test_register_no_double_emails(self):
        
        user1 = CustomUser.objects.create_user(username='user1', password='password1', email='user1@mail.de')
        
        url = reverse('register')
        data = {
            'email': 'user1@mail.de',
            'password' : 'password2',
            'username' : 'user2'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    