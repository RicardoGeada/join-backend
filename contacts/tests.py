from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from .models import Contact

# Create your tests here.
class ContactsAPITests(APITestCase):
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword', email='test@mail.com')
        self.other_user = CustomUser.objects.create_user(username='otheruser', password='otherpassword', email='other@mail.com')
        self.client.login(email='test@mail.com', password='testpassword')
        self.contact_no_user = Contact.objects.create(name='contact_no_user', email='contact_no_user@mail.com', phone=11111111111111, badge_color=1, initials='CN')
        self.contact_user = Contact.objects.create(name='contact_user', email='contact_user@mail.com', phone=22222222222222, badge_color=2, initials='CU', active_user=self.user)
        self.contact_other_user = Contact.objects.create(name='contact_other_user', email='contact_other_user@mail.com', phone=33333333333333, badge_color=3, initials='CO', active_user=self.other_user)
    
    # test_contact_is_created_for_new_user
    
    def test_user_can_create_new_contact(self):
        """
        Ensure user can create a new contact.
        """
        url = reverse('contact-list')
        data = {
            'name' : 'contact',
            'email' : 'contact@mail.de',
            'phone' : 999999999999999,
            'badge_color' : 15,
            'initials' : 'US'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contact = Contact.objects.filter(id=response.data['id']).first()
        self.assertEqual(Contact.objects.count(), 4)
        self.assertEqual(contact.name, 'contact')
    
    
    def test_user_can_edit_contact(self):
        """
        Ensure user can edit contact.
        """
        url = reverse('contact-detail', kwargs={'pk' : self.contact_no_user.pk})
        updated_data = {
            'name'  : 'updated contact1',
            'email' : 'updated.contact1@mail.com',
            'phone' : 123456789,
            'badge_color' : 15,
            'initials' : 'UC',
        }
        response = self.client.put(url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact_no_user.refresh_from_db()
        self.assertEqual(self.contact_no_user.name, updated_data['name'])
        self.assertEqual(self.contact_no_user.email, updated_data['email'])
        self.assertEqual(self.contact_no_user.phone, str(updated_data['phone']))
        self.assertEqual(self.contact_no_user.badge_color, updated_data['badge_color'])
        self.assertEqual(self.contact_no_user.initials, updated_data['initials'])
      
      
    def test_user_cant_edit_other_user_contact(self):
        """
        Ensure user cant edit the contact info of another active user.
        """
        url = reverse('contact-detail', kwargs={'pk' : self.contact_other_user.pk})
        updated_data = {
            'name'  : 'updated contact',
            'email' : 'updated.contact@mail.com',
            'phone' : 123456789,
            'badge_color' : 15,
            'initials' : 'UC',
        }
        response = self.client.put(url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.contact_other_user.name, 'contact_other_user')
        self.assertEqual(self.contact_other_user.email, 'contact_other_user@mail.com')
        self.assertEqual(self.contact_other_user.phone, 33333333333333)
        self.assertEqual(self.contact_other_user.badge_color, 3)
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
            'badge_color' : 15,
            'initials' : 'UC',
        }
        response = self.client.put(url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact_user.refresh_from_db()
        self.assertEqual(self.contact_user.name, updated_data['name'])
        self.assertEqual(self.contact_user.email, updated_data['email'])
        self.assertEqual(self.contact_user.phone, str(updated_data['phone']))
        self.assertEqual(self.contact_user.badge_color, updated_data['badge_color'])
        self.assertEqual(self.contact_user.initials, updated_data['initials'])
    
    # partial update?
    
    def test_user_can_get_contacts(self):
        """
        Ensure user receives all contacts.
        """
        url = reverse('contact-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['name'], 'contact_no_user')
        self.assertEqual(response.data[1]['name'], 'contact_user')
        self.assertEqual(response.data[2]['name'], 'contact_other_user')
    
    
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
        self.assertEqual(Contact.objects.filter(id=1).first(), None)
    
    
    def test_user_cant_delete_contact_from_other_users(self):
        """
        Ensure user can't delete contact from other active_user.
        """
        url = reverse('contact-detail', kwargs={'pk' : self.contact_other_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Contact.objects.count(), 3)
        self.assertEqual(Contact.objects.get(id=3), self.contact_other_user)
        
        
    def test_user_can_delete_own_contact_and_user_account(self):
        """
        Ensure user can delete own contact and user account.
        """
        url = reverse('contact-detail', kwargs={'pk' : self.contact_user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertEqual(Contact.objects.filter(id=self.contact_user.pk).first(), None)
        self.assertEqual(CustomUser.objects.filter(id=self.user.pk).first(), None)
   
    # test_contact_will_be_deleted_from_task