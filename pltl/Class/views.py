""" class view"""
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, RequestContext
from django.template import RequestContext
from Class.forms import ClassForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from Class.models import Class
from Assignment.models import Assignment
from Enrolled_Class.models import Enrolled_Class
from Course.models import Course
from User.models import User
from django.contrib import auth
from Class.models import get_semester
from Homework.models import Homework
from django.core.urlresolvers import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import timedelta, datetime, date
from django.utils import timezone
from Assignment.forms import AssignmentForm
from Assignment.PostSerializer import PostSerializer
import csv

''' This function will create class using model form '''
def class_list(request):
    class_info = Class.objects.all()
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            new_class = form.save()
            entemp = Enrolled_Class(email=User.objects.get(\
            email=request.session['_auth_user_id']),\
            class_id=Class.objects.get(\
            class_id=request.POST.get('class_id')),\
            role='Instructor')
            entemp.full_clean()
            entemp.save()
    else:
        form = ClassForm()
        form.fields['course_id'].label = "Select Course "
        form.fields['course_id'].queryset = Course.objects.all()
    return render_to_response('classes.html', {'classes':class_info,\
    'form':form}, context_instance=RequestContext(request))

''' This function will show current Classes instructor teaching this semester '''
def instructors_current_classes(request):
    class_info = Enrolled_Class.objects.filter(\
    role='Instructor',\
    email=request.session['_auth_user_id'],\
    class_id=(Class.objects.filter(semester=get_semester(),\
    year=datetime.now().year).values('class_id'))).values('class_id')
    return class_info

''' This function will show registered Class list of student for current semester '''
def student_current_class_status(request):
    student_class_status = Enrolled_Class.objects.filter(
    email=request.session['_auth_user_id']).exclude(
    status='').values('class_id', 'status')
    return student_class_status

def instructors_current_classes_course_name(request):
    classl = Enrolled_Class.objects.filter(role='Instructor',\
    email=request.session['_auth_user_id'],\
    class_id=(Class.objects.filter(\
    semester=get_semester(),\
    year=datetime.now().year).values('class_id'))).values('class_id')
    class_ids = list()
    for i in classl:
        class_ids.append(i['class_id'])
    course_name = list()
    for i in class_ids:
        course = Course.objects.filter(course_id=(Class.objects.filter(\
        class_id=i).values('course_id'))).values('course_name')
        for j in course:
            course_name.append(j['course_name'])
    return course_name

'''This function will zip Instructors current class id and course name '''
def instructors_current_courses_classes(request):
    classl = Enrolled_Class.objects.filter(role='Instructor',\
    email=request.session['_auth_user_id'],\
    class_id=(Class.objects.filter(semester=get_semester(),\
    year=datetime.now().year).values('class_id'))).values('class_id').order_by('-id')
    class_ids = list()
    courselistd = list()
    for i in classl:
        # Each Class ID is appending
        class_ids.append(i['class_id'])
        for i in class_ids:
            # For list of class ID getting Course Name
            course = Course.objects.filter(course_id=(Class.objects.filter(\
            class_id=i).values('course_id'))).values('course_name')
            for j in course:
                # All the course name is appending
                courselistd.append(j['course_name'])
    class_course_list = zip(classl, courselistd)
    return class_course_list

