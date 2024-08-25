from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from tasks.models import Task
from .models import Contact
from rest_framework.authtoken.models import Token

class ContactsAPITests(APITestCase):
    
    def setUp(self):
        # set up users
        self.user = CustomUser.objects.create_user(username='contact_user', password='testpassword', email='contact_user@mail.com')
        self.other_user = CustomUser.objects.create_user(username='contact_other_user', password='otherpassword', email='contact_other_user@mail.com')
        
        # authorization for user
        self.user_token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        
        # set up contacts
        self.contact_no_user = Contact.objects.create(name='contact_no_user', email='contact_no_user@mail.com', phone=11111111111111, badge_color=1)
        self.contact_user = Contact.objects.get(active_user=self.user)
        self.contact_other_user = Contact.objects.get(active_user=self.other_user)
        
    
    def test_contact_is_created_for_new_user(self):
        """
        Ensure contact is created for new user.
        """
        new_user = CustomUser.objects.create_user(username='newuser', password='newpassword', email='new@mail.com')
        new_contact = Contact.objects.get(active_user=new_user)
        self.assertEqual(new_contact.name,'newuser')
        self.assertEqual(new_contact.email,'new@mail.com')
        self.assertEqual(new_contact.initials, 'NE')
        
    
    def test_user_can_create_new_contact(self):
        """
        Ensure user can create a new contact.
        """
        url = reverse('contact-list')
        data = {
            'name' : 'newcontact',
            'email' : 'newcontact@mail.com',
            'phone' : 999999999999999,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contact = Contact.objects.filter(id=response.data['id']).first()
        self.assertEqual(Contact.objects.count(), 4)
        self.assertEqual(contact.name, 'newcontact')
        self.assertEqual(contact.email, 'newcontact@mail.com')
        self.assertEqual(contact.phone, '999999999999999')
        
    
    def test_user_cant_create_contact_for_other_user(self):
        """
        Ensure user can't create a new contact for other users.
        active_user can't be set
        """
        url = reverse('contact-list')
        data = {
            'name' : 'newcontact',
            'email' : 'newcontact@mail.com',
            'active_user' : self.other_user.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contact = Contact.objects.filter(id=response.data['id']).first()
        self.assertEqual(contact.name, 'newcontact')
        self.assertEqual(contact.email, 'newcontact@mail.com')
        self.assertEqual(contact.active_user, None)
        self.assertEqual(Contact.objects.filter(active_user=self.other_user).count(), 1)
        
    
    def test_user_can_edit_contact(self):
        """
        Ensure user can edit contact without a user.
        """
        url = reverse('contact-detail', kwargs={'pk' : self.contact_no_user.pk})
        updated_data = {
            'name'  : 'updated contact',
            'email' : 'updated.contact@mail.com',
            'phone' : 123456789,
        }
        response = self.client.put(url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact_no_user.refresh_from_db()
        self.assertEqual(self.contact_no_user.name, updated_data['name'])
        self.assertEqual(self.contact_no_user.email, updated_data['email'])
        self.assertEqual(self.contact_no_user.phone, str(updated_data['phone']))
        self.assertEqual(self.contact_no_user.initials, 'UC')
      
      
    def test_user_cant_edit_other_user_contact(self):
        """
        Ensure user cant edit the contact info of another active user.
        """
        url = reverse('contact-detail', kwargs={'pk' : self.contact_other_user.pk})
        updated_data = {
            'name'  : 'updated contact',
            'email' : 'updated.contact@mail.com',
            'phone' : 123456789,
        }
        response = self.client.put(url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.contact_other_user.name, 'contact_other_user')
        self.assertEqual(self.contact_other_user.email, 'contact_other_user@mail.com')
        self.assertEqual(self.contact_other_user.phone, None)
        self.assertEqual(self.contact_other_user.initials, 'CO')
          
    
    def test_user_can_edit_own_contact(self):
        """
        Ensure user can edit own contact.
        """
        url = reverse('contact-detail', kwargs={'pk' : self.contact_user.pk})
        updated_data = {
            'name'  : 'updated contact',
            'email' : 'updated.contact@mail.com',
            'phone' : 123456789,
        }
        response = self.client.put(url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact_user.refresh_from_db()
        self.assertEqual(self.contact_user.name, updated_data['name'])
        self.assertEqual(self.contact_user.email, updated_data['email'])
        self.assertEqual(self.contact_user.phone, str(updated_data['phone']))
        
    
    def test_user_cant_change_active_user_of_own_contact(self):
        """
        Ensure user cant change active_user of own contact.
        """
        url = reverse('contact-detail', kwargs={'pk' : self.contact_user.pk})
        updated_data = {
            'active_user' : self.other_user.pk
        }
        response = self.client.patch(url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact_user.refresh_from_db()
        self.assertEqual(self.contact_user.active_user, self.user)
    
    
    def test_user_can_get_contacts(self):
        """
        Ensure user receives all contacts.
        """
        url = reverse('contact-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], 'contact_user')
        self.assertEqual(response.data[1]['name'], 'contact_other_user')
        self.assertEqual(response.data[2]['name'], 'contact_no_user')
    
    
    def test_user_can_get_contact_detail(self):
        """
        Ensure we can retrieve a contact by id.
        """
        url = reverse('contact-detail', kwargs={'pk': self.contact_other_user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'contact_other_user')
        
        
    def test_user_can_delete_contact(self):
        """
        Ensure user can delete contacts without acitve_user.
        """
        url = reverse('contact-detail', kwargs={'pk' : self.contact_no_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertEqual(Contact.objects.filter(id=self.contact_no_user.pk).first(), None)
    
    
    def test_user_cant_delete_contact_from_other_users(self):
        """
        Ensure user can't delete contact from other active_user.
        """
        url = reverse('contact-detail', kwargs={'pk' : self.contact_other_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Contact.objects.count(), 3)
        self.assertEqual(Contact.objects.get(id=self.contact_other_user.pk), self.contact_other_user)
        
        
    def test_user_can_delete_own_contact_and_user_account(self):
        """
        Ensure user can delete own contact and user account together.
        """
        url = reverse('contact-detail', kwargs={'pk' : self.contact_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertEqual(Contact.objects.filter(id=self.contact_user.pk).first(), None) # no contact
        self.assertEqual(CustomUser.objects.filter(id=self.user.pk).first(), None) # no user
   
    
    def test_contact_gets_deleted_from_tasks(self):
        """
        Ensure the contact gets removed from all assigned tasks when it gets deleted.
        """
        task_with_contact = Task.objects.create(status='to-do', description='Test Description', priority=1, due_date='2030-07-22', category='Technical Task')
        task_with_contact.assigned_to.add(self.contact_user)
        self.assertIn(self.contact_user, task_with_contact.assigned_to.all())
        
        self.contact_user.delete()
        
        task_with_contact.refresh_from_db()
        
        self.assertEqual(Contact.objects.filter(id=self.contact_user.pk).first(), None)
        self.assertNotIn(self.contact_user, task_with_contact.assigned_to.all())