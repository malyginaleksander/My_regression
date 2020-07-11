import logging
import ConfigFiles.logger as cl
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.utils import keys_to_typing
from selenium import webdriver
from selenium.webdriver.common.by import By
from PageFactory.HomePage import HomePage
from PageFactory.PlansPage import PlansPage
from PageFactory import BasePage
from PageFactory.ConfirmPlanPage import ConfirmPlanPage
from PageFactory.InfoFillingPage import InfoFillingPage
from PageFactory.ConfirmationPage import ConfirmationPage
from PageFactory.VerificationPage import VerificationPage

import pytest


class TestEnrollWeb():
    log = cl.genericLogger(logging.DEBUG)


    def test_Enrollment(self):
       baseURL = "https://www.nrghomepower.com/pa/?mboxSession=a6b56f39c5c549c480cde6a1c2c94733"
       driver = webdriver.Firefox()
       driver.maximize_window()
       driver.implicitly_wait(30)
       driver.get(baseURL)

       hp = HomePage(driver)
       result= hp.verifyHomeTitle("NRG_regression Home Power | NRG_regression")
       assert result == True
       hp.getPlans("15001")
       self.log.info("Entered zip code 15001")


       pp=PlansPage(driver)
       pp.setSelectBtn("Essentials Electric Plan")
       pp.clickSelect()
       print("Selected the product")
       self.log.debug("This is debug info")
       self.log.info("Selected the product")

       cp=ConfirmPlanPage(driver,self.log)
       cp.clickContinue()
       print("clicked on continue")
       self.log.info("clicked on continue")

       ifp=InfoFillingPage(driver)
       ifp.fillData("Geet","saini","gurjeet.saini@nrg.com","gurjeet.saini@nrg.com","(656) 888-7776","Address44","city","15001","4667600675")

       vp=VerificationPage(driver)
       vp.scroll_termsandconditions_and_agree()

       cop=ConfirmationPage(driver)
       confirmationNum = cop.get_confirmation_number()
       print("Confirmation Number is: "+ confirmationNum)
       self.log.info("*************------------------------***************************")
       self.log.info("                                                                ")
       driver.quit()

# tew=TestEnrollWeb()
# tew.test_Enrollment()
