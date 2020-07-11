import csv

# from BasePage import BasePage
import logging
# import ConfigFiles.logger as cl
import os
import time
import datetime

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
# from generators.accountNO_generator import account_generator_accountNo
# from generators.names_and_address_generator import name_phone_address_generator
# from generators.zip_city_generator import generator_zip_city
# from GME.GME_regression.GME_WebEnroll_settings import email_given, tester, test_name, url_1, make_report
from datetime import datetime

# from Regression.sprint_regression.GME_regression_new.GME_WebEnroll_settings import tester, test_name,  make_report, url_1, env
from Regression.PageFactory.BasePage import BasePage
from Regression.generators.accountNO_generator import account_generator_accountNo
from Regression.generators.names_and_address_generator import name_phone_address_generator
# from Regression.generators.zip_city_generator import *


test_name = "test_GME_WebEnroll"
chosen_driver = "chrome"  #choose "firefox" or "chrome"
env = 'pt'
url_1 = "http://gme.enroll."+env+".nrgpl.us/?product_id="
API_link = "http://nerf.api."+env+".nrgpl.us/api/v1/orders/?enrollment_number="
workbook_name = "./inbox_data_files/TestData.xlsx"
data_sheet_name = 'GME_regression' # FOR REGRESSION
make_report = "1" # If you need to feel full report - enter "1", if no - enter "0"
sap_list=[]





