'''This is the Enrolled_Class test'''
from django.test import TestCase
from Class.models import Class
from User.models import User
from Course.models import Course
from Enrolled_Class.models import Enrolled_Class
from django.core.exceptions import ValidationError

'''making our own Test class for model Enrolled_Class'''
class Test_Class(TestCase):

    def test_model_class_id_foreign_key_relation(self):
        enrolled1 = Enrolled_Class.objects.create(email=User.objects.create(email="xyz@gmail.com", fname="XYZ", lname="ABC", password="123xyz"),class_id=Class.objects.create(class_id="CS601FALL201501", course_id=Course.objects.create(course_id="CS601", course_name="Operating System"), semester="FALL", year="2015"),role="STUDENT",status="ENROLLED")
        u = User.objects.create_user(fname='Ray', lname='Ferr', email='ray@email.com', password='goat')
        enrolled1.peer_leader = u
        enrolled1.full_clean()
        enrolled1.save()
        self.assertEqual(Enrolled_Class.objects.filter(class_id__class_id="CS601FALL201501").count(), 1)

    def test_model_email_foreign_key_relation(self):
    	enrolled1 = Enrolled_Class.objects.create(email=User.objects.create(email="xyz@gmail.com", fname="XYZ", lname="ABC", password="123xyz"),class_id=Class.objects.create(class_id="CS601FALL201501", course_id=Course.objects.create(course_id="CS601", course_name="Operating System"), semester="FALL", year="2015"),role="STUDENT",status="ENROLLED")
        u = User.objects.create_user(fname='Sam', lname='Tarin', email='tar@email.com', password='goat')
        enrolled1.peer_leader = u
        enrolled1.full_clean()
        enrolled1.save()
        self.assertEqual(Enrolled_Class.objects.filter(email__email="xyz@gmail.com").count(), 1)
