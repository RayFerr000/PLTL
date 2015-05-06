'''This is the Enrolled_Class models'''
from django.db import models
from Class.models import Class
from User.models import User


'''making our own Enrolled_Class class'''
class Enrolled_Class(models.Model):
    email = models.ForeignKey(User, to_field='email')
    class_id = models.ForeignKey(Class, to_field='class_id',)
    role = models.CharField(max_length=20, default='DEFAULT VALUE', blank=False)
    status = models.CharField(max_length=50, default='DEFAULT VALUE', blank=False)
    peer_leader = models.ForeignKey(User, related_name="peer_leader", null=True, blank=True)
    students_led = models.ManyToManyField(User, related_name="students_led", null=True, blank=True)

    def __str__(self): 
        return self.class_id_id
