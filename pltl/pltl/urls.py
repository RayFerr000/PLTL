from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from User.views import user_signup_save, login,logout
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', TemplateView.as_view(template_name = 'index.html'), name = 'home'),
    url(r'^Class/Assignments/',include('Homework.urls')),
    
    url(r'^signup/', user_signup_save, name="user_signup_save"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'User/', include('User.urls', namespace="User")),
    #url(r'^login/', login, name = "login"),
    url(r'^logout/', logout, name = "logout"),
    #url(r'^User/search_for_class','Class.views.search_for_class', name = "searchForClass"),
    url(r'^Courses/', 'Course.views.course_list', name = "course"),
    url(r'^Classes/', 'Class.views.class_list', name = "class"),
    url(r'^Homework/', 'Homework.views.home_list', name = "Homework"),    
    url(r'^class/', TemplateView.as_view(template_name = 'class_homepage.html'), name = "class"),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

