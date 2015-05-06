from django.forms import ModelForm
from django.forms import ModelChoiceField
from Homework.models import Homework
from Assignment.models import Assignment
from User.models import User
from django import forms


class HomeworkForm(ModelForm):
    class Meta:
        model = Homework
        fields = ['homework_soln']
