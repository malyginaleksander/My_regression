#from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.by import By
from Regression.ECC_PageFactory.SignUpFromMail import SignUpFromMail
import time

class test_SignUpAccount():

    def click_portallink_signup(self, driver, confirmationNum, password, payload):

        driver.get("https://accounts.google.com/signin/v2/identifier?hl=en&continue=https%3A%2F%2Fmail.google.com%2Fmail&service=mail&flowName=GlifWebSignIn&flowEntry=Identifier")
        registerAcct = SignUpFromMail(driver)
        registerAcct.gmail_login(payload)
        self.driver.implicitly_wait(10)
        pwh = driver.current_window_handle

        registerAcct.search_email_click_signuplink(confirmationNum)
        registerAcct.registerportal_login(pwh, password, payload)

        driver.switch_to.window( pwh )

    def click_termsofservice_link(self, driver, confirmationNum, password, payload):

        driver.get("https://accounts.google.com/signin/v2/identifier?hl=en&continue=https%3A%2F%2Fmail.google.com%2Fmail&service=mail&flowName=GlifWebSignIn&flowEntry=Identifier")
        registerAcct = SignUpFromMail(driver)
        registerAcct.gmail_login(payload)
        time.sleep(1)
        pwh = driver.current_window_handle

        registerAcct.click_toslink(confirmationNum)


    def click_portal_link(self, driver, confirmationNum, password, payload):

        driver.get("https://accounts.google.com/signin/v2/identifier?hl=en&continue=https%3A%2F%2Fmail.google.com%2Fmail&service=mail&flowName=GlifWebSignIn&flowEntry=Identifier")
        registerAcct = SignUpFromMail(driver)
        registerAcct.gmail_login(payload)
        time.sleep(1)
        pwh = driver.current_window_handle

        registerAcct.search_email_click_signuplink(confirmationNum)

#tsignup= SignUpAccount()
#tsignup.clickLinkNdSignUp(driver,confirmationNum,password)