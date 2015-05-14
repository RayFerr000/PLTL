""" This form takes input from User for uploading assignment"""
from django import forms
from datetime import date, timedelta

class AssignmentForm(forms.Form):
    """ This form takes input from User for uploading assignment"""
    assignment_name = forms.CharField(widget=forms.TextInput(attrs={'required':'True'}))
    pub_date = forms.DateField(initial=date.today,
               widget=forms.DateInput(format="%Y-%m-%d", attrs={'readonly':'readonly'}))
    due_date = forms.DateField(initial=(date.today() + timedelta(days=8)),
 widget=forms.DateInput(format="%Y-%m-%d"))
    total_grade = forms.IntegerField(widget=forms.TextInput(attrs={'required':'True'}))
    assignmentfile = forms.FileField(
        label='Select a file'
    )
