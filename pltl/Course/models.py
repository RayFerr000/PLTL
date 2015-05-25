'''This is the Course models'''
from django.db import models

# Create your models here.
'''making our own Course class'''
class Course(models.Model):
	course_id = models.CharField(max_length=20, default = 'DEFAULT VALUE', db_index=True, unique=True, blank=False)
	course_name = models.CharField(max_length=200, blank=False)
	
	def __unicode__(self):
		return self.course_id
def allCourses():
	course_info = Course.objects.all()
	return course_info
