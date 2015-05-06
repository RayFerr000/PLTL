from django.shortcuts import render, render_to_response, RequestContext
from django.template import RequestContext
from Homework.forms import HomeworkForm
from django.http import HttpResponseRedirect,HttpResponse
from Homework.models import Homework
from Assignment.models import Assignment
from User.models import User
from django.contrib import auth
from datetime import datetime
import json

def home_list(request):
    ass_id = 2
    email = "ankan@email.com" #request.session['_auth_user_id']
    assignment_id = Assignment.objects.get(assignment_id = ass_id)
    ass_info = Assignment.objects.filter(assignment_id = ass_id)
    user_email = User.objects.get(email = email)

    if request.method == 'POST':
        form = HomeworkForm(request.POST, request.FILES)
        if form.is_valid():
            new_home = form.save(commit=False)
            new_home.assignment_id = assignment_id
            new_home.submitted_by = user_email 
            new_home.save()
    else:
        form = HomeworkForm()
        form.fields['homework_soln'].label = "Select homework to Upload "

    homework_info = Homework.objects.filter(assignment_id = assignment_id, submitted_by = user_email)

    return render_to_response('homework.html',{'ass_info': ass_info,'form': form , 'homework_info' : homework_info},context_instance=RequestContext(request))


def homework_submissions_for_particular_assignment(request):
    request.session['assignment_id'] = 1
    
    submittedHomeworks = Homework.objects.filter(assignment_id = request.session['assignment_id'])
    students = {}
    for submission in submittedHomeworks:
        
        students[submission.submitted_by] = {}
        students[submission.submitted_by]['email'] = submission.submitted_by
        students[submission.submitted_by]['name']  = User.objects.get(email = submission.submitted_by).get_full_name()
        students[submission.submitted_by]['grade'] = submission.grade
        students[submission.submitted_by]['feedback'] = submission.feedback
    
    if request.POST:
        return submit_grade(request,students)
    
    return render(request,'gradeAssignment.html', {'students' : students })

def submit_grade(request, students):
    request.session['assignment_id'] = 1
    
    email = request.POST.get('email')
    grade = request.POST.get('Grade')
    feedback = request.POST.get('Feedback')
    
    homework = Homework.objects.get(assignment_id = request.session['assignment_id'] , submitted_by = email)
    homework.grade = grade
    homework.feedback = feedback 
    homework.save()
    
    
    #Since grades and feedback have already been retrieved, update to reflect the changes.
    students[email]['grade'] = grade
    students[email]['feedback'] = feedback
    
    return HttpResponse(json.dumps(students),content_type = 'application/json')
