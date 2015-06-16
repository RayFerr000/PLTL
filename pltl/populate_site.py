from User.models import User
from Class.models import Class
from Course.models import Course
from Assignment.models import Assignment
from Enrolled_Class.models import Enrolled_Class
from datetime import datetime, timedelta, date
from Homework.models import Homework

#Create Users
u = User.objects.create_user(fname='Ray', lname='Ferr', email='ray@email.com', password='goat')
u.full_clean()
u = User.objects.create_user(fname='Sam', lname='Tarin', email='tar@email.com', password='goat')
u.full_clean()
u = User.objects.create_user(fname='Praj', lname='Bav', email='praj@email.com', password='goat')
u.full_clean()
u = User.objects.create_user(fname='Ankan', lname='Giri', email='ankan@email.com', password='goat')
u.full_clean()
u = User.objects.create_user(fname='Michelle', lname='Desiqueira', email='mdesi@email.com', password='goat')
u.full_clean()
u = User.objects.create_user(fname='John', lname='Snow', email='jsnow@email.com', password='goat')
u.full_clean()
u = User.objects.create_user(fname='Tyrion', lname='Lannister', email='tlann@email.com', password='goat')
u.full_clean()
u = User.objects.create_user(fname='Charles', lname='Barkley', email='cbark@email.com', password='goat')
u.full_clean()
u = User.objects.create_user(fname='Issac', lname='Newton', email='inew@email.com', password='goat')
u.full_clean()
u = User.objects.create_user(fname='James', lname='Holmes', email='jholmes@email.com', password='goat')
u.full_clean()
u = User.objects.create_user(fname='Michael', lname='Gross', email='mgross@email.com', password='goat')
u.is_staff = True
u.full_clean()
u.save()
u = User.objects.create_superuser(fname='Frandy', lname='Andujar', email='frandy@email.com', password='goat')
u.is_staff = True
u.full_clean()
u.save()

#Create oourse CSC 102 and class X101 of that course
course = Course.objects.create(course_id='CSC 102', course_name='Intro to Computer Science')
course.full_clean()

b = Class.objects.create(class_id='X101', course_id=course, semester='Summer', year='2015', class_description='An introduction to Computer Science')
b.full_clean()

#Create course CSC 202 and class X201 of that course
course = Course.objects.create(course_id='CSC 202', course_name='Intro to Programming')
course.full_clean()

c = Class.objects.create(class_id='X201', course_id=course, semester='Summer', year='2015', class_description='Programming basics in Python')
c.full_clean()

#Create an assignment in the class X201
assign = Assignment.objects.create(assignment_name='Coding For Fun', class_id=Class.objects.get(class_id='X101'), pub_date=date.today(), due_date=date.today()+timedelta(days=8), total_grade=100)
assign.full_clean()

#Create an assignment in the class X201
assign = Assignment.objects.create(assignment_name='Python HW1', class_id=Class.objects.get(class_id='X201'), pub_date=date.today(), due_date=date.today()+timedelta(days=8), total_grade=100)
assign.full_clean()
assign = Assignment.objects.create(assignment_name='Java HW1', class_id=Class.objects.get(class_id='X201'), pub_date=date.today(), due_date=date.today()+timedelta(days=8), total_grade=100)
assign.full_clean()
assign = Assignment.objects.create(assignment_name='Python HW2', class_id=Class.objects.get(class_id='X201'), pub_date=date.today(), due_date=date.today()+timedelta(days=8), total_grade=100)
assign.full_clean()
assign = Assignment.objects.create(assignment_name='Java HW2', class_id=Class.objects.get(class_id='X201'), pub_date=date.today(), due_date=date.today()+timedelta(days=8), total_grade=100)
assign.full_clean()

#Enroll everyone into the Class 'X201'
for user in User.objects.all():
    if user.is_admin == True:
        pass
    elif user.is_staff == True:
        enroll = Enrolled_Class.objects.create(email=user, class_id=b, role='Instructor', status='Registered')
        enroll.full_clean()
    else:
        enroll = Enrolled_Class.objects.create(email=user, class_id=b, role='Student', status='Registered')
        enroll.full_clean()

#Enroll everyone into the Class 'X201'
for user in User.objects.all():
    if user.is_admin == True:
        pass
    elif user.is_staff == True:
        enroll = Enrolled_Class.objects.create(email=user, class_id=c, role='Instructor', status='Registered')
        enroll.full_clean()
    else:
        enroll = Enrolled_Class.objects.create(email=user, class_id=c, role='Student', status='Registered')
        enroll.full_clean()

enrolledStudents = Enrolled_Class.objects.filter(class_id=c).exclude(role='Instructor')

#enroll students into class
for student in enrolledStudents:
    student.status = 'Enrolled'
    student.full_clean()
    student.save()

#make the first two students in the list of all students leaders
for i in xrange(2):
    enrolledStudents[i].role = 'Peer Leader'
    enrolledStudents[i].full_clean()
    enrolledStudents[i].save()

#assign the first half of students to leader 0, second half to leader 1
for i in xrange(8):
    if i < 4:
        enrolledStudents[0].students_led.add(User.objects.get(email=enrolledStudents[i+2].email))
        enrolledStudents[i+2].peer_leader = User.objects.get(email=enrolledStudents[0].email)
        enrolledStudents[0].full_clean()
        enrolledStudents[0].save()
        enrolledStudents[i+2].full_clean()
        enrolledStudents[i+2].save()
    else:
        enrolledStudents[1].students_led.add(User.objects.get(email=enrolledStudents[i+2].email))
        enrolledStudents[i+2].peer_leader = User.objects.get(email=enrolledStudents[1].email)
        enrolledStudents[1].full_clean()
        enrolledStudents[1].save()
        enrolledStudents[i+2].full_clean()
        enrolledStudents[i+2].save()

#For each student in the class, submit a homework for each assignment
homework_number = 0
for student in enrolledStudents:
    if student.role == 'Peer Leader':
        pass
    else:
        for assign in Assignment.objects.all():
            homework = Homework.objects.create(homework_id=homework_number, assignment_id=assign, homework_soln="some solution", submitted_by=student.email, submitted_timestamp=datetime.now())
            homework_number += 1
exit()   
