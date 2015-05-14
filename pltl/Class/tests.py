'''This is the Class test'''
from django.utils import unittest
from django.test import TestCase, RequestFactory, Client
from Class.models import Class, get_semester
from Course.models import Course
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.contrib import auth
from User.models import User
from Enrolled_Class.models import Enrolled_Class 
from User.views import create_class, search_classes
from Class.views import instructors_current_classes
from Class.views import student_current_class_status
from datetime import timedelta, date, datetime
from django.conf import settings
from django.utils.importlib import import_module
from User.admin import make_staff

'''making our own Test class for model Class'''
class Test_Class(TestCase):

    def test_model_course_id_foreign_key_relation(self):
        course1 = Course.objects.create(course_id="CS501", course_name="Operating System")
        class1 = Class(class_id = "CS601FALL201501", course_id = Course.objects.create(course_id="CS601"), semester="FALL", year="2015")
        class1.full_clean()  # `event` correctly set. This should pass
        class1.save()
        self.assertEqual(Class.objects.filter(course_id__course_id="CS601").count(), 1)
    
    def test_class_created_for_specific_course_id(self):
        Course.objects.create(course_id='CSC001', course_name='data structure')
        course = Course.objects.get(course_id='CSC001')
        Class.objects.create(class_id='CS101', course_id=course, semester='Fall', year='2015')
        newClass = Class.objects.get(class_id='CS101', course_id='CSC001', semester='Fall', year='2015')
        self.assertEqual(course.course_id, newClass.course_id_id)

    def test_enrolled_class_created_for_specific_class_id(self):
        Course.objects.create(course_id='CSC001', course_name='data structure')
        Class.objects.create(class_id='CS101', course_id=Course.objects.get(course_id='CSC001'), semester='Fall', year='2015')
        classt = Class.objects.get(class_id='CS101')
        User.objects.create(fname='Micheal', lname='Grossberg', email='mgross@email.com', password='goat')
        Enrolled_Class.objects.create(email=User.objects.get(email='mgross@email.com'), class_id=classt, role='Instructor')
        newEnrolledClass = Enrolled_Class.objects.get(class_id='CS101')
        self.assertEqual(classt.class_id, newEnrolledClass.class_id_id)

    def test_student_register_for_valid_class(self):
        Course.objects.create(course_id='CSC001', course_name='data structure')
        Class.objects.create(class_id='CS101', course_id=Course.objects.get(course_id='CSC001'), semester='Fall', year='2015')
        User.objects.create(fname='djangotest', lname='djangotest', email='djangotest@email.com', password='djangotest')
        User.objects.create(fname='djangotest2', lname='djangotest2', email='djangotest2@email.com', password='djangotest2')
        Enrolled_Class.objects.create(email=User.objects.get(email='djangotest@email.com'), class_id=Class.objects.get(class_id='CS101'), role='Instructor')
        InsEnrolledClass = Enrolled_Class.objects.filter(class_id='CS101', role='Instructor').values('class_id')
        Enrolled_Class.objects.create(email=User.objects.get(email='djangotest2@email.com'), class_id=Class.objects.get(class_id='CS101'), role='Student', status='Registered')
        StuEnrolledClass = Enrolled_Class.objects.filter(class_id='CS101', role='Student').values('class_id')
        self.assertTrue(InsEnrolledClass, StuEnrolledClass)

    def test_student_droped_registered_class(self):
        Course.objects.create(course_id='CSC001', course_name='data structure')
        Class.objects.create(class_id='CS101', course_id=Course.objects.get(course_id='CSC001'), semester='Fall', year='2015')
        User.objects.create(fname='test', lname='test', email='test@email.com', password='test')
        User.objects.create(fname='test2', lname='test2', email='test2@email.com', password='test2')
        Enrolled_Class.objects.create(email=User.objects.get(email='test@email.com'), class_id=Class.objects.get(class_id='CS101'), role='Instructor')
        Enrolled_Class.objects.create(email=User.objects.get(email='test2@email.com'), class_id=Class.objects.get(class_id='CS101'), role='Student', status='Registered')
        StuEnrolledClass = Enrolled_Class.objects.filter(class_id='CS101', role='Student').values('status')
        Enrolled_Class.objects.create(email=User.objects.get(email='test2@email.com'), class_id=Class.objects.get(class_id='CS101'), role='Student', status='')
        StuDropClass = Enrolled_Class.objects.filter(class_id='CS101', role='Student').values('status')
        self.assertTrue(StuDropClass, StuEnrolledClass)

    def test_get_correct_semester_name(self):
        currentrunningsemester = 'Spring'
        response = get_semester()
        self.assertEqual(currentrunningsemester, response)

    def test_instructors_current_classes(self):
        Course.objects.create(course_id='CSC001', course_name='data structure')
        Class.objects.create(class_id='CS101', course_id=Course.objects.get(course_id='CSC001'), semester='Spring', year='2015')
        User.objects.create(fname='Micheal', lname='Grossberg', email='mgross@email.com', password='goat')
        Enrolled_Class.objects.create(email=User.objects.get(email='mgross@email.com'), class_id=Class.objects.get(class_id='CS101'), role='Instructor')
        number_of_current_classes = len(Enrolled_Class.objects.filter(role='Instructor',email=User.objects.get(email='mgross@email.com'), class_id = (Class.objects.filter(semester='Spring', year='2015').values('class_id'))).values('class_id'))
        
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        request.method = 'POST'
        request.session['_auth_user_id'] = 'mgross@email.com'
        response = instructors_current_classes(request)
        self.assertEqual(number_of_current_classes, len(response))

    def test_student_current_class_status(self):
        Course.objects.create(course_id='CSC001', course_name='data structure')
        Class.objects.create(class_id='CS101', course_id=Course.objects.get(course_id='CSC001'), semester='Spring', year='2015')
        User.objects.create(fname='Samsoon', lname='Tarin', email='tar@email.com', password='goat')
        Enrolled_Class.objects.create(email=User.objects.get(email='tar@email.com'), class_id=Class.objects.get(class_id='CS101'), role='Student', status='Registered')
        students_current_class = len(Enrolled_Class.objects.filter(status='Registered', email='tar@email.com', role='Student').values('class_id'))

        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        request.method = 'POST'
        request.session['_auth_user_id'] = 'tar@email.com'
        response = student_current_class_status(request)
        self.assertEqual(students_current_class, len(response))
    
    def test_valid_class_created(self):
        request = HttpRequest()
        Course.objects.create(course_id='CSC001', course_name='data structure')
        Class.objects.create(class_id='CS101', course_id=Course.objects.get(course_id='CSC001'), semester='Spring', year='2015')
        number_of_classes = Class.objects.count()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['class_id'] = 'CS123'
        Course.objects.create(course_id='4RR', course_name='Operating System')
        request.POST['course_id'] = Course.objects.get(course_id='4RR')
        request.POST['semester'] = 'Spring'
        request.POST['year'] = '2015'

        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        request.method = 'POST'
        request.session['_auth_user_id'] = 'tar@email.com'
        response = create_class(request)
        self.assertEqual(number_of_classes, Class.objects.count())

    def test_invalid_class_created(self):
        number_of_classes = Class.objects.count()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['class_id'] = ''
        Course.objects.create(course_id='', course_name='')
        request.POST['course_id'] = Course.objects.get(course_id='')
        request.POST['semester'] = ''
        request.POST['year'] = ''

        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        request.method = 'POST'
        request.session['_auth_user_id'] = ''
        response = create_class(request)
        self.assertEqual(number_of_classes, Class.objects.count())
