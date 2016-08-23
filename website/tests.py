from django.contrib import messages
from django.test import TestCase
from .models import Contact
from .views import CONTACT_SUCCESS, NAME_ERROR, EMAIL_ERROR

class HomePageTest(TestCase):

    def setUp(self):
        self.test_name = "Michael"
        self.test_email = "michael@michael.com"
        self.test_phone = "111-1111"
        self.test_comments = "This is a great website."
        self.test_waiting_list = 'Yes'
        self.new_contact_data = {
            'name': self.test_name, 
            'email': self.test_email, 
            'phone': self.test_phone, 
            'comments': self.test_comments,
            'waiting_list': self.test_waiting_list
        }

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_POST_saves_new_contact(self):
        reponse = self.client.post('/', data=self.new_contact_data)

        self.assertEqual(Contact.objects.count(), 1)
        new_contact = Contact.objects.first()
        self.assertEqual(new_contact.name, self.test_name)
        self.assertEqual(new_contact.email, self.test_email)
        self.assertEqual(new_contact.phone, self.test_phone)
        self.assertEqual(new_contact.comments, self.test_comments)
        self.assertEqual(new_contact.waiting_list, True)

    def test_home_page_POST_renders_home_page_with_contact_anchor(self):
        response = self.client.post('/', data=self.new_contact_data)
        self.assertEquals(response.context['anchor'], 'contact')


    def test_home_page_POST_no_name_doesnt_create_contact(self):
        data = self.new_contact_data.copy()
        data['name'] = ''

        reponse = self.client.post('/', data=data)

        self.assertEqual(Contact.objects.count(), 0)

    def test_home_page_POST_no_email_doesnt_create_contact(self):
        data = self.new_contact_data.copy()
        data['email'] = ''

        reponse = self.client.post('/', data=data)

        self.assertEqual(Contact.objects.count(), 0)

    def test_home_page_POST_passes_errors_to_home_page(self):
        data = self.new_contact_data.copy()
        data['name'] = ''
        data['email'] = ''

        response = self.client.post('/', data=data)

        self.assertEqual(response.context['name_error'], NAME_ERROR)
        self.assertEqual(response.context['email_error'], EMAIL_ERROR)
        self.assertNotIn('success', response.context)

    def test_home_page_POST_passes_success_to_home_page(self):
        response = self.client.post('/', data=self.new_contact_data)
        self.assertEquals(response.context['success'], CONTACT_SUCCESS)

    def test_home_page_POST_passes_form_values_to_home_page(self):
        response = self.client.post('/', data=self.new_contact_data)

        self.assertEqual(response.context['name_value'], self.test_name)
        self.assertEqual(response.context['email_value'], self.test_email)
        self.assertEqual(response.context['phone_value'], self.test_phone)
        self.assertEqual(response.context['comments_value'], self.test_comments)
        self.assertEqual(response.context['waiting_list_value'], bool(self.test_waiting_list))
