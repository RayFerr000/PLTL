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
    		signUpButton = driver.find_element_by_id("loginButton")
    		signUpButton.click()

    		WebDriverWait(driver, 100).until(
               		lambda driver: driver.find_element_by_xpath('.//*[@id="emailInput"]'))
    		driver.find_element_by_xpath('.//*[@id="emailInput"]').send_keys("mgross@email.com")
    		pwd_field = driver.find_element_by_xpath('.//*[@id="LoginModal"]/form/div[2]/div/label/input')
    		pwd_field.send_keys("goat")

    		submitLogin = driver.find_element_by_id("submitLogin")
    		submitLogin.click()

    		driver.get("http://127.0.0.1:8000/User/Class/X201/")
                WebDriverWait(driver, 100).until(
               		lambda driver:driver.find_element_by_tag_name('body'))
                body = driver.find_element_by_tag_name('body')
                print body.text
                '''WebDriverWait(driver, 100).until(
               		lambda driver: driver.find_element_by_xpath('.//*[@id="uploadAssignmentButton"]'))
                uploadAssignment = driver.find_element_by_xpath('.//*[@id="uploadAssignmentButton"]')
                uploadAssignment.click()'''
       

	def tearDown(self):
    		self.driver.close()

if __name__ == "__main__":
    		unittest.main()

