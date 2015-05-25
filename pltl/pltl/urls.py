from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView
from User.views import user_signup_save, login,logout
from django.conf import settings
from django.conf.urls.static import static
from pltl import views
from django.conf.urls import handler404

admin.autodiscover()


urlpatterns = patterns('',
    
   url(r'^$', TemplateView.as_view(template_name = 'index.html'), name = 'home'),
    url(r'^help/', TemplateView.as_view(template_name = 'help.html'), name = 'help'),
    url(r'^contact/', TemplateView.as_view(template_name = 'contact.html'), name = 'contact'),
    url(r'^Class/Assignment/',include('Homework.urls')),
    
    url(r'^signup/', user_signup_save, name="user_signup_save"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'User/', include('User.urls', namespace="User")),
    #url(r'^login/', login, name = "login"),
    url(r'^logout/', logout, name = "logout"),
    #url(r'^User/search_for_class','Class.views.search_for_class', name = "searchForClass"),
    url(r'^Courses/', 'Course.views.course_list', name = "course"),
    url(r'^Classes/', 'Class.views.class_list', name = "class"),
    url(r'^Homework/(?P<ass_id>\w+)$', 'Homework.views.homework_submission', name = "homework_submission"),
    url(r'^Homework/', 'Homework.views.homework_submission', name = "homework_submission"),
    url(r'^PageNotFound/', TemplateView.as_view(template_name = '404.html'), name = '404'),
    url(r'^class/', TemplateView.as_view(template_name = 'class_homepage.html'), name = "class"),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.error404
