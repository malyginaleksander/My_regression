from selenium.webdriver.common.by import By
from Regression.PageFactory.BasePage import BasePage
from selenium import webdriver



class ConfirmPlanPage(BasePage):
    def __init__(self, driver,log):
        super().__init__(driver)
        self.driver = driver
        self.log=log

    #locators
    continueBtn="//*[@id='bg-container']//*[contains(@class,'enroll desktop')]//button"

    def getContinueBtn(self):
      self.log.info("Confirming the plan From ConfirmPlan Page")
      return  self.driver.find_element(By.XPATH,self.continueBtn)

    def clickContinue(self):
      self.getContinueBtn().click()