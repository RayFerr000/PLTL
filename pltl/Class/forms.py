from django.forms import ModelForm
from django.forms import ModelChoiceField
from Class.models import Class
from Course.models import Course
from Course.forms import CourseForm
from django import forms


class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = ['class_id', 'course_id', 'semester','year', 'class_description']
