from django.shortcuts import render, render_to_response, RequestContext
from django.template import RequestContext
from Homework.forms import HomeworkForm
from django.http import HttpResponseRedirect, HttpResponse
from Homework.models import Homework
from Assignment.models import Assignment
from Enrolled_Class.models import Enrolled_Class
from User.models import User
from django.contrib import auth
from datetime import datetime
from django.core.urlresolvers import reverse
import json

def homework_submission(request, ass_id):
    email = request.session['_auth_user_id']
    cl_id = Assignment.objects.filter(assignment_id = ass_id).values('class_id')
    class_id = cl_id[0]['class_id']
    enrolled_by = Enrolled_Class.objects.filter(email = email, class_id = class_id, role = 'Student', status = 'Enrolled').values('email')
    if enrolled_by:
        assignment_id = Assignment.objects.get(assignment_id = ass_id)
        ass_info = Assignment.objects.filter(assignment_id = ass_id)
        user_email = User.objects.get(email = email)
        ass_name = ""
        for ass in ass_info:
            index = ass.assignmentfile.name.rfind('_')
            ass_name = ass.assignmentfile.name[index+1:]

        if request.method == 'POST':
            form = HomeworkForm(request.POST, request.FILES)
            if form.is_valid():
                new_home = form.save(commit=False)
                new_home.assignment_id = assignment_id
                new_home.submitted_by = user_email 
                new_home.save()
            return HttpResponseRedirect(reverse('homework_submission',kwargs={'ass_id': ass_id}))
        else:
            form = HomeworkForm()

        homework_info = Homework.objects.filter(assignment_id = assignment_id, submitted_by = user_email)
        homework_name = ""
        if homework_info:
            for home in homework_info:
                index = home.homework_soln.name.rfind('_')
                homework_name = home.homework_soln.name[index+1:]
        return render_to_response('homework.html',{'ass_info': ass_info, 'ass_name': ass_name, 'form': form , 'homework_info' : homework_info, 'homework_name' : homework_name, 'ass_id': ass_id},context_instance=RequestContext(request))
    else:
        return render_to_response('404.html')

def homework_submissions_for_particular_assignment(request,assignment_id):
    role = instructor_or_leader(request,assignment_id)
    if role == 'Instructor':
        submittedHomeworks = Homework.objects.filter(assignment_id = assignment_id)
    else:
        submittedHomeworks = []
        leaderEnrolledClass= Enrolled_Class.objects.get(class_id = Assignment.objects.get(assignment_id = assignment_id).class_id,
                                                                                          email = request.session['_auth_user_id'] )
        for student in leaderEnrolledClass.students_led.all():
            if Homework.objects.filter(assignment_id = assignment_id, submitted_by = student.email).exists():
            
                submittedHomeworks.append(Homework.objects.get(assignment_id = assignment_id, submitted_by = student.email))
    
    assignment_name = Assignment.objects.get(assignment_id = assignment_id).assignment_name
    students = {}
    for submission in submittedHomeworks:
        
        students[submission.submitted_by] = {}
        students[submission.submitted_by]['email'] = submission.submitted_by
        students[submission.submitted_by]['name']  = User.objects.get(email = submission.submitted_by).get_full_name()
        students[submission.submitted_by]['grade'] = submission.grade
        students[submission.submitted_by]['homework_soln'] = submission.homework_soln.url
        
        students[submission.submitted_by]['feedback'] = submission.feedback
        students[submission.submitted_by]['graded_by'] = submission.graded_by
    
    if request.POST:
        return submit_grade(request,students,assignment_id,role)
    
    return render(request,'gradeAssignment.html', {'students' : students, 'assignment_id' : assignment_id,
                                                   'assignment_name' : assignment_name,'role':role } )

def submit_grade(request, students,assignment_id,role):

    email = request.POST.get('email')
    grade = request.POST.get('Grade')
    feedback = request.POST.get('Feedback')
    
    homework = Homework.objects.get(assignment_id=assignment_id, submitted_by = email)
    homework.grade = grade
    homework.feedback = feedback 
    homework.graded_by = role
    homework.save()
    
    #Since grades and feedback have already been retrieved, update to reflect the changes.
    students[email]['grade'] = grade
    students[email]['feedback'] = feedback


    return HttpResponse(json.dumps(students),content_type = 'application/json')

def instructor_or_leader(request,assignment_id):
    emailOfGrader = request.session['_auth_user_id']
    grader = Enrolled_Class.objects.get(class_id = Assignment.objects.get(assignment_id = assignment_id).class_id , email = emailOfGrader)
    if grader.role == 'Instructor':
        return 'Instructor'
    else:
        return 'Peer Leader'