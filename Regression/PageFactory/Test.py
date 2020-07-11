

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.utils import keys_to_typing
from selenium import webdriver
from selenium.webdriver.common.by import By




class Test():

    def testEnrollment(self):
       baseURL = "https://www.google.com"
       driver = webdriver.Firefox()
       driver.maximize_window()
       driver.implicitly_wait(3)
       driver.get(baseURL)


tew=Test()
tew.testEnrollment()