"""user view"""
# -*- coding: utf-8 -*-
from django.shortcuts import redirect, render_to_response, RequestContext
from django.shortcuts import render
from django.template import RequestContext, loader
from User.models import User
from django.http import HttpResponse
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from Class.forms import ClassForm
from Class.models import Class, get_semester
from Course.models import Course, allCourses
from Class.views import instructors_current_courses_classes
from Class.views import student_current_class_status
from Enrolled_Class.models import Enrolled_Class

def user_signup_save(request):
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User(fname=fname, lname=lname, email=email,
    last_login=datetime.now())
    user.set_password(password)
    #force_insert=True forces the database to do an insert rather then an update
    status = user.save(force_insert=True)
    if status == 'success':
        subject = 'Welcome to PLTL'
        with open("templates/SignUpNotification.txt", "r") as data:
            msgbody = data.read()
        msg = 'Dear ' + fname +',\n' + msgbody
        from_mail = settings.EMAIL_HOST_USER
        send_mail(subject, msg, from_mail, [email, from_mail],
        fail_silently=True)
    return redirect('home')

def login(request):
    # After login Create class can be called
    if request.POST.get('class_id'):
        return create_class(request)

    if request.POST.get('email'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)

    elif request.session['_auth_user_id']:
        # Instructors Current class and course will be generated on pageload
        sem = get_semester
        year = datetime.now().year
        return render_to_response('home.html', {'sem':sem, 'year':year,
        'inscourses':instructors_current_courses_classes(request),
        'student_class_status':student_current_class_status(request),
        'courses':allCourses()}, context_instance=RequestContext(request))

    if user is not None:
        auth.login(request, user)
        # Instructors Current class and course will be generated on pageload
        sem = get_semester
        year = datetime.now().year
        return render_to_response('home.html', {'sem':sem, 'year': year,
        'inscourses': instructors_current_courses_classes(request),
        'student_class_status': student_current_class_status(request),
        'courses': allCourses()}, context_instance=RequestContext(request))
    else:
        return HttpResponse("invalid, not logged in")

def logout(request):
    auth.logout(request)
    return render(request, 'index.html')

''' This function will create class taking course id from course table '''
def create_class(request):
    sem = get_semester
    year = datetime.now().year
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            new_class = form.save()
            enroll_class = Enrolled_Class(email=User.objects.get(
            email=request.session['_auth_user_id']),
            class_id=Class.objects.get(\
            class_id=request.POST.get('class_id')), role='Instructor')
            enroll_class.full_clean()
            enroll_class.save()
    else:
        form = ClassForm()
    return render_to_response('home.html', {'sem':sem, 'year': year,
    'inscourses': instructors_current_courses_classes(request),
    'student_class_status': student_current_class_status(request),
    'courses': allCourses(), 'form': form},
    context_instance=RequestContext(request))

''' This function will search, drop and register class '''
def search_classes(request):
    sem = get_semester
    year = datetime.now().year
    if 'class_id' in request.GET and request.GET['class_id']:
        srch = request.GET['class_id']
        classes = Class.objects.filter(class_id=srch).values()
        # return course name of the searched class
        course_name = Course.objects.filter(course_id=(Class.objects.filter(
        class_id=srch).values('course_id'))).values('course_name')
        # return class description
        class_des = Class.objects.filter(
        class_id=srch).values('class_description', 'class_id')
        class_details = Class.objects.filter(class_id=srch).values()
        if len(classes) == 0:
            label = 'NoRecordFound'
        if len(classes) != 0:
            label = 'RecordFound'

        return render(request, 'home.html', {'sem':sem,
        'year': year, 'label':label,
        'inscourses': instructors_current_courses_classes(request),
        'courses': allCourses(), 'class_des': class_des,
        'class_details':class_details,
        'student_class_status': student_current_class_status(request),
        'searchclass': classes, 'courseName': course_name, 'query': srch})

    if 'register' in request.GET and request.GET['register']:
        # if student wants to rester for class
        reg = request.GET['register']
        # check if the student already registered for the class
        # if not insert else update
        temp, created = Enrolled_Class.objects.get_or_create(
        email=User.objects.get(email=request.session['_auth_user_id']),
        class_id=Class.objects.get(class_id=reg), role='Student',
        defaults={'status' : 'Registered'})
        if not created:
            temp.status = 'Registered'
            temp.save()
        label = 'register'
        return render(request, 'home.html', {'label':label, 'sem':sem,
        'year': year,
        'inscourses': instructors_current_courses_classes(request),
        'courses': allCourses(),
        'student_class_status': student_current_class_status(request),
        'query': reg})

    if 'dropclass' in request.GET and request.GET['dropclass']:
        # if student wants to drop the class
        drop = request.GET['dropclass']
        drop_temp = Enrolled_Class.objects.filter(email=User.objects.get(
        email=request.session['_auth_user_id']), class_id=Class.objects.get(
        class_id=drop), status='Registered', role='Student')
        drop_temp.update(status='')
        label = 'drop'
        enrollstudent = Enrolled_Class.objects.filter(
        email=request.session['_auth_user_id'],
        class_id=drop, status='Enrolled').values('class_id')
        if len(enrollstudent) == 0:
            label2 = 'none'
        if len(enrollstudent) != 0:
            label2= 'yes'
        return render(request, 'home.html', {'label':label,
        'label2': label2,
        'sem':sem,
        'year': year,
        'inscourses': instructors_current_courses_classes(request),
        'courses': allCourses(),
        'student_class_status': student_current_class_status(request)})
    else:
        return HttpResponse('Please submit a search term.')

