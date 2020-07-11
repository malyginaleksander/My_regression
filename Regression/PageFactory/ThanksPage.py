from selenium.webdriver.common.by import By
from Regression.PageFactory.BasePage import BasePage
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import logging
import Regression.ConfigFiles.logger as cl

class ThanksPage(BasePage):
   log = cl.genericLogger(logging.DEBUG)

   def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver



   #locators
   thanks_loc="thanks"

   def getthanksText(self):
       return self.getElementText(self.thanks_loc)

    # def getEPConfirmCode(self, idText):
      #   return self.getElementText(idText)

   # def getConfirmationNum(self):
       # self.log.info("Displaying the confirmation number from Confirmation Page")
       # return self.getconfirmationText()