from django.shortcuts import render, render_to_response, RequestContext
from django.template import RequestContext
from Class.forms import ClassForm
from django.http import HttpResponseRedirect
from Class.models import Class
from Enrolled_Class.models import Enrolled_Class
from Course.models import Course
from User.models import User
from django.contrib import auth
from Class.models import get_semester

from django.core.urlresolvers import reverse
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import timedelta, datetime, date
from django.utils import timezone
from Assignment.models import Assignment
from Assignment.forms import AssignmentForm
from Assignment.PostSerializer import PostSerializer

def class_list(request):
    class_info = Class.objects.all()
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            new_class = form.save(commit=False)
            new_class = form.save()
            Enrolled = Enrolled_Class(email = User.objects.get(email=request.session['_auth_user_id']),
                                            class_id =Class.objects.get(class_id=request.POST.get('class_id')),
                                            role = 'Instructor')
            Enrolled.full_clean()
            Enrolled.save()
            print Enrolled_Class.objects.all()
    else:
        form = ClassForm()
        form.fields['course_id'].label = "Select Course "
        form.fields['course_id'].queryset = Course.objects.all()

    return render_to_response('classes.html',{'classes': class_info, 'form': form},context_instance=RequestContext(request))

def instructors_current_classes(request):
    
    class_info = Enrolled_Class.objects.filter(role='Instructor',email=request.session['_auth_user_id'], 
                                                   class_id = (Class.objects.filter(semester=get_semester(), year=datetime.now().year).values('class_id'))).values('class_id')    
    return class_info

'''
def user_enroll_in_class(request):
    email=request.session['_auth_user_id'] 
    class_id = request.POST.get('class_id')
    enroll = Enrolled_Class(email = email, class_id = class_id , role = 'Student')
    return pass
'''

'''def instructors_current_classes_course_name(request):
    class_info = Enrolled_Class.objects.filter(role='Instructor',email=request.session['_auth_user_id'], class_id = (Class.objects.filter(semester=get_semester(), year=datetime.now().year).values('class_id'))).values('class_id')
    
    for i in class_info:
        class_id = i['class_id']
        course_name = Course.objects.filter(course_id = (Class.objects.filter(class_id=class_id).values('course_id'))).values('course_name')
        print course_name
    
    course_name = []
    j = 0
    for i in class_info:
        class_id = i['class_id']
        course_name[j] = Course.objects.filter(course_id = (Class.objects.filter(class_id=class_id).values('course_id'))).values('course_name')
        j = j+1

        print course_name

    return course_name'''

def assignment_list(request, class_id):
    # Handle file upload
    if request.method == 'POST':
        
        req_pub_date = request.POST.get('pub_date')
        req_due_date = request.POST.get('due_date')
    
        form = AssignmentForm(request.POST, request.FILES)
        #if request.POST.get('class_id'):
        req_class_id = class_id
        print '-------POST------'+req_class_id
        #else:
        #req_class_id = 'X201'
        if form.is_valid():                  
            newdoc = Assignment(assignment_name=request.POST.get('assignment_name'), class_id=Class.objects.get(class_id=req_class_id), pub_date=req_pub_date, due_date=req_due_date, total_grade=request.POST.get('total_grade'), assignmentfile=request.FILES['assignmentfile'])
            newdoc.save()
        print form.full_clean()

            # Redirect to the document list after POST
        return HttpResponseRedirect(reverse('User:Class:assignment',kwargs={'class_id': req_class_id}))
    else:
        req_class_id = class_id
        print '-------GET------'+req_class_id
        form = AssignmentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Assignment.objects.all().filter(class_id=req_class_id)


    # Render list page with the documents and the form
    return render_to_response(
        'list.html',
        {'documents': documents, 'form': form, 'class_id':req_class_id},context_instance=RequestContext(request))


@api_view(['GET'])
def getAssignmentList(request, class_id):
 print "++++++++++++++++++api call here"
 if request.method == 'GET':
  
  documents = Assignment.objects.all().filter(class_id=class_id)

  serializer = PostSerializer(documents, many=True)
  return Response(serializer.data)
