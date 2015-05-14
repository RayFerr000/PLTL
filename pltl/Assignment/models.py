""" This is assignment app"""
from django.db import models
from Class.models import Class
from datetime import datetime
from time import time

def get_upload_file_name(instance, filename):
    return "assignment/%s_%s" % (str(time()).replace('.','_'), filename)

class Assignment(models.Model):
    """This module is for maintaining assignments uploaded by instructor for a course"""
    assignment_id = models.AutoField(primary_key=True)
    assignment_name = models.CharField(max_length=50, default='DEFAULT VALUE', blank=False)
    class_id = models.ForeignKey(Class, to_field='class_id')
    pub_date = models.DateField('Date Published')
    due_date = models.DateField('Due Date')
    total_grade = models.IntegerField(default=0)
    assignmentfile = models.FileField(upload_to=get_upload_file_name, null=True, blank=True)

def __unicode__(self):              # __unicode__ on Python 2
    return self.assignment_id
