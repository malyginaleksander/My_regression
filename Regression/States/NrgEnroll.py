from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Regression.PageFactory.BasePage import BasePage
import logging
import Regression.ConfigFiles.logger as cl
from selenium import webdriver
import time

class NrgEnroll(BasePage):
        def __init__(self, driver):
            super().__init__(driver)
            self.driver = driver

        log = cl.genericLogger(logging.DEBUG)

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
        phone_mark_Pref_loc="phone_marketing_consent_span"
        email_Mark_Pref_loc="email_marketing_consent_span"
        mark_data_Pref_loc="data_sharing_consent_span"
        save_Pref_loc="communication_preferences_agree"
        email_domain_error_loc="id_email_domain-error"
        email_match_error_loc="id_ver_email-error"
        valid_email_address_loc="id_email-error"
        thankyou_page_loc= "col-md-12"
        elec_utility_loc="electric-utility_slug"
        img_loc="/html/body/div/div[2]/center[2]/span/a/img"
        signup_now_NRG_loc="html/body/div[2]/div[2]/center/a/img"

        #gas
        gasUan_loc="id_gas-uan"
        gasUtilitySlug_loc="id_gas-utility_slug"
        option_loc = "option"
        service_point_id_loc="id_gas-uan"

            # Plans Page

        selectelectricutility_planspage_loc = '//div[@id="plan-utility-header-electric"]//div//div//a[contains(text(),"Select Electric Utility …")]'
        clickGasUtility_dd_loc = '//div[@class="gas-utility-selector"]//div[contains(@class,"select")]/a'
        continue_loc = '//div[contains(@class,"enroll desktop")]//button[@class="enroll-btn"]'
        naturalgasplan_loc ='show-gas-plans'
        gasutlity_dropdown= '//div[@id="plan-utility-header-gas"]//div//div//a[contains(text(),"Select Gas Utility …")]'
        clickElectricUtlity_dropdown_confirmplanpage= '//div[@class="electric-utility-selector"]//div[contains(@class,"select")]/a'
        click_stateDD_loc='//div[@id="plan-state-header"]//div[contains(@class,"state-select-widget")]/input[@class="state-input"]'
        select_stateDD_loc='//div[@id="plan-state-header"]//div[contains(@class,"state-select-widget")]/div/a[contains(text(),"Pennsylvania")]'

        zipcodeForPlans_loc='//label[contains(text(),"Narrow plans by zip code")]//..//div//input[@name="zipcode"]'
        shopplans_pricingloc='//label[contains(text(),"Narrow plans by zip code")]//..//div//button[@class="zip-submit"]'

        menuLink_loc = '//div[@id="menu"]//li//a[contains(text(),"Shop")]'
        planType_loc = ''



        def enter_member_firstname(self, fName):
            self.sendKeys(fName,self.mem_fName_loc)
        def enter_member_lastname(self, lName):
            self.sendKeys(lName,self.mem_lName_loc)
        def enter_member_number(self, memNum):
            self.sendKeys(str(memNum),self.mem_num_loc)
        def enter_account_number(self, acctNo):
            self.sendKeys(str(acctNo),self.acctNo_loc)
        def enterGasAcct(self, gasNo):
            self.sendKeys(gasNo,self.gasUan_loc)
        def enter_firstname(self, fName):
            self.sendKeys(fName,self.firstName_loc)
        def enter_lastname(self, lName):
            self.sendKeys(lName,self.lastName_loc)
        def enter_email(self, email):
            self.sendKeys(email,self.email_loc)
        def enter_verifyemail(self, verifyEmail):
            self.sendKeys(verifyEmail,self.verifyEmail_loc)
        def enter_phonenumber(self, phoneNum):
            self.sendKeys(str(phoneNum),self.phoneNum_loc)
        def enter_streetaddress(self, streetAdd):
            self.sendKeys(streetAdd,self.streetAdd_loc)
        def enter_city(self, city):
            self.sendKeys(city,self.city_loc)
        def enter_zipcode(self, zipcode):
            self.sendKeys(str(zipcode),self.zipcode_loc)
        def enter_agreementdetails(self, agrID):
            self.sendKeys(str(agrID),self.agreementId_loc)
        def click_continue(self):
            # self.elementClick(self.continueBtn)
            self.driver.find_element_by_id(self.continueBtn).click()
        def phone_marketing_preferences(self):
            self.elementClick(self.phone_mark_Pref_loc)
        def email_marketing_preferences(self):
            self.elementClick(self.email_Mark_Pref_loc)
        def marketing_data_preferences(self):
            self.elementClick(self.mark_data_Pref_loc)
        def save_preferences(self):
            self.elementClick(self.save_Pref_loc)
        def select_option(self, elem, valueToSelect):
            for option in elem.find_elements_by_tag_name( self.option_loc ):
                if option.text == valueToSelect:
                    option.click( )
                    time.sleep( 1 )


        ## Enroll
        def clickImage(self):
            elem = self.driver.find_element_by_xpath(self.signup_now_NRG_loc).click()
            time.sleep(2)


        ## Personal Information
        def enter_personal_information(self, payload):
            elem = self.driver.find_element_by_id(self.firstName_loc).send_keys(payload.first_name)
            elem = self.driver.find_element_by_id(self.lastName_loc).send_keys(payload.last_name)
            elem = self.driver.find_element_by_id(self.email_loc).send_keys(payload.email_addr)
            elem = self.driver.find_element_by_id(self.verifyEmail_loc).send_keys(payload.confirm_email_addr)
            elem = self.driver.find_element_by_id(self.phoneNum_loc).send_keys(str(payload.Service_phone_number))
            elem = self.driver.find_element_by_id(self.streetAdd_loc).send_keys(payload.Service_Address1)
            elem = self.driver.find_element_by_id(self.city_loc).send_keys(payload.city)
            elem = self.driver.find_element_by_id(self.zipcode_loc).send_keys(str(payload.zipcode))
            time.sleep(2)


        def enter_electric_account_details(self, payload):

            billing_address_loc= 'id_billing_address_1'
            billing_city_loc= 'id_billing_address_city'

            elem = self.driver.find_element_by_id(self.agreementId_loc).send_keys(payload.accountNo)
            try:
                elem = self.driver.find_element_by_id(self.acctNo_loc).send_keys(payload.accountNo)
            except:
                pass
            time.sleep(2)
            elem = self.driver.find_element_by_id(self.continueBtn).click()
            time.sleep(4)


        def select_ElectricUtility_and_submit(self, payload):
            elem = self.driver.find_element_by_name(self.elec_utility_loc)
            if elem.is_displayed():
                for option in elem.find_elements_by_tag_name(self.option_loc):
                    if option.text == payload.utility:
                        option.click()
                        break

            elem = self.driver.find_element_by_id(self.agreementId_loc).send_keys(payload.accountNo)
            try:
                elem = self.driver.find_element_by_id(self.acctNo_loc).send_keys(payload.accountNo)
            except:
                pass
            time.sleep(2)
            elem = self.driver.find_element_by_id(self.continueBtn).click()
            time.sleep(4)

        def click_useasitis(self):
            try:
                self.driver.find_element_by_xpath('//div//a[contains(text(),"Use as it is")]').click()
            except:
                pass


        def fill_data(self, payload):

            self.enter_firstname(payload.first_name)
            self.enter_lastname(payload.last_name)
            self.enter_email(payload.email_addr)
            self.enter_verifyemail(payload.confirm_email_addr)
            self.enter_phonenumber(payload.Service_phone_number)
            self.enter_streetaddress(payload.Service_Address1)
            self.enter_city(payload.city)
            # self.click_useasitis()
            time.sleep(2)
            self.driver.find_element_by_id(self.zipcode_loc).click()
            time.sleep(3)
            self.click_useasitis()
            self.driver.find_element_by_id(self.zipcode_loc).click()
            self.driver.find_element_by_id(self.zipcode_loc).send_keys(str(payload.zipcode))
            self.enter_agreementdetails(payload.accountNo)
            self.driver.implicitly_wait(2)

        def isElementExists(driver, by, value):
         try:
            driver.implicitly_wait(1)
            driver.find_element(by, value)
            driver.implicitly_wait(60)
            return True
         except Exception:
            return False

        def no_at_no_dot(self, payload):
            isAtTheRateExist = payload.email_addr.find( '@', 2 )
            print( str( isAtTheRateExist ) + " is index of @" )
            if (isAtTheRateExist <= 0):
             assert self.driver.find_element_by_id(self.valid_email_address_loc).is_displayed()
            print( "@ symbol is being displayed" )
            isDotExist = payload.email_addr.find( '.', isAtTheRateExist + 2 )
            print( str( isDotExist ) + " is the index of dot" )
            if (isDotExist <= 0):
             assert self.driver.find_element_by_id(self.valid_email_address_loc).is_displayed()
            else:
             print( "dot is being displayed" )

        def fill_data_no_at_and_no_dot(self, payload):
             self.enter_firstname(payload.first_name)
             self.enter_lastname(payload.last_name)
             self.enter_email(payload.email_addr)
             self.enter_verifyemail(payload.confirm_email_addr)
             self.no_at_no_dot(payload)
             self.enter_phonenumber(payload.Service_phone_number)
             self.enter_streetaddress(payload.Service_Address1)
             self.enter_city(payload.city)
             self.enter_zipcode(payload.zipcode)
             self.enter_agreementdetails(payload.accountNo)
             self.enter_member_number(payload.member_number)
             self.click_continue()
             time.sleep(2)
             if payload.email_addr.lower() not in payload.confirm_email_addr.lower()  or  payload.confirm_email_addr.lower() not in   payload.email_addr.lower() :
                assert self.driver.find_element_by_id(self.email_match_error_loc).is_displayed()
             print(payload.VerifyConfNo)
             if payload.VerifyConfNo == "No":
                errMsg_loc="//div//*[contains(text(),'"+payload.VerifyErrMsg+"')]"
                assert self.driver.find_element_by_xpath(errMsg_loc).is_displayed()
             print("emails don't match. exception occured")
             time.sleep(4)

        def blacklisted_email(self, payload):

             self.enter_firstname(payload.first_name)
             self.enter_lastname(payload.last_name)
             self.enter_email(payload.email_addr)
             self.driver.implicitly_wait(2)
             self.enter_verifyemail(payload.confirm_email_addr)
             self.driver.implicitly_wait(2)
             print("check error msg")
             if payload.Invalid_domain in payload.email_addr.lower():
                 self.log.info("Verifying the domain like @example etc. Error Msg should be displayed ")
                 assert self.driver.find_element_by_id(self.email_domain_error_loc).is_displayed()
                 print("Asserted the Error message for email domain error")
                 error_text = self.driver.find_element_by_id(self.email_domain_error_loc).text
                 print(error_text)
                 file = open("./TextFileConfirmations/test_confirmationTextFiles.txt", 'a')
                 file.write(payload.confirm_email_addr + " " + "__Email error Text = '" + error_text + "'  ")
             else:
                 try:
                     error_text = self.driver.find_element_by_id('id_email-error').text
                     print(error_text)
                     file = open("./TextFileConfirmations/test_confirmationTextFiles.txt", 'a')
                     file.write(payload.confirm_email_addr + " " + "__Email error Text = '" + error_text + "'  ")
                 except:
                     pass



             self.no_at_no_dot(payload)
             self.driver.implicitly_wait(2)
             self.enter_phonenumber(payload.Service_phone_number)
             self.enter_streetaddress(payload.Service_Address1)
             self.enter_city(payload.city)
             # time.sleep(1)
             self.driver.find_element_by_id(self.zipcode_loc).click()
             # time.sleep(3)
             WebDriverWait(self.driver, 10).until(
                 EC.element_to_be_clickable((By.XPATH, '//div//a[contains(text(),"Use as it is")]')))


             self.click_useasitis()
             self.driver.find_element_by_id(self.zipcode_loc).click()
             # time.sleep(2)
             self.driver.find_element_by_id(self.zipcode_loc).send_keys(str(payload.zipcode))
             self.enter_agreementdetails(payload.accountNo)
             self.enter_member_number(payload.member_number)

             try:
                 time.sleep(3)
                 account_details_loc = self.driver.find_element_by_xpath("//div//div//*[contains(text(),'Account Details')]")
                 # time.sleep(4)
                 self.driver.execute_script("return arguments[0].scrollIntoView();", account_details_loc)
                 # time.sleep(2)
             except:
                 pass

             try:
                 time.sleep(3)
                 United_MileagePlusMiles_loc = self.driver.find_element_by_xpath("//div//div//*[contains(text(),'United MileagePlus Miles')]")
                 # time.sleep(4)
                 self.driver.execute_script("return arguments[0].scrollIntoView();", United_MileagePlusMiles_loc)
                 # time.sleep(2)
             except:
                 pass

             self.click_continue()
             self.driver.implicitly_wait(2)
             if payload.email_addr.lower() not in payload.confirm_email_addr.lower()  or  payload.confirm_email_addr.lower() not in payload.email_addr.lower() :
                assert self.driver.find_element_by_id(self.email_match_error_loc).is_displayed()
                print("Asserted the Error message for the Email Match error")
             print(payload.VerifyConfNo)

             if payload.VerifyConfNo == "No":
                errMsg_loc="//div//*[contains(text(),'"+payload.VerifyErrMsg+"')]"
                assert self.driver.find_element_by_xpath(errMsg_loc).is_displayed()
                print("Stop and do not proceed to the Confirmation page.Asserted the error message from the payload ")
             else:
                 print ("Error Message shown. Proceed to the Confirmation Page. ")



        def fill_memberdetails(self, payload):
             self.enter_account_number(payload.accountNo)
             self.enter_member_firstname(payload.first_name)
             self.enter_member_lastname(payload.last_name)
             self.enter_member_number(payload.member_number)
             self.click_continue()


        def fill_MemberDetails_Dual(self, payload):
            try:
                self.driver.find_element_by_id(self.mem_num_loc).send_keys(str(payload.member_number))
            except:
                pass

        def verify_error_message(self,payload):
            errMsg_loc="//*[text()='"+payload.error_msg+"']"
            assert self.driver.find_element_by_xpath(errMsg_loc).is_displayed()
            print("Asserted the Error message for gas account number")

        def fill_memberdetails_for_badmember(self, payload):
             self.enter_account_number(payload.accountNo)
             time.sleep( 2 )
             self.click_continue()
             time.sleep(2)
             assert self.driver.find_element_by_xpath("//div//*[contains(text(),'Member number is required')]").is_displayed()

        def fill_gasdata(self, payload):
            elem = self.driver.find_element_by_id(self.gasUtilitySlug_loc)
            self.select_option(elem, payload.gas_util)
            time.sleep( 4 )
            self.enterGasAcctDetailsLandingPage(payload)
            time.sleep(2)

        def preferences_selection_confirmationpage(self, payload):
            time.sleep(2)
            service_add_loc=self.driver.find_element_by_xpath("//div//div//*[contains(text(),'Same as Service Address')]")
            time.sleep(4)
            self.driver.execute_script("return arguments[0].scrollIntoView();", service_add_loc)
            if payload.phone_marketing_preferences in "Yes":
               self.phone_marketing_preferences()
            if payload.email_marketing_preferences in "Yes":
               self.email_marketing_preferences()
            if payload.marketing_data_preferences in "Yes":
               self.marketing_data_preferences()
            time.sleep(1)
            self.save_preferences()
            time.sleep(3)
            assert self.driver.find_element_by_class_name(self.thankyou_page_loc).is_displayed()
            print("asserted the ThankYou Page")


        def select_allpreferences_on_confirmationpage(self):
            time.sleep(1)
            service_add_loc=self.driver.find_element_by_xpath("//div//div//*[contains(text(),'Same as Service Address')]")
            time.sleep(4)
            self.driver.execute_script("return arguments[0].scrollIntoView();", service_add_loc)
            self.phone_marketing_preferences()
            self.email_marketing_preferences()
            self.marketing_data_preferences()
            self.save_preferences()
            assert self.driver.find_element_by_class_name(self.thankyou_page_loc).is_displayed()
            print("asserted the ThankYou Page")

        def verify_invalid_email(self, payload):
             self.enter_firstname(payload.first_name)
             self.enter_lastname(payload.last_name)
             self.enter_email(payload.email_addr)
             self.enter_verifyemail(payload.confirm_email_addr)
             time.sleep(2)
             self.enter_phonenumber(payload.Service_phone_number)
             self.enter_streetaddress(payload.Service_Address1)
             self.enter_city(payload.city)
             self.driver.find_element_by_id(self.zipcode_loc).click()
             time.sleep(3)
             self.driver.find_element_by_id(self.zipcode_loc).send_keys(str(payload.zipcode))
             self.enter_agreementdetails(payload.accountNo)
             self.enter_member_number(payload.member_number)
             self.click_continue()
             time.sleep(4)
             assert self.driver.find_element_by_id(self.valid_email_address_loc).is_displayed()
             print("Exception while finding the error message")
             time.sleep(4)

        def check_invalid_email(self, payload):
             assert self.driver.find_element_by_id(self.valid_email_address_loc).is_displayed()
             print("Exception while finding the error message")
             time.sleep(4)

        def Click_SignUpNow(self):
            self.driver.find_element_by_xpath("//img[@src='/images/NRG_regression-Home_Sign-up-now_button.png']").click()
            time.sleep(4)

        def Click_SignUpNow_IL(self, payload):
            self.driver.find_element_by_xpath(payload.signup_loc).click()
            time.sleep(4)


        def enterGasAcctDetails(self, payload):
            if payload.Service_Point_ID == "" or payload.Service_Point_ID is None:
                self.driver.find_element_by_id(self.gasUan_loc).send_keys(str(payload.gas_account))
            else:
                elem = self.driver.find_element_by_id(self.service_point_id_loc).send_keys(str(payload.Service_Point_ID))
                time.sleep(2)
                self.driver.find_element_by_id("id_gas-billing_uan").click()
                self.driver.find_element_by_id("id_gas-billing_uan").send_keys(str(payload.gas_account))

        def enterGasAcctDetailsLandingPage(self, payload):
            self.driver.find_element_by_id(self.gasUan_loc).send_keys(str(payload.gas_account))

        def landing_invalid_zip(self,payload):
            elem = self.driver.find_element_by_xpath("//div//*[contains(text(),'Enter your ZIP Code')]//following-sibling::*[1]").send_keys(payload.zipcode)
            elem = self.driver.find_element_by_xpath("//div//*[contains(text(),'Enter your ZIP Code')]//following-sibling::*[2]").click()  # See plans button
            time.sleep(3)

            assert "We don't currently service homes in the ZIP code "+payload.zipcode+"." in self.driver.page_source

        def landing_valid_zip(self, payload):
            self.driver.find_element_by_xpath("//div//p/a[text()='Home']").click()
            self.driver.switch_to.alert.accept()

            elem = self.driver.find_element_by_xpath(
                "//div//*[contains(text(),'Enter your ZIP Code')]//following-sibling::*[1]").send_keys(payload.zipcode)
            elem = self.driver.find_element_by_xpath(
                "//div//*[contains(text(),'Enter your ZIP Code')]//following-sibling::*[2]").click()  # See plans button
            time.sleep(3)

            assert self.driver.find_element_by_xpath("//div//div//*[@id='show-electric-plans']").is_displayed()
            assert self.driver.find_element_by_xpath("//div//div//*[@id='show-gas-plans']").is_displayed()


        def select_electric_utility(self,payload):
            self.driver.find_element_by_xpath(self.selectelectricutility_planspage_loc).click()
            self.selectUtilities_loc = '//div[@id="plan-utility-header-electric"]//div//div//a[contains(text(),"Select Electric Utility …")]//parent::div/div/a[contains(text(),"'+payload.utility_name+'")]'
            self.driver.find_element_by_xpath(self.selectUtilities_loc).click()

        select_plan_loc=''
        def select_electric_plan(self,payload):
            self.select_plan_loc = '//div[@class="plan-wrapper"]//h3[contains(text(),"'+payload.planName+'")]//parent::div//parent::div//div//a//button[contains(text(),"Select")]'
            el1 = self.driver.find_element_by_xpath('//h3[contains(text(),"' + payload.planName + '")]')
            webdriver.ActionChains(self.driver).move_to_element(el1).perform()
            webdriver.ActionChains(self.driver).move_to_element(el1).perform()
            time.sleep(3)
            el = self.driver.find_element_by_xpath(self.select_plan_loc)
            webdriver.ActionChains(self.driver).move_to_element(el).perform()
            webdriver.ActionChains(self.driver).move_to_element(el).perform()
            time.sleep(3)
            webdriver.ActionChains(self.driver).click(el).perform()

        def select_gas_utility(self,payload):
            self.driver.find_element_by_xpath(self.clickGasUtility_dd_loc ).click()
            self.gas_utility_loc = '//div[@class="gas-utility-selector"]//div//a[contains(@href,"selected")][contains(text(),"'+payload.gasUtilityName+'")]'


            el1 = self.driver.find_element_by_xpath(self.gas_utility_loc)
            webdriver.ActionChains(self.driver).move_to_element(el1).perform()
            time.sleep(3)
            self.other_gas_utility='//div//h2[contains(text(),"Did you know we offer Gas plans?")]'
            el = self.driver.find_element_by_xpath(self.other_gas_utility)
            webdriver.ActionChains(self.driver).move_to_element(el).perform()
            webdriver.ActionChains(self.driver).move_to_element(el).perform()
            time.sleep(3)
            el1 = self.driver.find_element_by_xpath(self.gas_utility_loc)
            webdriver.ActionChains(self.driver).click(el1).perform()
            # self.driver.find_element_by_xpath(self.gas_utility_loc).click()


        def select_gas_plan(self,payload):
            self.select_gas_plan_loc = '//h3[contains(text(),"'+payload.gasPlanName+'")]//parent::div//a//button[text()="Select"]'
            print(self.select_gas_plan_loc)
            el1 = self.driver.find_element_by_xpath('//h3[contains(text(),"'+payload.gasPlanName+'")]')
            self.driver.execute_script("return arguments[0].scrollIntoView();", el1)
            time.sleep(3)
            el = self.driver.find_element_by_xpath(self.select_gas_plan_loc)
            webdriver.ActionChains(self.driver).click(el).perform()


        def click_naturalgasplan(self):
            self.driver.find_element_by_id(self.naturalgasplan_loc).click()


        def clickcontinue_planspage(self,payload):
            time.sleep(3)
            self.driver.find_element_by_xpath(self.continue_loc).click()

        def select_gas_utility_planspage(self,payload):
            self.driver.find_element_by_xpath(self.gasutlity_dropdown).click()
            self.selectgasUtilities_loc = '//div[@id="plan-utility-header-gas"]//div//div//a[contains(text(),"Select Gas Utility …")]//parent::div/div/a[contains(text(),"'+payload.gasUtilityName+'")]'
            self.driver.find_element_by_xpath(self.selectgasUtilities_loc).click()

        def select_gas_plan_planspage(self,payload):
            self.select_gasplan_planspage_loc = '//div[@class="plan-wrapper"]//h3[contains(text(),"' + payload.gasPlanName + '")]//parent::div//parent::div//div//a//button[contains(text(),"Select")]'
            el1 = self.driver.find_element_by_xpath('//h3[contains(text(),"' + payload.gasPlanName + '")]')
            webdriver.ActionChains(self.driver).move_to_element(el1).perform()
            webdriver.ActionChains(self.driver).move_to_element(el1).perform()
            time.sleep(3)
            el = self.driver.find_element_by_xpath(self.select_gasplan_planspage_loc)
            webdriver.ActionChains(self.driver).move_to_element(el).perform()
            webdriver.ActionChains(self.driver).move_to_element(el).perform()
            time.sleep(5)
            if payload.gasPlanName in "Gas plan that benefits Big Brothers Big Sisters":
                el1 = self.driver.find_element_by_xpath('//h3[contains(text(),"Cash Back Natural Gas Plan")]')
                webdriver.ActionChains(self.driver).move_to_element(el1).perform()
                webdriver.ActionChains(self.driver).move_to_element(el1).perform()
                time.sleep(3)
            webdriver.ActionChains(self.driver).click(el).perform()


        def select_electric_utility_confirmplanpage(self,payload):
            self.driver.find_element_by_xpath(self.clickElectricUtlity_dropdown_confirmplanpage ).click()
            self.electric_utility_confirmplanpage_loc = '//div[@class="electric-utility-selector"]//div//a[contains(@href,"selected")][contains(text(),"'+payload.utility_name+'")]'
            el1 = self.driver.find_element_by_xpath(self.electric_utility_confirmplanpage_loc)
            webdriver.ActionChains(self.driver).move_to_element(el1).perform()
            self.other_ele_utility='//div//h2[contains(text(),"Did you know we offer Electric plans?")]'
            el = self.driver.find_element_by_xpath( self.other_ele_utility)
            webdriver.ActionChains(self.driver).move_to_element(el).perform()
            webdriver.ActionChains(self.driver).move_to_element(el).perform()
            time.sleep(5)
            el1 = self.driver.find_element_by_xpath(self.electric_utility_confirmplanpage_loc)
            webdriver.ActionChains(self.driver).click(el1).perform()


        def select_electric_plan_confirmplanpage(self,payload):
            self.select_electric_plan_loc = '//h3[contains(text(),"'+payload.electricPlanName+'")]//parent::div//a//button[text()="Select"]'
            print(self.select_electric_plan_loc)
            el1 = self.driver.find_element_by_xpath('//h3[contains(text(),"'+payload.electricPlanName+'")]')
            self.driver.execute_script("return arguments[0].scrollIntoView();", el1)
            el = self.driver.find_element_by_xpath(self.select_electric_plan_loc)
            webdriver.ActionChains(self.driver).click(el).perform()

        confirm_your_plan_label_loc = '//h1[contains(text(),"Confirm Your Plan ")]'
        def click_ConfirmYourPlanLabel(self):
            try:
               self.driver.find_element_by_xpath(self.confirm_your_plan_label_loc).click()
            except:
               pass
        def select_gas_plan_planspage_new2(self,payload):
            self.select_gasplan_planspage_loc = '//div[@class="plan-wrapper"]//h3[contains(text(),"'+payload.gasPlanName+'")]//parent::div//parent::div//div//a//button[contains(text(),"Select")]'
            el1 = self.driver.find_element_by_xpath('//h3[contains(text(),"' + payload.gasPlanName + '")]')

            self.driver.execute_script("return arguments[0].scrollIntoView();", el1)
            el = self.driver.find_element_by_xpath(self.select_gasplan_planspage_loc)
            webdriver.ActionChains(self.driver).click(el).perform()

        def Click_Shops_FromMenu(self,payload):
            self.driver.find_element_by_xpath(self.menuLink_loc ).click()

        def Click_Plans_FromMenu(self,payload):
            self.planType_loc = '//div[@id="menu"]//li//a[contains(text(),"'+payload.planType+'")]'
            self.driver.find_element_by_xpath(self.planType_loc).click()


        def enterZipcode_submit_ForPlans(self,payload):
            self.driver.find_element_by_xpath(self.zipcodeForPlans_loc).click()
            self.driver.find_element_by_xpath(self.zipcodeForPlans_loc).send_keys(payload.zipcode)
            self.driver.find_element(By.XPATH, self.shopplans_pricingloc).click()


        def select_state_fromDD(self,payload):
            self.select_stateDD_loc = '//div[@id="plan-state-header"]//div[contains(@class,"state-select-widget")]/div/a[contains(text(),"'+payload.StateForDD+'")]'
            el = self.driver.find_element_by_xpath(self.click_stateDD_loc)
            self.driver.execute_script("return arguments[0].scrollIntoView();", el)
            webdriver.ActionChains(self.driver).click(el).perform()


        def fill_personalinformation(self, payload):

            time.sleep(10)
            self.enter_firstname(payload.first_name)
            time.sleep(3)
            self.enter_lastname(payload.last_name)
            time.sleep(2)
            self.enter_email(payload.email_addr)
            time.sleep(2)
            self.enter_verifyemail(payload.confirm_email_addr)
            time.sleep(2)
            self.enter_phonenumber(payload.Service_phone_number)
            self.enter_streetaddress(payload.Service_Address1)
            self.enter_city(payload.city)
            # self.click_useasitis()
            time.sleep(2)
            self.driver.find_element_by_id(self.zipcode_loc).click()
            time.sleep(3)
            self.click_useasitis()
            self.driver.find_element_by_id(self.zipcode_loc).click()
            self.driver.find_element_by_id(self.zipcode_loc).send_keys(str(payload.zipcode))
            self.enter_agreementdetails(payload.accountNo)
            self.enter_member_firstname(payload.first_name)
            self.enter_member_lastname(payload.last_name)
            self.enter_member_number(payload.member_number)

            try:
                 time.sleep(3)
                 account_details_loc = self.driver.find_element_by_xpath("//div//div//*[contains(text(),'Account Details')]")
                 time.sleep(4)
                 self.driver.execute_script("return arguments[0].scrollIntoView();", account_details_loc)
                 time.sleep(2)
            except:
                 pass

            try:
                 time.sleep(3)
                 United_MileagePlusMiles_loc = self.driver.find_element_by_xpath("//div//div//*[contains(text(),'United MileagePlus Miles')]")
                 time.sleep(4)
                 self.driver.execute_script("return arguments[0].scrollIntoView();", United_MileagePlusMiles_loc)
                 time.sleep(2)
            except:
                pass

            self.click_continue()
            time.sleep(5)


        def select_preferences_and_save(self):
            time.sleep(1)
            service_add_loc=self.driver.find_element_by_xpath("//div//div//*[contains(text(),'Same as Service Address')]")
            time.sleep(4)
            self.driver.execute_script("return arguments[0].scrollIntoView();", service_add_loc)
            self.phone_marketing_preferences()
            self.email_marketing_preferences()
            self.marketing_data_preferences()
            self.save_preferences()
            time.sleep(10)


