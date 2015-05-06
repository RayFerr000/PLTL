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
u = User.objects.create_user(fname='Michael', lname='Gross', email='mgross@email.com', password='goat')
u.is_staff = True
u.full_clean()
u.save()
u = User.objects.create_superuser(fname='Frandy', lname='Andujar', email='frandy@email.com', password='goat')
u.is_staff = True
u.full_clean()
u.save()

#Create course CSC 102 and class X101 of that course
course = Course.objects.create(course_id='CSC 102', course_name='Intro to Computer Science')
course.full_clean()
#course.save()
c = Class.objects.create(class_id='X101', course_id=course, semester='Spring', year='2015', class_description='An introduction to Computer Science')
c.full_clean()
##c.save()
#
#Create course CSC 202 and class X201 of that course
course = Course.objects.create(course_id='CSC 202', course_name='Intro to Programming')
course.full_clean()
#course.save()
c = Class.objects.create(class_id='X201', course_id=course, semester='Spring', year='2015', class_description='Programming basics in Python')
c.full_clean()
##c.save()
##.save()

#Create an assignment in the class X201
assign = Assignment.objects.create(assignment_name='Python HW1', class_id=Class.objects.get(class_id='X201'), pub_date=date.today(), due_date=date.today()+timedelta(days=8), total_grade=100)
assign.full_clean()
#assign.save()

#Enroll everyone into the Class 'X201'and create an instance of homework for each which corresponds to the assignnment
homework_number = 0
for user in User.objects.all():
    if user.is_admin == True:
        pass
    elif user.is_staff == True:
        enroll = Enrolled_Class.objects.create(email=user, class_id=c, role='Instructor', status='DEFAULT VALUE')
        enroll.full_clean()
    else:
        register = Enrolled_Class.objects.create(email=user, class_id=c, role='Student', status='Registered')
        register.full_clean()
        homework = Homework.objects.create(homework_id=homework_number, assignment_id=assign, homework_soln="some solution", submitted_by=user.email, submitted_timestamp=datetime.now())
        homework.full_clean()
        homework_number += 1
exit()
#user1 = User.objects.get(fname='Ray')
#user2 = User.objects.get(fname='Sam')
#user3 = User.objects.get(fname='Praj')
#enroll1 = Enrolled_Class.objects.create(email=user1, class_id=c, role='Student', status='Registered')
#enroll1.full_clean()
