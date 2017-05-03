# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client, SimpleTestCase
from tasks.models import Task
from django.contrib.auth.models import User

class TaskTestCase(TestCase):
    """
        Unittest for task model
    """
    def setUp(self):
        Task.objects.create(name='To do',
                            description='or.. may be..')
        Task.objects.create(name='Not to do',
                            description='?')

    def test_task_can_be_done(self):
        """
            Sorry, dont know why do we need unittest here. (
        """
        t1 = Task.objects.get(name='To do')
        t2 = Task.objects.get(name='Not to do')
        t1.done = True
        t2.done = True
        t1.save()
        t2.save()
        self.assertTrue(t1.done)
        self.assertTrue(t2.done)


class AuthTestCase(TestCase):
    """
        tests if we can log in to system
    """
    def setUp(self):
        self.client = Client()

    def test_post_to_login_returns_ok(self):
        response = self.client.post('/login/', {'username': 'cust',
                                                'password': 'qwerty'})
        self.assertEqual(response.status_code, 200)

    def test_post_to_login_returns_template_with_errors(self):
        response = self.client.post('/login/', {'username': 'cust',
                                                'password': 'qwerty'})
        self.assertContains(response, 'Incorrect username', status_code=200)
        self.assertTemplateUsed(response, 'login.html')

    def test_register_check_passwords(self):
        """
            If password != pass_again returns template with
            error: Passwords are different
        """
        response = self.client.post('/register/', {'username': 'cust',
                                                   'password': 'qwerty',
                                                   'pass_again': 'not_qwerty',
                                                   'first_name': 'John',
                                                   'last_name': 'Doe'})
        self.assertContains(response, 'Passwords are different')

    def test_can_register(self):
        response = self.client.post('/register/', {'username': 'cust',
                                                   'password': 'qwerty',
                                                   'pass_again': 'qwerty',
                                                   'first_name': 'John',
                                                   'last_name': 'Doe'})
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200)
        self.client.logout()

    def test_user_login(self):
        User.objects.create_user(username='cust', password='qwerty')
        response = self.client.post('/login/', {'username': 'cust',
                                                'password': 'qwerty'})
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200)


class TaskListTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='cust',
                                             password='qwerty')

    def test_redirects_in_not_authorized(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=/', status_code=302,
                             target_status_code=200)


    def test_get_request_returns_HTML(self):
        self.client.login(username='cust', password='qwerty')
        response = self.client.get('/')
        self.assertContains(response, '!DOCTYPE html', status_code=200)
        self.assertTemplateUsed(response, 'task_list.html')

    def test_post_to_mark_task_done(self):
        self.client.login(username='cust', password='qwerty')
        task = Task.objects.create(name='some_name', description='0000')
        self.assertEqual(task.done, False)
        response = self.client.post('/done/', {'task_id': '1'})
        task.refresh_from_db()
        self.assertEqual(task.done, True)
