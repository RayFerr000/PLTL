from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class PLTLCreateAssignment(unittest.TestCase):
	def setUp(self):
    		self.driver = webdriver.Firefox()
    		self.driver.maximize_window()
    		self.driver.get("http://127.0.0.1:8000/")

	def test_create_assignment(self):
               
                driver = self.driver
    		loginButton = driver.find_element_by_id("loginButton")
    		loginButton.click()

    		WebDriverWait(driver, 100).until(
               		lambda driver: driver.find_element_by_xpath('.//*[@id="emailInput"]'))
    		driver.find_element_by_xpath('.//*[@id="emailInput"]').send_keys("mgross@email.com")
    		pwd_field = driver.find_element_by_xpath('.//*[@id="LoginModal"]/form/div[2]/div/label/input')
    		pwd_field.send_keys("goat")

    		submitLogin = driver.find_element_by_id("submitLogin")
    		submitLogin.click()

    		#assert "Search" in body.text, "Login Tested"
    		#assert "Create" in body.text, "Login Tested"
                
		WebDriverWait(driver, 100).until(
               		lambda driver:driver.find_element_by_xpath('.//*[@id="classTab"]'))
                create_tab = driver.find_element_by_xpath('.//*[@id="classTab"]')
                create_tab.click()
                class_name = driver.find_element_by_xpath('.//*[@id="class_id"]')                
                classname = 'csc'+strftime("%H:%M:%S", gmtime())
                classname = classname.replace(':', '')
                class_name.send_keys(classname)
                course_select = driver.find_element_by_xpath('.//*[@id="classTab"]/div[1]/section/form/div[1]/div[2]/select/option[2]')
                course_select.click()
                semester = driver.find_element_by_xpath('.//*[@id="classTab"]/div[1]/section/form/div[2]/div[1]/select/option[2]')
                semester.click()
                year = driver.find_element_by_xpath('.//*[@id="year"]')
                year.send_keys("2015")
                class_description = driver.find_element_by_xpath('.//*[@id="class_description"]')
                class_description.send_keys("description of the class goes here")
                
                WebDriverWait(driver, 100).until(
               		lambda driver:driver.find_element_by_xpath('.//*[@id="btnNew"]'))
                createButton = driver.find_element_by_xpath('.//*[@id="btnNew"]')
                createButton.click()
                driver.refresh()
                alert = driver.switch_to.alert()
                print alert.text
		alert.accept()
                
                WebDriverWait(driver, 100).until(
               		lambda driver:driver.find_element_by_xpath('.//*[@id="createdClasses"]/tbody/tr[2]/td[1]/a'))
                classExisting = driver.find_element_by_xpath('.//*[@id="createdClasses"]/tbody/tr[2]/td[1]/a')
                print classExisting.text
                classExisting.click()               
                
                uploadAssignment = driver.find_element_by_xpath('.//*[@id="uploadAssignmentButton"]')
                uploadAssignment.click()
                WebDriverWait(driver, 100).until(
               		lambda driver:driver.find_element_by_xpath('.//*[@id="id_assignment_name"]'))
                uploadAssignmentName = driver.find_element_by_xpath('.//*[@id="id_assignment_name"]')
                upload_Assignment = 'csc'+strftime("%H:%M:%S", gmtime())
                upload_Assignment = upload_Assignment.replace(':', '')
                uploadAssignmentName.send_keys(upload_Assignment)
                
                uploadAssignmentgrades = driver.find_element_by_xpath('.//*[@id="id_total_grade"]')
                uploadAssignmentgrades.send_keys("20")
                elem = driver.find_element_by_xpath('.//*[@id="id_assignmentfile"]')
		elem.send_keys("/home/prajakta/ads/test.c")
                createAssignment = driver.find_element_by_xpath('.//*[@id="create"]')
                createAssignment.click()
                
                
                WebDriverWait(driver, 100).until(
               		lambda driver:driver.find_element_by_xpath('.//*[@id="assignmentListDetails"]/tbody/tr[1]/td[1]/a'))
                assignment_created = driver.find_element_by_xpath('.//*[@id="assignmentListDetails"]/tbody/tr[1]/td[1]/a')
                
                assert upload_Assignment in assignment_created
       

	def tearDown(self):
    		self.driver.close()

if __name__ == "__main__":
    		unittest.main()

