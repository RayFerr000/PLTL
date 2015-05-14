'''This is the Class models'''
from django.db import models
from Course.models import Course
from djangoyearlessdate.models import YearlessDateField, YearField
from datetime import datetime


'''making our own Class class'''
class Class(models.Model):
	class_id = models.CharField(max_length=20, default='DEFAULT VALUE', db_index=True, unique=True, blank=False)
	course_id = models.ForeignKey(Course, to_field='course_id')
	semester = models.CharField(max_length=20, default='DEFAULT VALUE', blank=False)
	year = YearField(null=False, blank=False)
	class_description = models.CharField(max_length=500, default='Enter 500 characters at max', blank=True)
	
	def __str__(self): 
        	return self.class_id

def get_semester():
    month = datetime.now().month
    if month==1:
        sem = "Winter"
    elif month >=2 and month <= 5:
        sem = "Spring"
    elif month >=6 and month <= 8:
        sem = "Summer"
    elif month >=9 and month <= 12:
        sem = "Fall"
    return  sem
