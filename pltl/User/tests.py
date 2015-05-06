from django.test import TestCase, RequestFactory, Client
from django.conf import settings
from django.utils.importlib import import_module
from django.http import HttpRequest
from User.models import User
from User.views import user_signup_save, login
from User.admin import make_staff

class UserTests(TestCase):
    def test_valid_user_saves(self):
        number_of_users = User.objects.count()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['fname'] = 'john'
        request.POST['lname'] = 'doe'
        request.POST['email'] = 'jdoe@gmail.com'
        request.POST['password'] = 'michelle'
        response = user_signup_save(request)
        self.assertEqual(number_of_users +1, User.objects.count())

    def test_invalid_users_dont_save(self):
        number_of_users = User.objects.count()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['fname'] = ''
        request.POST['lname'] = ''
        request.POST['email'] = ''
        request.POST['password'] = ''
        response = user_signup_save(request)
        self.assertEqual(number_of_users, User.objects.count())

    def test_password_is_hashed(self):
        user = User.objects.create_user(fname='john', lname='doe', email='jdoe@gmail.com', password='michelle')
        self.assertNotEqual('michelle', User.objects.first().password)
        self.assertTrue(User.objects.first().check_password('michelle'))

    def test_registered_user_can_login(self):
        user = User.objects.create_user(fname='john', lname='doe', email='jdoe@gmail.com', password='michelle')
        request = HttpRequest()
        #Need to add session to this mock request
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        request.method = 'POST'
        request.POST['email'] = 'jdoe@gmail.com'
        request.POST['password'] = 'michelle'
        response = login(request)
        self.assertIn(user.email, request.session['_auth_user_id'])

    def test_unregistered_user_cant_login(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        request.method = 'POST'
        request.POST['email'] = 'jdoe@gmail.com'
        request.POST['password'] = 'michelle'
        response = login(request)

        #Test to make sure session is empty
        self.assertEqual(0, len(request.session.keys()))

    def test_admin_has_permissions(self):
        admin = User.objects.create_superuser(fname='Jhon', lname='Doe', email='jdoe@gmail.com', password='michelle')
        self.assertNotEqual(len(admin.get_all_permissions()), 0)

    def test_admin_can_designate_staff(self):
        admin = User.objects.create_superuser(fname='Jhon', lname='Doe', email='jdoe@gmail.com', password='michelle')
        user = User.objects.create_user(fname='ray', lname='ferranti', email='rferr@gmail.com', password='michelle')
        #Make sure that is_staff is initally False
        self.assertEqual(user.is_staff, False)
        queryset = User.objects.filter(email='rferr@gmail.com')
        request = HttpRequest()
        make_staff(admin, request, queryset)
        #Make sure is_staff has been changed
        self.assertEqual(User.objects.get(email='rferr@gmail.com').is_staff, True)
