from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

class PLTLLogin(unittest.TestCase):
	def setUp(self):
    		self.driver = webdriver.Firefox()
    		self.driver.maximize_window()
    		self.driver.get("http://127.0.0.1:8000/")

	def test_sign_up(self):
                driver = self.driver
    		signUpButton = driver.find_element_by_id("signUpButton")
    		signUpButton.click()

    		WebDriverWait(driver, 100).until(
               		lambda driver: driver.find_element_by_xpath('.//*[@id="emailInput"]'))
    		driver.find_element_by_xpath('.//*[@id="emailInput"]').send_keys("praj@email.com")
    		pwd_field = driver.find_element_by_xpath('.//*[@id="LoginModal"]/form/div[2]/div/label/input')
    		pwd_field.send_keys("goat")

    		submitLogin = driver.find_element_by_id("submitLogin")
    		submitLogin.click()

    		body = driver.find_element_by_tag_name('body')
    		assert "Search" in body.text, "Login Tested"
    		assert "Create" not in body.text, "Login Tested"
    		#print body.text
       
       def test_login_for_instructor(self):
                driver = self.driver
    		loginButton = driver.find_element_by_id("loginButton")
    		loginButton.click()

    		WebDriverWait(driver, 100).until(
               		lambda driver: driver.find_element_by_xpath('.//*[@id="emailInput"]'))
    		driver.find_element_by_xpath('.//*[@id="emailInput"]').send_keys("praj@email.com")
    		pwd_field = driver.find_element_by_xpath('.//*[@id="LoginModal"]/form/div[2]/div/label/input')
    		pwd_field.send_keys("goat")

    		submitLogin = driver.find_element_by_id("submitLogin")
    		submitLogin.click()

    		body = driver.find_element_by_tag_name('body')
    		assert "Search" in body.text, "Login Tested"
    		assert "Create" in body.text, "Login Tested"
    		#print body.text

	def tearDown(self):
    		self.driver.close()

if __name__ == "__main__":
    		unittest.main()

