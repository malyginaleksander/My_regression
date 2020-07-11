import logging
import ConfigFiles.logger as cl
import time
from PageFactory.BasePage import BasePage


class EnergyPlusEnroll(BasePage):
    log = cl.genericLogger(logging.DEBUG)
    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver
        self.driver.implicitly_wait(15)

    # Common and Enrollment locators
    state_loc="state"
    firstName_loc = "first_name"
    middleName_loc = "middle_initial"
    lastName_loc = "last_name"
    email_loc = "email_addr"
    verifyEmail_loc = "confirm_email_addr"
    phoneNum_loc = "Service_phone_number"
    streetAdd_loc = "Service_Address1"
    streetAdd2_loc = "Service_Address2"
    city_loc = "Service_City"
    zipcode_loc = "Service_Zip5"
    continueBtn = "billing"
    clickImag_loc="/html/body/div/div[2]/form/div[9]/div[2]/a/img"
    name_key_confirm_loc="/html/body/div/div[2]/form/div[11]/div[3]/div[1]/div[1]/div[4]/div[2]/div[3]/div[2]/label[1]/input"
    btnUtilSubmit_loc="btnUtilSubmit"
    page_loc="page"

    #Electric locators

    AccountMainElectric_loc= "AccountMainElectric"
    localUtility_loc="LocalUtility"
    option_loc="option"
    resbus_loc="resbus"
    accountNo2_loc="accountNo2"
    accountNo_loc="accountNo"
    avgMonthUsage_loc="average_month_usage"
    busNameDet_loc="busnamedet"
    drpTaxYes_loc="drpTaxYes"
    greenopt_loc="greenopt"

    #Gas locators
    gasNo_loc = "chkGasNo"
    AccountMainGas_loc="AccountMainGas"
    gastypesel_loc="gastypesel"
    usageUnits_loc="usage_units"
    usageMonth_loc = "usage_month"

    # Rewards Information locators
    partner_memnum_loc="partner_memnum"
    pfname_loc="pfname"
    plname_loc="plname"
    partnerSubmitbtn_loc = "partnerSubmitbtn"

    # Submit Locators
    authorizeYes_loc = "authorizeYes"
    submitbtn_loc = "submitbutton"

    #Conf. Locators
    confirmation_loc="confirmationCode"

    def enterFName(self, fName):
        self.sendKeys(fName, self.firstName_loc)
    def enterMName(self,mName):
        self.sendKeys(mName,self.middleName_loc)
    def enterLName(self, lName):
        self.sendKeys(lName, self.lastName_loc)
    def enterEmail(self, email):
        self.sendKeys(email, self.email_loc)
    def enterVerifyEmail(self, verifyEmail):
        self.sendKeys(verifyEmail, self.verifyEmail_loc)
    def enterPhoneNum(self, phoneNum):
        self.elementClick(self.phoneNum_loc)
        self.sendKeys(phoneNum, self.phoneNum_loc)
    def enterStreetAdd(self, streetAdd):
        self.sendKeys(streetAdd, self.streetAdd_loc)
    def enterStreetAdd2(self, streetAdd):
        self.sendKeys(streetAdd, self.streetAdd2_loc)
    def enterCity(self, city):
        self.sendKeys(city, self.city_loc)
    def enterZipcode(self, zipcode):
        self.elementClick(self.zipcode_loc)
        self.sendKeys(zipcode, self.zipcode_loc)
    def clickContinue(self):
        self.elementClick(self.continueBtn)
    def clickNameKeyConfirm(self):
        self.elementClick( self.name_key_confirm_loc, "xpath" )

    #reuseable methods


    def fill_personal_info_EP_web(self, payload):
        # Personal Information
        elem = self.driver.find_element_by_id(self.firstName_loc).send_keys(payload.first_name)
        elem = self.driver.find_element_by_id(self.middleName_loc).send_keys(payload.middle_initial)
        elem = self.driver.find_element_by_id(self.lastName_loc).send_keys(payload.last_name)
        elem = self.driver.find_element_by_id(self.email_loc).send_keys(payload.email_addr)
        elem = self.driver.find_element_by_id(self.verifyEmail_loc).send_keys(payload.confirm_email_addr)
        elem = self.driver.find_element_by_id(self.streetAdd_loc).send_keys(payload.Service_Address1)
        elem = self.driver.find_element_by_id(self.streetAdd2_loc).send_keys("apt 2a")
        elem = self.driver.find_element_by_id(self.city_loc).send_keys(payload.Service_City)
        elem = self.driver.find_element_by_id(self.zipcode_loc).click()
        elem = self.driver.find_element_by_id(self.zipcode_loc).send_keys(str(payload.zipcode))
        elem = self.driver.find_element_by_id(self.phoneNum_loc).click()
        elem = self.driver.find_element_by_id(self.phoneNum_loc).send_keys(str(payload.phone))
        elem = self.driver.find_element_by_id("billing").click()
        elem = self.driver.find_element_by_xpath("/html/body/div/div[2]/form/div[9]/div[2]/a/img").click()


    def check_gas(self, payload):
        self.driver.find_element_by_id(self.gasNo_loc).is_displayed()
        elem = self.driver.find_element_by_id(payload.elect_gas_radio).click()
        time.sleep(2)  #Need sleep


    def clickGasNo(self,payload):
        try:
            time.sleep(4)
            if self.driver.find_element_by_id(self.gasNo_loc).is_displayed():
                elem = self.driver.find_element_by_id(payload.elect_gas_radio).click()
                time.sleep(2)
        except:
            pass

    def selectOption(self,elem,valueToSelect):
        time.sleep(1)
        for option in elem.find_elements_by_tag_name(self.option_loc):
            if option.text == valueToSelect:
                option.click()
                time.sleep(1)
                break


    def fillEnrollDetails(self,payload,streetAdd2,city):
        # Personal Information
        self.enterFName( payload.first_name )
        self.enterMName( payload.middle_initial )
        self.enterLName( payload.last_name )
        self.enterEmail( payload.email_addr )
        self.enterVerifyEmail( payload.confirm_email_addr )
        self.enterStreetAdd( payload.Service_Address1 )
        self.enterStreetAdd( streetAdd2 )
        self.enterCity( city )
        self.enterZipcode( payload.zipcode )
        self.enterPhoneNum( str(payload.phone) )
        self.elementClick( self.continueBtn )
        self.elementClick( self.clickImag_loc, "xpath" )

    def fillElectricDetails_EPWeb_ChoicePage(self,payload):
     self.driver.find_element_by_id(self.AccountMainElectric_loc).is_displayed()
     elem = self.driver.find_element_by_class_name(self.localUtility_loc)
     self.selectOption(elem, payload.LocalUtility)
     elem = self.driver.find_element_by_class_name(self.resbus_loc)
     self.selectOption(elem, payload.account_type)
     self.driver.find_element_by_class_name(self.accountNo2_loc).is_displayed()
     self.driver.find_element_by_class_name(self.accountNo_loc).send_keys(str(payload.accountNo))
     if payload.greenopt_check == "yes":
        elem = self.driver.find_element_by_class_name(self.greenopt_loc).click()
        time.sleep( 6 )

    def fillElectricDetails_EPWeb_IL(self, payload, drptaxyes_text):
      self.driver.find_element_by_id(self.AccountMainElectric_loc).is_displayed()
      elem = self.driver.find_element_by_class_name(self.localUtility_loc)
      self.selectOption(elem, payload.LocalUtility)
      elem = self.driver.find_element_by_class_name(self.resbus_loc)
      self.selectOption(elem, payload.account_type)
      self.driver.find_element_by_class_name(self.accountNo2_loc).is_displayed()
      self.driver.find_element_by_class_name(self.accountNo_loc).send_keys(str(payload.accountNo))
      if self.driver.find_element_by_class_name(self.busNameDet_loc).is_displayed():
         elem = self.driver.find_element_by_class_name(self.busNameDet_loc).send_keys(payload.busnamedet)
      if self.driver.find_element_by_class_name(self.drpTaxYes_loc).is_displayed():
         elem = self.driver.find_element_by_class_name(self.drpTaxYes_loc)
         self.selectOption(elem, drptaxyes_text)  # drptaxyes text:  No, I'm non-exempt
      if payload.greenopt_check == "yes":
         elem = self.driver.find_element_by_class_name(self.greenopt_loc).click()
      time.sleep(6)


    def fillElectricDetails_EPWeb_MA_MD_NJ_PA(self, payload, avgMonthUsageText, drptaxyes_text):
          if self.driver.find_element_by_id(self.AccountMainElectric_loc).is_displayed():
              elem = self.driver.find_element_by_class_name(self.localUtility_loc)
              self.selectOption(elem, payload.LocalUtility)
              elem = self.driver.find_element_by_class_name(self.resbus_loc)
              self.selectOption(elem, payload.account_type)
              if self.driver.find_element_by_class_name(self.accountNo2_loc).is_displayed():
                  elem = self.driver.find_element_by_class_name(self.accountNo2_loc).send_keys(str(payload.accountNo))
                  elem = self.driver.find_element_by_class_name(self.accountNo_loc).send_keys(str(payload.sr_num))
                  self.clickNameKeyConfirm()  # name key confirm
              else:
                  self.driver.find_element_by_class_name(self.accountNo_loc).send_keys(str(payload.accountNo))
              if self.driver.find_element_by_class_name(self.avgMonthUsage_loc).is_displayed():
                  elem = self.driver.find_element_by_class_name(self.avgMonthUsage_loc)
                  self.selectOption(elem, avgMonthUsageText)  # the value is:    Less than 10,000 kWh
              if self.driver.find_element_by_class_name(self.busNameDet_loc).is_displayed():
                  elem = self.driver.find_element_by_class_name(self.busNameDet_loc).send_keys(payload.busnamedet)
              if self.driver.find_element_by_class_name(self.drpTaxYes_loc).is_displayed():
                  elem = self.driver.find_element_by_class_name(self.drpTaxYes_loc)
                  self.selectOption(elem, drptaxyes_text)  # drptaxyes text:  No, I'm non-exempt
              if payload.greenopt_check == "yes":
                  elem = self.driver.find_element_by_class_name(self.greenopt_loc).click()
              time.sleep(2)


    def fill_gas_details_for_MD_NJ(self, payload, usageUnits, usageMonth, drptaxyes_text):
       ## Gas
         if payload.enroll_gas == "Yes":
             time.sleep(2)
             elem = self.driver.find_element_by_id( self.AccountMainGas_loc )
             elem = elem.find_element_by_class_name( self.localUtility_loc )
             self.selectOption( elem, payload.LocalUtility )
             elem = self.driver.find_element_by_id( self.AccountMainGas_loc )
             elem = elem.find_element_by_class_name( self.resbus_loc )
             self.selectOption( elem, payload.account_type )
             elem = self.driver.find_element_by_id( self.AccountMainGas_loc )
             if payload.gastypesel != "No":
               elem = elem.find_element_by_class_name( self.gastypesel_loc )  # gastypesel
               self.selectOption( elem, payload.gastypesel )
             elem = self.driver.find_element_by_id( self.AccountMainGas_loc )
             elem.find_element_by_class_name( self.accountNo_loc ).send_keys(str(payload.accountNo))
             if payload.usage_units_month=="Yes":
               elem = self.driver.find_element_by_id(self.AccountMainGas_loc)
               elem = elem.find_element_by_class_name(self.usageUnits_loc).send_keys(usageUnits)  #123
               elem = self.driver.find_element_by_id(self.AccountMainGas_loc)
               elem = elem.find_element_by_class_name(self.usageMonth_loc)
               self.selectOption( elem, usageMonth )    #usageMonth: July
             if payload.businessName=="Yes":
               elem = self.driver.find_element_by_id( self.AccountMainGas_loc )
               elem.find_element_by_class_name(self.busNameDet_loc).send_keys(payload.busnamedet)
             if payload.Taxfield=="Yes":
               elem = self.driver.find_element_by_id( self.AccountMainGas_loc )
               elem = elem.find_element_by_class_name(self.drpTaxYes_loc)
               self.selectOption( elem, drptaxyes_text )   #drpTaxYes Text is: No, I'm non-exempt


    def submitData(self):
        elem = self.driver.find_element_by_id( self.btnUtilSubmit_loc ).click( )
        time.sleep( 2 )


    def fillRewardsInfo(self,payload):
        # Rewards Information
        elem = self.driver.find_element_by_id(self.partner_memnum_loc ).send_keys(str(payload.memnum))   #2198765432
        elem = self.driver.find_element_by_id(self.pfname_loc ).send_keys( payload.pfname )
        elem = self.driver.find_element_by_id(self.plname_loc).send_keys( payload.plname )
        elem = self.driver.find_element_by_id( self.partnerSubmitbtn_loc ).click()

    def clickSubmit(self):
        # Submit
        elem = self.driver.find_element_by_id( self.authorizeYes_loc ).click()
        elem = self.driver.find_element_by_id( self.authorizeYes_loc).click()
        elem = self.driver.find_element_by_id( self.submitbtn_loc ).click()


    def EP_Confirmation(self):
        time.sleep(2)
        elem = self.driver.find_element_by_id(self.confirmation_loc)
        confcode = elem.text
        print("Confirmation =  " + confcode)


    # EP Web enroll fill electric details
    def fillElectricForEPWeb(self,payload, avgMonthUsageText,drptaxyes_text):
       # Electric
       self.driver.find_element_by_id(self.AccountMainElectric_loc).is_displayed()
       elem = self.driver.find_element_by_class_name(self.localUtility_loc)
       self.selectOption(elem, payload.LocalUtility)
       elem = self.driver.find_element_by_class_name(self.resbus_loc)
       self.selectOption(elem, payload.account_type)
       self.driver.find_element_by_class_name(self.accountNo2_loc).is_displayed()
       self.driver.find_element_by_class_name(self.accountNo_loc).send_keys(str(payload.accountNo))
       self.driver.find_element_by_class_name(self.drpTaxYes_loc).is_displayed()
       elem = self.driver.find_element_by_class_name(self.drpTaxYes_loc)

