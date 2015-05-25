'''This is the Homework test'''
from django.test import TestCase
from Class.models import Class
from User.models import User
from Course.models import Course
from Enrolled_Class.models import Enrolled_Class
from Assignment.models import Assignment
from Homework.models import Homework
from django.core.exceptions import ValidationError
from datetime import timedelta, date
from django.conf import settings
from django.utils.importlib import import_module
from django.http import HttpRequest
from Homework.views import homework_submission
from django.core.files import File
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

'''making our own Test class for model Homework'''
class Test_Class(TestCase):

    def test_model_assignment_id_foreign_key_relation(self):
        Assignment.objects.create(assignment_name="ass1", class_id=Class.objects.create(class_id="CS601FALL201501", course_id=Course.objects.create(course_id="CS601", course_name="Operating System"), semester="FALL", year="2015"), pub_date=date.today(), due_date=date.today()+timedelta(days=8), total_grade=70)
        assignment = Assignment.objects.get(assignment_name="ass1")
        homework = Homework.objects.create(assignment_id=assignment,homework_soln='solution',submitted_by=User.objects.create(email="xyz@gmail.com", fname="XYZ", lname="ABC", password="123xyz"),submitted_timestamp=date.today())
        self.assertEqual(Homework.objects.filter(assignment_id__assignment_id=assignment.assignment_id).count(), 1)

    def test_model_email_foreign_key_relation(self):
    	User.objects.create(email="xyz@gmail.com", fname="XYZ", lname="ABC", password="123xyz")
        email = User.objects.get(email="xyz@gmail.com")
        Assignment.objects.create(assignment_name="ass1", class_id=Class.objects.create(class_id="CS601FALL201501", course_id=Course.objects.create(course_id="CS601", course_name="Operating System"), semester="FALL", year="2015"), pub_date=date.today(), due_date=date.today()+timedelta(days=8), total_grade=70)
        assignment = Assignment.objects.get(assignment_name="ass1")
        homework = Homework.objects.create(assignment_id=assignment,homework_soln='solution',submitted_by=email,submitted_timestamp=date.today())
        self.assertEqual(email.email, homework.submitted_by.email)

    def test_valid_homework_upload(self):
        User.objects.create(email="xyz@gmail.com", fname="XYZ", lname="ABC", password="123xyz")
        email = User.objects.get(email="xyz@gmail.com")
        Course.objects.create(course_id='CS601', course_name='OS')
        course = Course.objects.get(course_id='CS601')
        Class.objects.create(class_id='CS601FALL201501', course_id=course, semester='Fall', year='2015')
        classs = Class.objects.get(class_id='CS601FALL201501')
        Enrolled_Class.objects.create(email=email,class_id=classs,role='Student',status='Enrolled')
        Assignment.objects.create(assignment_name='ass1', assignmentfile='some', class_id=classs, pub_date=date.today(), due_date=date.today()+timedelta(days=8), total_grade=70)
        assignment = Assignment.objects.get(assignment_name="ass1")
        number_of_homeworks = Homework.objects.count()
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        request.method = 'POST'
        request.session['_auth_user_id'] = 'xyz@gmail.com'
        file_object = open("test-data/hw1.pdf", 'r')
        request.FILES['homework_soln'] = File(file_object)
        request.POST['submitted_timestamp'] = date.today()
        response = homework_submission(request,assignment.assignment_id)
        file_object.close()
        self.assertEqual(number_of_homeworks+1, Homework.objects.count())
