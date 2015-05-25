# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from Class import views

urlpatterns = patterns('',  url(r'^createAssignment/(?P<classid>\w+)$', views.createAssignment, name='classHome'),
                           url(r'^createAssignment/$', views.createAssignment, name='uploadAssignment'),
                           url(r'^view_all_grades/(?P<class_id>\w+)$', views.view_all_assignments_grades_for_student, name = 'view_all_grades_student'),
                           url(r'^view_all_class_grades/(?P<class_id>\w+)$', views.view_all_students_grades_for_all_assignment, name = 'view_all_grades'),
                           url(r'^view_class_grades/$', views.view_all_students_grades_for_all_assignment, name = 'view_all_grades'),
                           url(r'^download_csv/(?P<class_id>\w+)$', views.download_csv, name = 'download_csv'),        
			   			   url(r'^(?P<class_id>\w+)/$', views.assignment_list, name='assignments'),
                           url(r'^manage/(?P<class_id>\w+)/$', 'User.views.class_student_info', name='manage'),
                           url(r'^api/getAssignmentList/(?P<class_id>\w+)/$', views.getAssignmentList))
