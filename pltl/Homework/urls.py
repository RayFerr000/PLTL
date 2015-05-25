from django.conf.urls import patterns, include, url
from Homework.views import homework_submissions_for_particular_assignment

urlpatterns = patterns('', url(r'^(?P<assignment_id>\w+)/Grade',homework_submissions_for_particular_assignment,name = 'homeworkList')
    )
