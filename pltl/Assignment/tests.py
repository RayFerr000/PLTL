""" tests for assignment app"""
from django.utils import unittest
from django.http import HttpRequest
from django.core.files import File
from datetime import timedelta, date
from Course.models import Course
from Class.models import Class
from User.models import User
from Enrolled_Class.models import Enrolled_Class
from Assignment.models import Assignment
from Class.views import createAssignment, assignment_list
from django.conf import settings
from django.utils.importlib import import_module
# Create your tests here.

class AssignmentTestCase(unittest.TestCase):
    def test_assignment_created_in_specified_course(self):
        Course.objects.create(course_id='csc001', course_name='data structure')
        course = Course.objects.get(course_id='csc001')
        Class.objects.create(class_id='CS101', course_id=course, semester='Fall', year='2015')
        myclass = Class.objects.get(class_id='CS101', course_id='csc001', semester='Fall', year='2015')
        Assignment.objects.create(assignment_id=01, class_id=myclass, pub_date=date.today(), due_date=date.today()+timedelta(days=8), total_grade=70)
        assignment = Assignment.objects.get(assignment_id=01)
        self.assertEqual(myclass.class_id, assignment.class_id.class_id)
    
#    def test_valid_assignment_save(self):
#        User.objects.create(fname='Micheal', lname='Grossberg', email='mgross@email.com', password='goat')
#        Course.objects.create(course_id='csc004', course_name='data structure')
#        course1 = Course.objects.get(course_id='csc004')
#        Class.objects.create(class_id='CS102', course_id=course1, semester='Fall', year='2015')
#        myclass = Class.objects.get(class_id='CS102', course_id='csc004', semester='Fall', year='2015')
#        Enrolled_Class.objects.create(email=User.objects.get(email='mgross@email.com'), class_id=Class.objects.get(class_id='CS102'), role='Instructor')
#        number_of_assignments = Assignment.objects.count()
#        request = HttpRequest()
#        request.method = 'POST'
#        request.POST['assignment_name'] = 'assignment test'        
#        request.POST['pub_date'] = date.today()
#        request.POST['due_date'] = date.today()+timedelta(days=8)
#        request.POST['total_grade'] = 50
#        file_object = open("test-data/hw1.pdf", 'r')#("pltl/test-data/hw1.pdf", 'r')
#        request.FILES['assignmentfile'] = File(file_object)
#        request = HttpRequest()
#        engine = import_module(settings.SESSION_ENGINE)
#        session_key = None        
#        request.session = engine.SessionStore(session_key)
#        request.method = 'POST'        
#        request.session['_auth_user_id'] = 'mgross@email.com'
#       
#        response = assignment_list(request, myclass.class_id)
#        file_object.close()
#        self.assertEqual(number_of_assignments+1, Assignment.objects.count())
#   
#    def test_invalid_assignment_save(self):
#        User.objects.create(fname='Micheal', lname='Grossberg', email='gross@email.com', password='goat')        
#        Course.objects.create(course_id='csc005', course_name='artificial intelligance')
#        course2 = Course.objects.get(course_id='csc005')
#        Class.objects.create(class_id='CS103', course_id=course2, semester='Fall', year='2015')
#        myclassObject = Class.objects.get(class_id='CS103', course_id='csc005', semester='Fall', year='2015')
#	print User.objects.get(email='gross@email.com')
#        Enrolled_Class.objects.create(email=User.objects.get(email='gross@email.com'), class_id=Class.objects.get(class_id='CS103'), role='Instructor')  
#        number_of_assignments = Assignment.objects.count()
#        request = HttpRequest()  
#        engine = import_module(settings.SESSION_ENGINE)
#        session_key = None
#        request.session = engine.SessionStore(session_key)        
#        request.session['_auth_user_id'] = 'gross@email.com'
#        request.method = 'POST'
#        request.POST['assignment_id'] = ''        
#        request.POST['pub_date'] = ''
#        request.POST['due_date'] = ''
#        request.POST['total_grade'] = ''        
#        request.FILES['assignmentfile'] = ''
#        response = createAssignment(request, myclassObject.class_id)            
#        self.assertEqual(number_of_assignments, Assignment.objects.count())
