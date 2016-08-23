from django.contrib import messages
from django.test import TestCase
from .models import Contact
from .views import NAME_ERROR, EMAIL_ERROR, CONTACT_SUCCESS, NAME_TAG, EMAIL_TAG

class HomePageTest(TestCase):

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    
class NewContactTest(TestCase):

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

    def test_new_contact_POST_saves_new_contact(self):
        reponse = self.client.post('/new_contact', data=self.new_contact_data)

        self.assertEqual(Contact.objects.count(), 1)
        new_contact = Contact.objects.first()
        self.assertEqual(new_contact.name, self.test_name)
        self.assertEqual(new_contact.email, self.test_email)
        self.assertEqual(new_contact.phone, self.test_phone)
        self.assertEqual(new_contact.comments, self.test_comments)
        self.assertEqual(new_contact.waiting_list, True)

    def test_new_contact_POST_redirects_to_home_page(self):
        response = self.client.post('/new_contact', data=self.new_contact_data)
        self.assertRedirects(response, '/#contact')


    def test_new_contact_POST_no_name_doesnt_create_contact(self):
        data = self.new_contact_data.copy()
        data['name'] = ''

        reponse = self.client.post('/new_contact', data=data)

        self.assertEqual(Contact.objects.count(), 0)

    def test_new_contact_POST_no_email_doesnt_create_contact(self):
        data = self.new_contact_data.copy()
        data['email'] = ''

        reponse = self.client.post('/new_contact', data=data)

        self.assertEqual(Contact.objects.count(), 0)

    def test_new_contact_POST_passes_errors_to_home_page(self):
        data = self.new_contact_data.copy()
        data['name'] = ''
        data['email'] = ''
        errors = [NAME_ERROR, EMAIL_ERROR]

        response = self.client.post('/new_contact', data=data, follow=True)
        msgs = list(response.context['messages'])
        self.assertEqual(msgs[0].message, NAME_ERROR)
        self.assertEqual(msgs[0].level, messages.ERROR)
        self.assertIn(NAME_TAG, msgs[0].tags)
        self.assertEqual(msgs[1].message, EMAIL_ERROR)
        self.assertEqual(msgs[1].level, messages.ERROR)
        self.assertIn(EMAIL_TAG, msgs[1].tags)

    def test_new_contact_POST_passes_success_to_home_page(self):
        response = self.client.post('/new_contact', data=self.new_contact_data, follow=True)
        msgs = list(response.context['messages'])
        self.assertEqual(msgs[0].message, CONTACT_SUCCESS)
        self.assertEqual(msgs[0].level, messages.SUCCESS)

