from selenium import webdriver
from django.test import LiveServerTestCase
from django.conf import settings
from Assignment.models import Assignment
from Homework.models import Homework
from Enrolled_Class.models import Enrolled_Class
from selenium.webdriver.common.keys import Keys
import unittest
import time

def create_session_store():
    """ Creates a session storage object. """
    from django.utils.importlib import import_module
    engine = import_module(settings.SESSION_ENGINE)
    # Implement a database session store object that will contain the session key.
    store = engine.SessionStore()
    store.save()
    return store
 
class GradeAssignmentTest(LiveServerTestCase):  
    assignments = None
    assignment = None
    

    def setUp(self):
     	try:
            execfile('populate_site.py') 
        except SystemExit as e:
            pass
        #Choose the first assignment to test
        self.assignments = Assignment.objects.all()
        self.assignment = self.assignments[0]
 
        url = '/Class/Assignments/'+str(self.assignment.assignment_id)+'/Grade'
        self.selenium.get('%s%s' % (self.live_server_url,  url))


    def tearDown(self):
        self.selenium.quit()   
    def test_correct_assignment_name_displayed(self):
        header_text = self.selenium.find_element_by_tag_name('h4').text
        self.assertIn(self.assignment.assignment_name, header_text)
    def test_form_for_each_homework_submission(self):
        homeworkCount =  Homework.objects.filter(assignment_id = self.assignment.assignment_id).count()
        self.assertTrue(self.selenium.find_element_by_id('form'+str(homeworkCount)))

    def test_submitting_form_show_green_check(self):
        #Load the instructor into the session
        session_store = create_session_store()
        session_items = session_store
        session_items['_auth_user_id'] = 'mgross@email.com'
        session_items.save()
        
        save = self.selenium.find_element_by_id('Submit1')
        check = self.selenium.find_element_by_id('check1')
        self.assertFalse(check.is_displayed())
        save.send_keys('1')
        save.click()
        
        time.sleep(3)
        self.assertTrue(check.is_displayed())

