from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from User import views


urlpatterns = patterns('',
    url(r'^$', views.user_signup_save, name = 'user_signup_save'),
    url(r'^home', views.login, name = 'login'),
    url(r'^home/', views.create_class, name= "test"),
    url(r'^Class/', include('Class.urls', namespace= "Class")),
    url(r'^searchclass/', views.search_classes, name= "searchclass"),
    url(r'^manage/', views.class_student_info, name='class_student_info'),
    )
