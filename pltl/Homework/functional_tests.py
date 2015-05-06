from django.test import  TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class GradeAssignmentPageTest(TestCase):

    def setup(self):
        self.browser = webdriver.Firefox()
    
    def teardown(self):
        self.browser.quit()
    
    def test_form_for_each_student(self):
        self.browser.get('http://localhost:8000/Class/Assignments/Grade')
        self.fail('finish')
