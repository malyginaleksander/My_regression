from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Regression.PageFactory.BasePage import BasePage
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import logging
import Regression.ConfigFiles.logger as cl
import time
import datetime
import uuid
from datetime import datetime


class ConfirmationPage(BasePage):
   log = cl.genericLogger(logging.DEBUG)

   def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver


   #locators

   def get_confirmation_number(self, payload):
       # time.sleep(2)
       self.confirm_text = self.driver.find_element_by_xpath(
           "//*[@class='section row personal-info-section']/../div/div[2]")
       print(self.confirm_text.text)
       self.confirm_text_data = self.confirm_text.text
       now = datetime.now()
       current_time = now.strftime("_%m_%d_%Y_%I_%M_%S_%p_")
       self.driver.get("http://nerf.api.pt.nrgpl.us/api/v1/orders/?enrollment_number=" + str(self.confirm_text.text))

       WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'List all Orders, or create a new order')]")))

       self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[4]/pre/a[2]").click()

       time.sleep(5)

       self.sap_conf = self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[4]/pre/span[79]")
       self.uan_number = self.driver.find_element_by_xpath("//*[@id='content']/div[1]/div[4]/pre/span[25]")
       print(self.sap_conf.text, self.uan_number.text)

       time.sleep(1)

       # file = open( "./TextFileConfirmations/test_confirmationTextFiles.txt", 'a')
       # file = open( "./TextFileConfirmations/test_confirmationTextFiles_{}_{}".format(payload.ts, uuid.uuid4())  + str(current_time)+ "textfile.txt", 'a')
       # file = open( "./TextFileConfirmations/test_confirmationTextFiles_{}_{}".format(payload.tc, uuid.uuid4()) + str(self.date) + "textfile.txt", 'a')
       print(self.confirm_text_data)

       # file.write("enrollment # = " +str(self.confirm_text_data)+ "     sap conf. #= " +str(self.sap_conf.text)+ "       uan #=" +str(self.uan_number.text))

       time.sleep(1)













