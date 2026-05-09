#locator file
class Locators:
    username_textbox = "//*[@id=':r1:']"
    password_textbox = "//*[@id=':r2:']"
    login_button = "//*[@id='root']/div[2]/div[2]/div/div[2]/div/div/div[3]/div/div/form/div[4]/button"

    menu = "//*[@id='root']/div[2]/div[2]/div[1]/div/div[2]/div[2]/div"
    logout_button = "//*[@id='root']/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[4]"

    actual_error = "//*[@id=':r2:-helper-text']"
  
#Homepage file
from selenium.common import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from POMtaskfile.Locators.test_locators import *

class Homepage:
    def __init__(self,driver):
        self.driver = driver
        self.menu =Locators.menu
        self.logout_button = Locators.logout_button

    def click_on_menu(self):
     try:
        element = WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH,self.menu)))
        try:
            element.click()
        except ElementClickInterceptedException:
           self.driver.execute_script("arguments[0].click();",element)
     except TimeoutException:
        print(f"Timed out waiting for {self.menu}")
     except Exception as e:
        print(f"An error occurred: {e}")
    def click_logout_button(self):
     try:
        element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, self.logout_button)))
        try:
            element.click()
        except ElementClickInterceptedException:
           self.driver.execute_script("arguments[0].click();",element)
     except TimeoutException:
        print(f"Logout button {self.logout_button} not found in time.")
       
# loginpage file
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from POMtaskfile.Locators.test_locators import *

class LoginPage:
    def __init__(self,driver):
        self.driver = driver
        self.wait = WebDriverWait(driver,20)
        self.username_textbox = Locators.username_textbox
        self.password_textbox = Locators.password_textbox
        self.login_button = Locators.login_button
        self.error_message_locator = Locators.actual_error

    def enter_username(self,username):
        self.driver.find_element(By.XPATH,self.username_textbox).clear()
        self.driver.find_element(By.XPATH, self.username_textbox).send_keys(username)

    def enter_password(self,password):
        self.driver.find_element(By.XPATH,self.password_textbox).clear()
        self.driver.find_element(By.XPATH,self.password_textbox).send_keys(password)

    def click_login_button(self):
        self.driver.find_element(By.XPATH,self.login_button).click()

    def actual_error(self):
        error_element = self.wait.until(
            EC.visibility_of_element_located((By.XPATH, self.error_message_locator))
        )
        return error_element.text
      
# positive test case file
import time
import unittest
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from POMtaskfile.pages.test_homepage import Homepage
from POMtaskfile.pages.test_loginpage import LoginPage


@pytest.mark.positive
class LoginTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)
    def test_login(self):
        driver = self.driver
        driver.get("https://v2.zenclass.in/login")
        login = LoginPage(driver)
        login.enter_username("sap180996@gmail.com")
        login.enter_password("Padmini@123")
        login.click_login_button()

        homepage = Homepage(driver)
        wait = WebDriverWait(driver, 20)
        homepage.click_on_menu()
        time.sleep(2)
        homepage.click_logout_button()

    @classmethod
    def tearDown(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main()
  
#negative test case file
import unittest
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from POMtaskfile.pages.test_loginpage import LoginPage

@pytest.mark.negative
class LoginTest(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(20)
    def test_login(self):
        driver = self.driver
        driver.get("https://v2.zenclass.in/login")
        wait = WebDriverWait(driver, 10)
        login = LoginPage(driver)
        login.enter_username("sap180996@gmail.com")
        login.enter_password("Padmini")
        login.click_login_button()

        actual_error = login.actual_error()
        self.assertEqual(login.actual_error(),"*Incorrect password!")

    @classmethod
    def tearDown(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main()
  
