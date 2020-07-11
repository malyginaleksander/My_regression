from selenium.webdriver.common.by import By
from PageFactory.BasePage import BasePage
from selenium import webdriver
import ConfigFiles.logger as cl
import logging
import ConfigFiles.logger as cl
import time

class NRGPowerHome(BasePage):
    log = cl.genericLogger(logging.DEBUG)

    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver

    singUpNow_loc="//img[@src='/images/NRG_regression-Home_Sign-up-now_button.png']"

    def click_signupnow(self):
        self.driver.find_element(By.XPATH,self.singUpNow_loc).click()
        time.sleep( 4 )

