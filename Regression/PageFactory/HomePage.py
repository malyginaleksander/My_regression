from selenium.webdriver.common.by import By
from PageFactory.BasePage import BasePage
from selenium import webdriver
import ConfigFiles.logger as cl
import logging
import ConfigFiles.logger as cl
import time

class HomePage(BasePage):
    log = cl.genericLogger(logging.DEBUG)

    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver


    # locators
    zipCode = "//div[*[contains(text(),'Enter your ZIP Code')]]/input";
    clickBtn = "//button[contains(text(),'Find plans')]"


    zipCode_loc="template_variable_zipcode"
    seePlansBtn_loc="/html/body/div/div[2]/form/button"

    # test compare checkbox page
    zip_code1 = "/html/body/div[3]/div[2]/div[1]/form/div/input"
    shopNow_loc = "/html/body/div[3]/div[2]/div[1]/form/div/button"
    def shopNow(self,payload):
        self.driver.find_element( By.XPATH,self.zip_code1 ).send_keys( payload.zipcode )
        self.driver.find_element(By.XPATH,self.shopNow_loc).click()    #shop now button


    def checkPlans(self,payload):
        self.driver.find_element(By.NAME,self.zipCode_loc).send_keys(payload.zipcode)
        self.driver.find_element(By.XPATH,self.seePlansBtn_loc).click()   #See plans button
        time.sleep( 3 )

    def landingPageLinkCheck(self,payload):
        self.driver.find_element(By.XPATH,payload.xpath).click()
        try:
            self.driver.switch_to.alert.accept( )
        except:
            pass

    def getPlans(self, zipcode):
        self.getZipCodeField().send_keys(zipcode)
        self.getFindPlansBtn().click()
        self.log.info("Entered zipcode. From HomePage")

    def getZipCodeField(self):
        return self.driver.find_element(By.XPATH,self.zipCode)
        #return self.driver.findElement(By.NAME,self.zipCode)

    def getFindPlansBtn(self):
        return self.driver.find_element(By.XPATH,self.clickBtn)


    def enterZipCode(self,zipcode):
        self.getZipCodeField().sendKeys(zipcode)

    def clickFindPlans(self):
        self.clickFindPlans().click()


    def verifyHomeTitle(self,homeTitle):
        return self.verifyTitle(homeTitle)