''' This function will update class details if exists update else insert '''
def update_class_details(request):
    sem = get_semester
    year = datetime.now().year
    class_Id = request.POST.get('updateClass')
    course_Id = request.POST.get('updateCourse')
    semester_Id = request.POST.get('updateSem')
    yearId = request.POST.get('updateYear')
    class_des = request.POST.get('updateClassDes')
    temp_semester = Class.objects.filter(class_id=class_Id,
    course_id=Course.objects.get(
    course_id=course_Id)).values('semester')
    tempYear = Class.objects.filter(class_id=class_Id,
    course_id=Course.objects.get(course_id=course_Id)).values('year')
    tempClassDes = Class.objects.filter(class_id=class_Id,
    course_id=Course.objects.get(
    course_id=course_Id)).values('class_description')
    update, created = Class.objects.get_or_create(class_id=class_Id,
    course_id=Course.objects.get(
    course_id=course_Id), defaults={
    'semester' : temp_semester, 'year' : tempYear,
    'class_description' : tempClassDes})
    # check if the class id exist or not
    if not created:
        update.semester = semester_Id
        update.year = yearId
        update.class_description = class_des
        update.save()
        label = 'success'

    return render(request, 'home.html', {'label':label, 'sem':sem,
    'year': year, 'searchclass' : temp_semester,
    'inscourses': instructors_current_courses_classes(request),
    'courses': allCourses(),
    'student_class_status': student_current_class_status(request)})


"""this function will divide users into instructors, peer leaders, registered and enrolled users"""
def class_student_info(request, class_id):
    enrolled = Enrolled_Class.objects.filter(class_id=class_id).exclude(role='Instructor')
    instructors = Enrolled_Class.objects.filter(class_id=class_id, role='Instructor')
    show = False
    if request.user.is_authenticated():
        if request.user.is_staff:
            for instructor in instructors:
                if request.user.email == instructor.email.email:
                    show = True
        elif request.user.is_admin:
            show = True

    registered_students = []
    enrolled_students = []
    peer_leaders = []

    for em in enrolled:
        if em.status == 'Registered':
            registered_students.append(User.objects.get(email=em.email))
        elif em. role == 'Student' and em.status == 'Enrolled':
            enrolled_students.append(User.objects.get(email=em.email))
        elif em.role == 'Peer Leader' and em.status == 'Enrolled':
            peer_leaders.append(User.objects.get(email=em.email))

    if request.POST:
        if request.POST.get("enroll"):
            return enroll(request, show, class_id, enrolled, registered_students, enrolled_students, peer_leaders)
        if request.POST.get("remove"):
            return remove(request, show, class_id, enrolled, registered_students, enrolled_students, peer_leaders)
        if request.POST.get("make_peer_leader"):
            return make_peer_leader(request, show, class_id, enrolled, registered_students, enrolled_students, peer_leaders)
        if request.POST.get("make_student"):
            return make_student(request, show, class_id, enrolled, registered_students, enrolled_students, peer_leaders)
        if request.POST.get("student_led"):
            return student_led(request, show, class_id, enrolled, registered_students, enrolled_students, peer_leaders)

    return render(request, 'manage_users.html', {'show': show, 'class_id': class_id, 'enrolled': enrolled, 'registered_students': registered_students, 'enrolled_students':enrolled_students, 'peer_leaders': peer_leaders})