class GmeEnroll(BasePage):
        def __init__(self, driver):
            super().__init__(driver)
            self.driver = driver


        # log = cl.genericLogger(logging.DEBUG)

        # locators
        zipcode_mainpage_loc="zip-code"
        view_plans_loc= 'zip-search'
        firstName_loc="id_first_name"
        lastName_loc="id_last_name"
        email_loc="id_email"
        verifyEmail_loc="id_ver_email"
        phoneNum_loc="id_phone"
        streetAdd_loc="id_service_address_1"
        city_loc="id_service_address_city"
        zipcode_loc="id_service_address_zip"
        agreementId_loc="id_electric-uan"
        continueBtn="//*[@class='button green continue']"
        acctNo_loc="id_electric-billing_uan"
        verification_chkbox_loc= 'id_order_authorization' #id
        tos_verification_page_loc= 'tos-section' #class
        submit_ver_page_loc= "//*[@class='button  continue']"

        authLabel_loc = "//*[contains(text(),'Authorization')]"
        termsCond1_loc = "id_order_authorization"

        # termsCond2_loc = "id_affiliate_consent"
        tosSection_loc = "tos-section"
        afferm_loc = "id_crs_order_authorization"
        ptc_loc = "id_ptc_consent"
        LowIncome_loc = "id_li_consent"

        def clickAuthInfoLabel(self):
            self.elementClick(self.authLabel_loc, locatorType="XPATH")
        def clickTermsCond1(self):
            self.elementClick(self.termsCond1_loc)
        def click_afferm_ACR(self):
            self.elementClick(self.afferm_loc)
        def click_afferm_PTC(self):
            self.elementClick(self.ptc_loc)
        def click_afferm_LowIncome(self):
            self.elementClick(self.LowIncome_loc)

        def enter_account_number(self, acctNo):
            self.sendKeys(str(acctNo),self.acctNo_loc)
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
            self.driver.find_element_by_xpath(self.continueBtn).click()
        def clickSubmitBtn(self):
            self.elementClick(self.submit_ver_page_loc, locatorType="XPATH")

        def fill_personalinformation(self,  payload, firstname, lastname, address, zipcode_, city, accountNo, email, account_number, phonenumber ):

            try:
                self.dismiss_alert()
            except:
                pass
            time.sleep(4)
            a=zipcode_
            try:
                generated_zipCode_ = zipcode_.replace("'", '')
            except:
                generated_zipCode_=zipcode_

            generated_zipCode = int(float(generated_zipCode_))

            if len (str(generated_zipCode))==4:
                generated_zipCode = str("0")+str(generated_zipCode)

            self.enter_firstname(firstname)
            self.enter_lastname(lastname)
            self.enter_email(email)
            self.enter_verifyemail(email)
            self.enter_phonenumber(phonenumber)
            self.enter_streetaddress(address)
            self.enter_city(city)
            self.driver.find_element_by_id(self.zipcode_loc).send_keys(int(generated_zipCode))

           #close allert
            try:
                self.dismiss_alert()
            except:
                pass

            #verify - the name fields is full
            self.check_fields_are_filled( firstname, lastname, address, generated_zipCode, city, accountNo, email, account_number, phonenumber)

            #check full name of utility
            utility = self.driver.find_element_by_xpath("//div[@class='cell cell-account-number']/span[2]").text

            self.enter_agreementdetails(accountNo)

            try:
                 account_details_loc = self.driver.find_element_by_xpath("//div//div//*[contains(text(),'Account Details')]")
                 self.driver.execute_script("return arguments[0].scrollIntoView();", account_details_loc)
            except:

                 pass

            try:
                self.dismiss_alert()
            except:
                pass

            try:
                 # time.sleep(3)
                 United_MileagePlusMiles_loc = self.driver.find_element_by_xpath("//div//div//*[contains(text(),'United MileagePlus Miles')]")
                 # time.sleep(4)
                 self.driver.execute_script("return arguments[0].scrollIntoView();", United_MileagePlusMiles_loc)
                 # time.sleep(2)
            except:
                pass

            self.click_continue()
            WebDriverWait(self.driver, 70).until(expected_conditions.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'About You')]")))

        def check_fields_are_filled(self, firstname, lastname, address, generated_zipCode, city, accountNo, email, account_number, phonenumber):
            try:
                assert self.driver.find_element_by_id(self.firstName_loc).get_attribute('value') == firstname
            except:
                self.enter_firstname(firstname)
            try:
                assert self.driver.find_element_by_id(self.lastName_loc).get_attribute('value') == lastname
            except:
                self.enter_lastname(lastname)
            try:
                assert self.driver.find_element_by_id(self.email_loc).get_attribute('value') == email
            except:
                self.enter_email(email)
            try:
                assert self.driver.find_element_by_id(self.verifyEmail_loc).get_attribute('value') == email
            except:
                self.enter_verifyemail(email)
            try:
                assert self.driver.find_element_by_id(self.phoneNum_loc).get_attribute('value') == phonenumber
            except:
                self.enter_phonenumber(phonenumber)
            try:
                assert self.driver.find_element_by_id(self.streetAdd_loc).get_attribute('value') == address
            except:
                self.enter_streetaddress(address)
            try:
                assert self.driver.find_element_by_id(self.city_loc).get_attribute('value') == city
            except:
                self.enter_city(city)
            try:
                assert self.driver.find_element_by_id(self.zipcode_loc).get_attribute('value') == generated_zipCode
            except:
                self.driver.find_element_by_id(self.zipcode_loc).send_keys(str(generated_zipCode))

        def dismiss_alert(self):
            self.driver.switch_to.alert
            try:
                self.driver.find_element_by_id("mcx_decline").click()
                time.sleep(1)
            except:
                pass

        def getemailaddress(self,payload):
            self.enter_email(payload.email_addr)


        def gme_scroll_termsandconditions_and_agree(self, payload):
            self.driver.execute_script("window.scrollTo(0,300);")
            end_tos = self.driver.find_element_by_id('greentxt2')
            self.driver.execute_script("return arguments[0].scrollIntoView();", end_tos)
            print('scrolled')
            self.driver.implicitly_wait(5)
            self.clickTermsCond1()  # id_order_authorization
            # self.clickTermsCond2()  # id_affiliate_consent
            self.driver.implicitly_wait(5)
            if payload.StateSlug.upper() == "IL":
                self.click_afferm_ACR()
                time.sleep(1)
                self.click_afferm_PTC()
                time.sleep(1)
                self.click_afferm_LowIncome()
            else:
                pass
            self.clickSubmitBtn()

        def get_confirmation_number(self, payload,firstname, lastname, address, zipcode_, city, accountNo, email, account_number, phonenumber ):
            WebDriverWait(self.driver, 50).until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@class='processing']/strong")))
            time.sleep(1)
            conf_text = self.driver.find_element_by_xpath("//*[@class='processing']/strong").text

            query_text = 'http://nerf.api.' + env + '.nrgpl.us/api/v1/orders/?enrollment_number=' + str(conf_text)
            response = requests.get(query_text)
            data = response.json()
            order_status = data[0]['order_status']
            while order_status == 'backend_processing':
                    for i in range (1,5):
                        query_text = 'http://nerf.api.' + env + '.nrgpl.us/api/v1/orders/?enrollment_number=' + str(conf_text)
                        response = requests.get(query_text)
                        data = response.json()
                        order_status = data[0]['order_status']
            else:
                pass
            sap_request = data[0]['order_items'][0]['href']
            response_sap = requests.get(sap_request)
            data_sap = response_sap.json()
            sap_enrollment_confirmation = data_sap['sap_enrollment_confirmation']
            sap_conf_ = str("'" + str(sap_enrollment_confirmation))



            self.make_report_for_test_GME_WebEnroll(conf_text, order_status, sap_conf_, payload, firstname, lastname, address, zipcode_, city, accountNo, email, account_number, phonenumber)

            time.sleep(2)


        def make_report_for_test_GME_WebEnroll(self,  conf_text, order_status, sap_conf_, payload, firstname, lastname, address, zipcode_, city, accountNo, email, account_number, phonenumber):
            if make_report == "1":

                now = datetime.now()
                date = now.strftime("%m_%d_%Y")
                csv_filename = ("./outbox_data_files/" + test_name +"_"+ str(date) + "_tests_results.csv")

                data_report_list = [payload.ts,	payload.sku,	payload.StateSlug.upper(),	payload.UtilitySlug,
                                    firstname,	lastname,	address,	zipcode_,	city,	email,	accountNo,
                                    payload.comments, date, conf_text, order_status, sap_conf_, "Passed"]


                if os.path.isfile(csv_filename):
                    f = open(csv_filename, 'a', newline='')
                    csv_a = csv.writer(f)
                    csv_a.writerow(data_report_list)
                else:
                    f = open(csv_filename, 'a', newline='')
                    csv_a = csv.writer(f)
                    csv_a.writerow(
                        ['ts', 'sku', 'StateSlug', 'UtilitySlug', 'first_name', 'last_name', 'ServiceAddress1', 'zip_code',
                         'city', 'email', 'account_no', 'comments', 'date','conf_number','order_status', 'sap_enrollment_conf_', "test_status"])
                    csv_a.writerow(data_report_list)







        def gme_enroll_enter_zipcode_continue(self):
            self.zipCode_text= self.driver.find_element_by_id(GmeEnroll.zipcode_loc)
            self.zipCode_text.click()
            self.zipCode_text.send_keys("19018")
            self.view_plan_button= self.driver.find_element_by_class_name(GmeEnroll.view_plans_loc)
            self.view_plan_button.click()
            time.sleep(3)

        def get_plan_name_continue(self):
            self.plan_name= self.driver.find_element_by_xpath("//h5[contains(text(),'Pollution Free')]")
            print(self.plan_name.text)
            assert "Pollution FreeTM Farm to Market Reliable Rate" == self.plan_name.text
            self.sign_up_now= self.driver.find_element_by_link_text("Sign Up Now")
            self.sign_up_now.click()
            time.sleep(8)