def assignment_list(request, class_id):
    #Determine if the current user is a Peer Leader for this class
    email = request.session['_auth_user_id']
    enrolled_by1 = Enrolled_Class.objects.filter(email = email, class_id = class_id, role = 'Student', status = 'Enrolled').values('email')
    enrolled_by2 = Enrolled_Class.objects.filter(email = email, class_id = class_id, role = 'Instructor').values('email')
    enrolled_by3 = Enrolled_Class.objects.filter(email = email, class_id = class_id, role = 'Peer Leader').values('email')
    if enrolled_by1 or enrolled_by2 or enrolled_by3:
        role = Enrolled_Class.objects.filter(class_id = class_id, email = email).values('role') 
        print role
        if request.method == 'POST':        
            req_pub_date = request.POST.get('pub_date')
            req_due_date = request.POST.get('due_date')    
            form = AssignmentForm(request.POST, request.FILES)        
            req_class_id = class_id        
            if form.is_valid():                  
                newAssignment = Assignment(assignment_name=request.POST.get('assignment_name'),\
                class_id=Class.objects.get(class_id=req_class_id), pub_date=req_pub_date, due_date=req_due_date,\
                total_grade=request.POST.get('total_grade'), assignmentfile=request.FILES['assignmentfile'])
                newAssignment.save()
            print form.full_clean()
            # Redirect to assignments list after POST
            return HttpResponseRedirect(reverse('User:Class:assignments',kwargs={'class_id': req_class_id}))
        else:
            req_class_id = class_id
            print 'assignment_list -------GET------ used'+req_class_id
            form = AssignmentForm() # A empty, unbound form

    # Load documents for the list page
        documents = Assignment.objects.all().filter(class_id=req_class_id)
        user_role = Enrolled_Class.objects.filter(email=request.session['_auth_user_id'], \
        class_id=req_class_id).values('role')[0]['role']
   
    # Render list page with the documents and the form
        return render_to_response(
            'list.html',
            {'documents': documents, 'form': form, 'class_id':req_class_id, 'role':user_role,'Role':role},context_instance=RequestContext(request))
    else:
        return render_to_response('404.html')


def createAssignment(request, classid):
    email = request.session['_auth_user_id']
    enrolled_by1 = Enrolled_Class.objects.filter(email = email, class_id = classid, role = 'Instructor').values('email')
    enrolled_by2 = Enrolled_Class.objects.filter(email = email, class_id = classid, role = 'Peer Leader').values('email')
    if enrolled_by1 or enrolled_by2:
        print "create assignment page " +classid
        if request.method == 'POST':
            req_pub_date = request.POST.get('pub_date')
            req_due_date = request.POST.get('due_date')    
            form = AssignmentForm(request.POST, request.FILES)
            req_class_id = classid
            if form.is_valid():                  
                newAssignment = Assignment(assignment_name=request.POST.get('assignment_name'), \
                class_id=Class.objects.get(class_id=classid), pub_date=req_pub_date, due_date=req_due_date, \
           total_grade=request.POST.get('total_grade'), assignmentfile=request.FILES['assignmentfile'])
                newAssignment.save()
            print form.full_clean()
            documents = Assignment.objects.all().filter(class_id=req_class_id)            
            user_role = Enrolled_Class.objects.filter(email=request.session['_auth_user_id'], class_id=req_class_id).values('role')[0]['role']
            print user_role
            return HttpResponseRedirect(reverse('User:Class:assignments',kwargs={'class_id':req_class_id}))
        else:        
            req_class_id = classid
            print 'create -------GET------ used'+req_class_id
            form = AssignmentForm() # A empty, unbound form

        assignments = Assignment.objects.all().filter(class_id=req_class_id)
        
        user_role = Enrolled_Class.objects.filter(email=request.session['_auth_user_id'], class_id=req_class_id).values('role')[0]['role']
        
        return render_to_response(
            'createAssignment.html',
            {'documents': assignments, 'form': form, 'classid':req_class_id, 'role':user_role},context_instance=RequestContext(request))
    else:
        return render_to_response('404.html')


@api_view(['GET'])
def getAssignmentList(request, class_id): 
 if request.method == 'GET':  
  documents = Assignment.objects.all().filter(class_id=class_id).order_by('-assignment_id')
  serializer = PostSerializer(documents, many=True)
  return Response(serializer.data)
  
def view_all_students_grades_for_all_assignment(request, class_id):
    user = request.session['_auth_user_id']
    taught_by = Enrolled_Class.objects.get(email = user, class_id = class_id)
    if taught_by.role != 'Student':
        assignment_names = []
        assignment_ids = []
        Homeworks = {}
        Assignments = Assignment.objects.all().filter(class_id=class_id).order_by('assignment_id')
        if Assignments:
            for ass in Assignments:
                assignment_names.append(ass.assignment_name)
                assignment_ids.append(ass.assignment_id)
            Students = {}
            if taught_by.role == 'Peer Leader':
                Email = taught_by.students_led.all().order_by('email')
                for email in Email:
                    Students[email.email] = email.get_full_name()
            else:
                Emails = Enrolled_Class.objects.all().filter(class_id = class_id, role = 'Student').order_by('email')
                for emails in Emails:
                    Email = User.objects.all().filter(email = emails.email)
                    for email in Email:
                        Students[email.email] = email.get_full_name()            
            for student in Students:
                Homeworks[student] = list()
                Homeworks[student].append(Students[student])
                for assignment in assignment_ids:        
                    homeworks = Homework.objects.all().filter(submitted_by = student, assignment_id = assignment)
                    grade = '--'
                    if not homeworks:
                        grade = '--'
                    else:
                        for homework in homeworks:
                            grade = homework.grade
                            if not grade:
                                grade = '--'
                    Homeworks[student].append(grade)
        return render_to_response('view_class_grade.html',{'class_id':class_id, 'assignments': assignment_names, 'Homeworks': Homeworks},context_instance=RequestContext(request))
    else:
        return render_to_response('404.html')

