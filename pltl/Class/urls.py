# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from Class import views

urlpatterns = patterns('',  url(r'^(?P<class_id>\w+)/$', views.assignment_list, name='assignment'),
			   url(r'^$', views.assignment_list, name='assignment'),
                           url(r'^api/getAssignmentList/(?P<class_id>\w+)/$', views.getAssignmentList))
