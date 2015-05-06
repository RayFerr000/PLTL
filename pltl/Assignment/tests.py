""" tests for assignment app"""
from django.utils import unittest
from django.http import HttpRequest
from django.core.files import File
from datetime import timedelta, date
from Course.models import Course
from Class.models import Class
from Assignment.models import Assignment
from Assignment.views import assignment_list
# Create your tests here.

class AssignmentTestCase(unittest.TestCase):
    def test_assignment_created_in_specified_course(self):
        Course.objects.create(course_id='csc001', course_name='data structure')
        course = Course.objects.get(course_id='csc001')
        Class.objects.create(class_id='CS101', course_id=course, semester='Fall', year='2015')
        myclass = Class.objects.get(class_id='CS101', course_id='csc001', semester='Fall', year='2015')
        Assignment.objects.create(assignment_name="ass1", class_id=myclass, pub_date=date.today(), due_date=date.today()+timedelta(days=8), total_grade=70)
        assignment = Assignment.objects.get(assignment_name="ass1")
        self.assertEqual(myclass.class_id, assignment.class_id.class_id)
    
    def test_valid_assignment_save(self):
        Course.objects.create(course_id='csc002', course_name='data structure')
        course1 = Course.objects.get(course_id='csc002')
        Class.objects.create(class_id='CS102', course_id=course1, semester='Fall', year='2015')
        myclass = Class.objects.get(class_id='CS102', course_id='csc002', semester='Fall', year='2015')
        number_of_assignments = Assignment.objects.count()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['assignment_name'] = "ass1"
        #request.POST['class_id'] = myclass.class_id 
        request.POST['pub_date'] = date.today()
        request.POST['due_date'] = date.today()+timedelta(days=8)
        request.POST['total_grade'] = 50
        file_object = open("test-data/hw1.pdf", 'r')
        request.FILES['assignmentfile'] = File(file_object)
        response = assignment_list(request, myclass.class_id)
        file_object.close()
        self.assertEqual(number_of_assignments+1, Assignment.objects.count())
   
    def test_invalid_assignment_save(self):
        Course.objects.create(course_id='csc003',course_name='data structure')
        course1 = Course.objects.get(course_id='csc003')
        Class.objects.create(class_id='CS103', course_id=course1, semester='Fall', year='2015')
        myclass = Class.objects.get(class_id='CS103', course_id='csc003', semester='Fall', year='2015')        
        number_of_assignments1 = Assignment.objects.count()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['assignment_name'] = ''
        request.POST['class_id'] = ''
        request.POST['pub_date'] = ''
        request.POST['due_date'] = ''
        request.POST['total_grade'] = ''        
        request.FILES['assignmentfile'] = ''
        response = assignment_list(request, myclass.class_id)     
        number_of_assignments2 = Assignment.objects.count()       
        self.assertEqual(number_of_assignments1, number_of_assignments2)
