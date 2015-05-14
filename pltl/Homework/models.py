from django.db import models
from Assignment.models import Assignment
from User.models import User
from datetime import datetime
from time import time

def get_upload_file_name(instance, filename):
	return "homework/%s_%s" % (str(time()).replace('.','_'), filename)

class Homework(models.Model):
	homework_id = models.AutoField(primary_key=True)
	assignment_id = models.ForeignKey(Assignment, to_field = 'assignment_id')
	homework_soln = models.FileField(upload_to=get_upload_file_name)
	submitted_by = models.EmailField(max_length=20, blank = False)
	submitted_timestamp = models.DateTimeField(auto_now_add=True, blank=True)
	grade = models.CharField(max_length = 3, blank = True, null=True)
	feedback = models.CharField(max_length = 300, blank = True, null=True)
	graded_by = models.CharField(max_length = 50, blank = True, null=True)
