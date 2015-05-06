'''This is the Class test'''
from django.test import TestCase
from Class.models import Class
from Course.models import Course
from django.http import HttpRequest
from django.core.exceptions import ValidationError
from django.contrib import auth
from User.models import User 
from User.views import create_class, search_classes

'''making our own Test class for model Class'''
class Test_Class(TestCase):

    def test_model_course_id_foreign_key_relation(self):
        course1 = Course.objects.create(course_id="CS501", course_name="Operating System")
        class1 = Class(class_id = "CS601FALL201501",course_id = Course.objects.create(course_id="CS601"),semester="FALL",year="2015")
        class1.full_clean()  # `event` correctly set. This should pass
        class1.save()
        self.assertEqual(Class.objects.filter(course_id__course_id="CS601").count(), 1)
    '''
    def test_valid_class_saved(self):
        number_of_classes = Class.objects.count()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['class_id'] = 'CS123'
        request.POST['course_id'] = Course.objects.get(course_id='4RR')
        request.POST['semester'] = 'Spring'
        request.POST['year'] = '2015'
        response = create_class(request)
        self.assertEqual(number_of_classes +1, User.objects.count())

    def test_valid_search_class(self):
    	request = HttpRequest()
        request.method = 'GET'
        request.GET['class_id'] = 'CS123'
        response = search_classes(request)
        self.assertTrue(Class.objects.get('CS123'))
    '''
