from selenium.webdriver.common.by import By
from PageFactory.BasePage import BasePage
from selenium import webdriver

class InfoFillingPage(BasePage):
        def __init__(self, driver):
            super().__init__(driver)
            self.driver = driver

        # locators
        firstName_loc="id_first_name"
        lastName_loc="id_last_name"
        email_loc="id_email"
        verifyEmail_loc="id_ver_email"
        phoneNum_loc="id_phone"
        streetAdd_loc="id_service_address_1"
        city_loc="id_service_address_city"
        zipcode_loc="id_service_address_zip"
        agreementId_loc="id_electric-uan"
        continueBtn="continue-submit"
        acctNo_loc="id_electric-billing_uan"
        mem_fName_loc="id_member_first_name"
        mem_lName_loc="id_member_last_name"
        mem_num_loc="id_partner_member_number"


        def enterMemfName(self,fName):
            self.sendKeys(fName,self.mem_fName_loc)
        def enterMemLName(self,lName):
            self.sendKeys(lName,self.mem_lName_loc)
        def enterMemNum(self,memNum):
            self.sendKeys(memNum,self.mem_num_loc)

        def enterAcctNum(self,acctNo):
            self.sendKeys(acctNo,self.acctNo_loc)

        def enterFName(self,fName):
            self.sendKeys(fName,self.firstName_loc)

        def enterLName(self,lName):
            self.sendKeys(lName,self.lastName_loc)
        def enterEmail(self,email):
            self.sendKeys(email,self.email_loc)
        def enterVerifyEmail(self,verifyEmail):
            self.sendKeys(verifyEmail,self.verifyEmail_loc)
        def enterPhoneNum(self,phoneNum):
             self.sendKeys(phoneNum,self.phoneNum_loc)
        def enterStreetAdd(self,streetAdd):
             self.sendKeys(streetAdd,self.streetAdd_loc)
        def enterCity(self,city):
             self.sendKeys(city,self.city_loc)
        def enterZipcode(self,zipcode):
             self.sendKeys(zipcode,self.zipcode_loc)
        def enterAgreementDetails(self,agrID):
             self.sendKeys(agrID,self.agreementId_loc)
        def clickContinue(self):
             self.elementClick(self.continueBtn)


        def fillData(self,payload):
           self.enterFName(payload.fName)
           self.enterLName(payload.lName)
           self.enterEmail(payload.email)
           self.enterVerifyEmail(payload.vEmail)
           self.enterPhoneNum(payload.phoneNum)
           self.enterStreetAdd(payload.streetAdd)
           self.enterCity(payload.city)
           self.enterZipcode(payload.zipcode)
           self.enterAgreementDetails(payload.agrId)


        def fillMemDet(self,payload):
           try:
             self.enterAcctNum(payload.accountNo)
             self.enterMemfName(payload.first_name)
             self.enterMemLName(payload.last_name)
             self.enterMemNum( payload.member_number )
           except:
             pass
           self.clickContinue( )