from django.shortcuts import render, redirect, render_to_response, RequestContext
from django.template import RequestContext, loader
from User.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from datetime import datetime
from Class.forms import ClassForm
from Course.forms import CourseForm
from Class.models import Class, get_semester
from Class.views import instructors_current_classes
from Course.models import Course, allCourses
from django.core.urlresolvers import reverse
from Enrolled_Class.models import Enrolled_Class

def user_signup_save(request):
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User(fname=fname, lname=lname, email=email, last_login=datetime.now())
    user.set_password(password)
     
    #force_insert=True forces the database to do an insert rather then an update.
    status = user.save(force_insert=True)
    if status == 'success':
        subject = 'Welcome to PLTL'
        with open ("templates/SignUpNotification.txt", "r") as data:
            msgbody = data.read()
        print msgbody
        msg = 'Dear ' + fname +',\n' + msgbody
        from_mail = settings.EMAIL_HOST_USER
        send_mail(subject, msg,from_mail, [email,from_mail], fail_silently=True)
    return redirect('home')


def login(request):
    
    #student_class_status = Enrolled_Class.objects.filter(status='Registered', email = request.session['_auth_user_id']).values('class_id', 'status')
    
    if request.POST.get('class_id'):
        return create_class(request)
    
    if request.POST.get('email'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email = email , password = password)
    
    elif request.session['_auth_user_id']:
        
        return render_to_response('home.html',{'classes': instructors_current_classes(request), 'courses': allCourses()},context_instance=RequestContext(request))
    
    if user is not None:
        auth.login(request, user)

        return render_to_response('home.html',{'classes': instructors_current_classes(request), 'courses': allCourses()},context_instance=RequestContext(request))
    
    else:
        return HttpResponse("invalid, not logged in")

def logout(request):
    auth.logout(request)
    return render(request, 'index.html') 


def create_class(request):
    student_class_status = Enrolled_Class.objects.filter(status='Registered', email = request.session['_auth_user_id']).values('class_id', 'status')
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
    else:
        form = ClassForm()
    return render_to_response('home.html',{'classes': instructors_current_classes(request), 'student_class_status': student_class_status, 'courses': allCourses(),'form': form},context_instance=RequestContext(request))
 

def search_classes(request):
    student_class_status = Enrolled_Class.objects.filter(status='Registered', email = request.session['_auth_user_id']).values('class_id', 'status')
    
    if 'class_id' in request.GET and request.GET['class_id']:
        q = request.GET['class_id']
        classes = Class.objects.filter(class_id=q)
        courseName = Course.objects.filter(course_id = (Class.objects.filter(class_id=q).values('course_id'))).values('course_name')
        class_des = Class.objects.filter(class_id= q).values('class_description', 'class_id')       

        return render(request, 'home.html', {'classes': instructors_current_classes(request), 'courses': allCourses(),'class_des': class_des, 'student_class_status': student_class_status, 'searchclass': classes, 'courseName': courseName, 'query': q})
    
    if 'register' in request.GET and request.GET['register']:
        q = request.GET['register']

        temp = Enrolled_Class(email = User.objects.get(email = request.session['_auth_user_id']), class_id = Class.objects.get(class_id = q), status = 'Registered')
        temp.save()

        return render(request, 'home.html', {'classes': instructors_current_classes(request), 'courses': allCourses(), 'student_class_status': student_class_status, 'query': q})

    if 'dropclass' in request.GET and request.GET['dropclass']:
        q = request.GET['dropclass']

        temp = Enrolled_Class.objects.filter(class_id = q, email = request.session['_auth_user_id'], status='Registered')
        for i in temp:
            i.status = ''
            i.save()

        return render(request, 'home.html', {'classes': instructors_current_classes(request), 'courses': allCourses(), 'student_class_status': student_class_status, 'query': q})
    else:
        return HttpResponse('Please submit a search term.')

def class_student_info(request):
    template = loader.get_template('manage_users.html')
    enrolled_students = Enrolled_Class.objects.filter(class_id='X201').exclude(role='Instructor')
    students = []
    peer_leaders = []
    inactives = []
    for em in enrolled_students:
        if em.status != 'Active':
            inactives.append(User.objects.get(email=em.email))
        elif em.role == 'Student' and em.status == 'Active':
            students.append(User.objects.get(email=em.email))
        elif em.role == 'Peer Leader' and em.status == 'Active':
            peer_leaders.append(User.objects.get(email=em.email))

    print peer_leaders

    if request.POST:
        print request.POST.get("peer_leader")

        if request.POST.get("activate"):
            return activate(request, enrolled_students, students, peer_leaders, inactives)
        if request.POST.get("deactivate"):
            return deactivate(request, enrolled_students, students, peer_leaders, inactives)
        if request.POST.get("make_peer_leader"):
            return make_peer_leader(request, enrolled_students, students, peer_leaders, inactives)
        if request.POST.get("make_student"):
            return make_student(request, enrolled_students, students, peer_leaders, inactives)
    return render(request, 'manage_users.html', {'enrolled_students': enrolled_students, 'students': students, 'peer_leaders': peer_leaders, 'inactives': inactives})

