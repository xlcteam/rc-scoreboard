"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from models import LoginForm
from django.test.client import Client


#class SimpleTest(TestCase):
#    def test_basic_addition(self):
#        """
#        Tests that 1 + 1 always equals 2.
#        """
#        self.assertEqual(1 + 1, 2)

class LoginTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_basic_login_page(self):
        response = self.client.get('/login/')
        
        # check if page is OK
        self.assertEqual(response.status_code, 200)
        
        # check if we have a form
        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], LoginForm))

        # check if we get to index (/) after logging in
        self.assertTrue('next' in response.context)
        self.assertEqual(response.context['next'], '/')

    def test_login_page_with_forward(self):
        response = self.client.get('/login/?next=/soccer/events')

        # check if page is OK
        self.assertEqual(response.status_code, 200)

        # check if we have a form
        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], LoginForm))

        # check if we get to events (/events) after logging in
        self.assertTrue('next' in response.context)
        self.assertEqual(response.context['next'], '/soccer/events')

    def test_login_page_forwarding(self):
        response = self.client.post('/login/', {'username':
            'admin', 'password': 'admin', 'next': '/soccer/events'})

        # check if page is OK
        #self.assertEqual(response.status_code, 302)

class LogoutTest(TestCase):
    def setUp(self):
        self.client = Client()


    def test_logout_forward(self):
        response = self.client.get('/logout/')
        
        # check if page is OK
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'http://testserver/')
 