'''enroll will remove a student from the registered list and add him to the enrolled list'''
def enroll(request, show, class_id, enrolled, registered_students, enrolled_students, peer_leaders):
    for student in enrolled:
        if request.POST.get("email") == student.email.email:
            student.role = 'Student'
            student.status = 'Enrolled'
            student.full_clean()
            student.save()
    for student in registered_students:
        if request.POST.get("email") == student.email:
            registered_students.remove(student)
            enrolled_students.append(student)
    return render(request, 'manage_users.html', {'show': show, 'class_id': class_id, 'enrolled': enrolled, 'registered_students': registered_students, 'enrolled_students':enrolled_students, 'peer_leaders': peer_leaders})

'''remove will remove a student from enrolled and put him back into registered list'''
def remove(request, show, class_id, enrolled, registered_students, enrolled_students, peer_leaders):
    for student in enrolled:
        if request.POST.get("email") == student.email.email:
            student.role = 'Student'
            student.status = 'Registered'
            if student.peer_leader != None:
                for leader in enrolled:
                    if leader.email == student.peer_leader:
                        leader.students_led.remove(student.email)
            student.peer_leader = None
            student.full_clean()
            student.save()
    for student in enrolled_students:
        if request.POST.get("email") == student.email:
            enrolled_students.remove(student)
            registered_students.append(student)

    return render(request, 'manage_users.html', {'show': show, 'class_id': class_id, 'enrolled': enrolled, 'registered_students': registered_students, 'enrolled_students':enrolled_students, 'peer_leaders': peer_leaders})

'''make peer leader takes a student from enrolled and add him to the list of peer leaders'''
def make_peer_leader(request, show, class_id, enrolled, registered_students, enrolled_students, peer_leaders):
    for student in enrolled:
        if request.POST.get("email") == student.email.email:
            student.role = 'Peer Leader'
            student.status = 'Enrolled'
            student.full_clean()
            student.save()
    for student in enrolled_students:
        if request.POST.get("email") == student.email:
            enrolled_students.remove(student)
            peer_leaders.append(student)
    return render(request, 'manage_users.html', {'show': show, 'class_id': class_id, 'enrolled': enrolled, 'registered_students': registered_students, 'enrolled_students':enrolled_students, 'peer_leaders': peer_leaders})

'''the student will be added to the specified peer leaders group'''
def student_led(request, show, class_id, enrolled, registered_students, enrolled_students, peer_leaders):
    for leader in enrolled:
        if request.POST.get("student_leader") == leader.email.email:
            for student in enrolled:
                if request.POST.get("email") == student.email.email:
                    if student.peer_leader != None:
                        for other_leader in enrolled:
                            if other_leader.email == student.peer_leader:
                                other_leader.students_led.remove(student.email)
                    leader.students_led.add(student.email)
                    student.peer_leader = leader.email
                    leader.full_clean()
                    student.full_clean()
                    leader.save()
                    student.save()
    return render(request, 'manage_users.html', {'show': show, 'class_id': class_id, 'enrolled': enrolled, 'registered_students': registered_students, 'enrolled_students':enrolled_students, 'peer_leaders': peer_leaders})

'''remove all of the peer leaders students and make him a student again'''
def make_student(request, show, class_id, enrolled, registered_students, enrolled_students, peer_leaders):
    for leader in enrolled:
        if request.POST.get("email") == leader.email.email:
            leader.role = 'Student'
            leader.status = 'Enrolled'

            if leader.students_led.exists():
                for student in leader.students_led.all():
                    for student_led in enrolled:
                        if student == student_led.email:
                            student_led.peer_leader = None
                            student_led.full_clean()
                            student_led.save()

            leader.students_led.clear()
            leader.full_clean()
            leader.save()

    for leader in peer_leaders:
        if request.POST.get("email") == leader.email:
            peer_leaders.remove(leader)
            enrolled_students.append(leader)
    return render(request, 'manage_users.html', {'show': show, 'class_id': class_id, 'enrolled': enrolled, 'registered_students': registered_students, 'enrolled_students':enrolled_students, 'peer_leaders': peer_leaders})

'''this function will group students with their peer leaders'''
def group_view(request, class_id):
    peer_leaders = Enrolled_Class.objects.filter(class_id='X201', role='Peer Leader')
    instructors = Enrolled_Class.objects.filter(class_id=class_id, role='Instructor')
    group_view = {}
    show = False
    if request.user.is_authenticated():
        if request.user.is_staff:
            for instructor in instructors:
                if request.user.email == instructor.email.email:
                    show = True
        elif request.user.is_admin:
            show = True
    for leader in peer_leaders:
        group_view[leader.email] = leader.students_led.all()

    return render(request, 'group_view.html', {'show': show, 'class_id': class_id, 'group_view': group_view})