def activate(request, enrolled_students, students, peer_leaders, inactives):
    #print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWe Made It"
    #print request.POST.get("email")
    #change = inactives
    #times = 1
    for st in enrolled_students:
        if request.POST.get("email") == st.email.email:
            student = st
            #print student.status
            student.status = "Active"
            #print student.status
            student.save()

    for st in inactives:
        #print st
        #print
        if request.POST.get("email") == st.email:
#            print times
#            print request.POST.get("email")
#            print st.email
#            print request.POST.get("email") == st.email
#            print
#
#            print inactives
#            print students
#            print
            inactives.remove(st)
            students.append(st)
#            print inactives
#            print students
#            print
#
#            inactives.append(st)
#            students.remove(st)
#            print students
#            print inactives
#            print
#
#            times = times + 1

#        print "This is try #", times
#        print "This is request.POST.get(\"email\")"
#        print type(request.POST.get("email"))
#        print "This is st.email"
#        print type(st.email.email)
#        print "Are they equal?"
#        print request.POST.get("email") == st.email
#        print
#        times = times + 1

    return render(request, 'manage_users.html', {'enrolled_students': enrolled_students, 'students': students, 'peer_leaders': peer_leaders, 'inactives': inactives})

def deactivate(request, enrolled_students, students, peer_leaders, inactives):
#    change = students
#    times = 1
    for st in enrolled_students:
        if request.POST.get("email") == st.email.email:
            student = st
            #print student.status
            student.status = "Inactive"
            #print student.status
            student.save()

    for st in students:
#        print st
#        print
        if request.POST.get("email") == st.email:
#            print times
#            print request.POST.get("email")
#            print st.email
#            print request.POST.get("email") == st.email
#            print
#
#            print students
#            print inactives
#            print

            students.remove(st)
            inactives.append(st)
#            print students
#            print inactives
#            print
#
#            inactives.remove(st)
#            students.append(st)
#            print students
#            print inactives
#            print
#            times = times + 1

#        print "This is try #", times
#        print "This is request.POST.get(\"email\")"
#        print type(request.POST.get("email"))
#        print "This is st.email"
#        print type(st.email.email)
#        print "Are they equal?"
#        print request.POST.get("email") == st.email
#        print
#        times = times + 1

    return render(request, 'manage_users.html', {'enrolled_students': enrolled_students, 'students': students, 'peer_leaders': peer_leaders, 'inactives': inactives})

def make_peer_leader(request, enrolled_students, students, peer_leaders, inactives):
#    change = students
#    times = 1
    for st in enrolled_students:
        if request.POST.get("email") == st.email.email:
            student = st
            #print student.status
            student.status = "Active"
            student.role = "Peer Leader"
            #print student.status
            student.save()

    for st in students:
#        print st
#        print
        if request.POST.get("email") == st.email:
#            print times
#            print request.POST.get("email")
#            print st.email
#            print request.POST.get("email") == st.email
#            print
#
#            print students
#            print peer_leaders
#            print

            students.remove(st)
            peer_leaders.append(st)
#            print students
#            print peer_leaders
#            print
#
#            peer_leaders.remove(st)
#            students.append(st)
#            print students
#            print peer_leaders
#            print
#            times = times + 1

#        print "This is try #", times
#        print "This is request.POST.get(\"email\")"
#        print type(request.POST.get("email"))
#        print "This is st.email"
#        print type(st.email.email)
#        print "Are they equal?"
#        print request.POST.get("email") == st.email
#        print
#        times = times + 1

    return render(request, 'manage_users.html', {'enrolled_students': enrolled_students, 'students': students, 'peer_leaders': peer_leaders, 'inactives': inactives})

def make_student(request, enrolled_students, students, peer_leaders, inactives):
#    print "I AM IN make_student"
#    print request.POST.get("email")
    for st in enrolled_students:
        if request.POST.get("email") == st.email.email:
            student = st
            #print student.status
            student.status = "Active"
            student.role = "Student"
            #print student.status
            student.save()

    for st in peer_leaders:
#        print st
#        print
        if request.POST.get("email") == st.email:
#            print times
#            print request.POST.get("email")
#            print st.email
#            print request.POST.get("email") == st.email
#            print
#
#            print students
#            print peer_leaders
#            print

            peer_leaders.remove(st)
            students.append(st)
#            print students
#            print peer_leaders
#            print
#
#            peer_leaders.remove(st)
#            students.append(st)
#            print students
#            print peer_leaders
#            print
#            times = times + 1

#        print "This is try #", times
#        print "This is request.POST.get(\"email\")"
#        print type(request.POST.get("email"))
#        print "This is st.email"
#        print type(st.email.email)
#        print "Are they equal?"
#        print request.POST.get("email") == st.email
#        print
#        times = times + 1

    return render(request, 'manage_users.html', {'enrolled_students': enrolled_students, 'students': students, 'peer_leaders': peer_leaders, 'inactives': inactives})
