from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import unittest

class PLTLSearchClass(unittest.TestCase):
	def setUp(self):
    		self.driver = webdriver.Firefox()
    		self.driver.maximize_window()
    		self.driver.get("http://127.0.0.1:8081/")

	def test_search_class_for_user(self):
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
                WebDriverWait(driver, 100).until(
               		lambda driver: driver.find_element_by_tag_name('body'))
                body = driver.find_element_by_tag_name('body')
    		assert "Search" in body.text, "Login Tested"
                WebDriverWait(driver, 100).until(
    			lambda driver: driver.find_element_by_xpath('html/body/div[2]/dl/dd[2]'))
                class_tab = driver.find_element_by_xpath('html/body/div[2]/dl/dd[2]')
                class_tab.click()
                WebDriverWait(driver, 100).until(
    			lambda driver: driver.find_element_by_xpath('.//*[@id="class_id"]')
		)
                search_class = driver.find_element_by_xpath('.//*[@id="class_id"]')
                search_class.send_keys("X201")
                '''hover = ActionChains(driver).move_to_element(search_class)
                hover.perform()
                #hover.send_keys("X201")
		search_class.send_keys("X201")'''
                searchButton = driver.find_element_by_xpath('.//*[@id="btnSearch"]')
                searchButton.click()
                #class_searched = driver.find_element_by_xpath('.//*[@id="classTab"]/div[3]/table/tbody/tr[2]/td[1]').text
                #assert "X201" in class_searched
	def tearDown(self):
    		self.driver.close()

if __name__ == "__main__":
    		unittest.main()