def view_all_assignments_grades_for_student(request, class_id):
    user = request.session['_auth_user_id']
    enrolled_by = Enrolled_Class.objects.filter(email = user, class_id = class_id, role = 'Student', status = 'Enrolled').values('email')
    
    if enrolled_by:
        Assignments = Assignment.objects.all().filter(class_id=class_id).order_by('assignment_id')
        assignment_names = []
        assignment_ids = []
        Submitted_Homeworks = {} 
        for ass in Assignments:
            assignment_names.append(ass.assignment_name)
            assignment_ids.append(ass.assignment_id)
            Submitted_Homeworks[ass.assignment_id] = list()
            Submitted_Homeworks[ass.assignment_id].append(ass.assignment_name)
        for assignment in assignment_ids:
            homeworks = Homework.objects.all().filter(submitted_by = user, assignment_id = assignment)
            grade = '--'
            feedback = '--'
            graded_by = '--'
            submitted_on = '--'
            submitted_homework = '--'
            homework_name = '--'
            if not homeworks:
                grade = '--'
                feedback = '--'
                graded_by = '--'
                submitted_on = '--'
                submitted_homework = '--'
                homework_name = '--' 
            else:
                for homework in homeworks:                    
                    submitted_on = homework.submitted_timestamp
                    feedback = homework.feedback
                    graded_by = homework.graded_by
                    grade = homework.grade
                    submitted_homework = homework.homework_soln
                    index = homework.homework_soln.name.rfind('_')
                    homework_name = homework.homework_soln.name[index+1:]
                    if not grade:
                        grade = '--'
                        feedback = '--'
                        graded_by = '--'
            Submitted_Homeworks[assignment].append(submitted_homework)
            Submitted_Homeworks[assignment].append(homework_name)
            Submitted_Homeworks[assignment].append(submitted_on)
            Submitted_Homeworks[assignment].append(grade)
            Submitted_Homeworks[assignment].append(feedback)
            Submitted_Homeworks[assignment].append(graded_by)
        return render_to_response('view_class_grade_forstudent.html',{'class_id':class_id, 'assignments': assignment_names, 'Submitted_Homeworks' : Submitted_Homeworks},context_instance=RequestContext(request))
    else:
        return render_to_response('404.html')

def download_csv(request, class_id):
    Assignments = Assignment.objects.all().filter(class_id=class_id).order_by('assignment_id')
    assignment_names = []
    assignment_ids = [] 
    for ass in Assignments:
        assignment_names.append(ass.assignment_name)
        assignment_ids.append(ass.assignment_id)
    Students = {}
    Emails = Enrolled_Class.objects.all().filter(class_id = class_id, role = 'Student').order_by('email')
    for emails in Emails:
        Email = User.objects.all().filter(email = emails.email)
        for email in Email:
            Students[email.email] = email.get_full_name()
    Homeworks = {}
    for student in Students:
        Homeworks[student] = list()
        Homeworks[student].append(Students[student])
        for assignment in assignment_ids:        
            homeworks = Homework.objects.all().filter(submitted_by = student, assignment_id = assignment)
            grade = '--'
            if not homeworks:
                grade = '--'
            else:
                for homework in homeworks:
                    grade = homework.grade
                    if not grade:
                        grade = '--'
            Homeworks[student].append(grade)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= "%s.csv"' % (class_id + '_all_assignment_grades')
    assignment_names.insert(0,'Students')
    writer = csv.writer(response)
    writer.writerow(assignment_names)
    hk_grades = list()
    if Homeworks:
        for hk_grade in Homeworks:
                hk_grades.append(Homeworks[hk_grade])
    for hk in hk_grades: 
        writer.writerow(hk)
    return response
