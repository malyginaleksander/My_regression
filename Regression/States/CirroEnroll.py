from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Regression.PageFactory.BasePage import BasePage
import Regression.ConfigFiles.logger as cl
import logging
import time
from selenium.webdriver.support import  expected_conditions as EC

class CirroEnroll(BasePage):
    log = cl.genericLogger(logging.DEBUG)

    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver

    def select_option(self, selectValue, elem):
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == selectValue:
                option.click()
                break
        time.sleep(1)

    # locators

    first_name = "id_first_name"
    middle_initial = "id_middle_initial"
    last_name = "id_last_name"
    email = "id_email"
    confirm_email = "id_ver_email"
    street_sddress1 = "id_service_address_1"
    apt_unit = "id_service_address_2"
    zipcode = "id_service_address_zip"
    phoneNum = "id_phone"
    city = "id_service_address_city"
    accountNo = "id_electric-uan"
    continue_button ="continue-submit"
    order_authorization_checkbox ="id_order_authorization"
    tos_section_class_name = "tos-section"
    submit_button = "agree"
    confirmation_number = "confirmation"

    def fill_personalinformation (self, first_name_generated, accountNo, payload):

        try:
            self.driver.implicitly_wait(2)
            elem = self.driver.find_element_by_id("id_business_name").send_keys("Business_name")
            print("Business account ")
        except NoSuchElementException:
            pass
        finally:
            self.driver.implicitly_wait(60)
            elem = self.driver.find_element_by_id(self.first_name).send_keys(first_name_generated)
            last_name = str(payload.ts)+ "_"+ payload.utility
            elem = self.driver.find_element_by_id(self.last_name).send_keys(last_name)
            elem = self.driver.find_element_by_id(self.email).send_keys(payload.email_addr)
            elem = self.driver.find_element_by_id(self.confirm_email).send_keys(payload.confirm_email_addr)
            elem = self.driver.find_element_by_id(self.phoneNum).send_keys(str(payload.Service_phone_number))
            elem = self.driver.find_element_by_id(self.street_sddress1).send_keys(payload.Service_Address1)
            elem = self.driver.find_element_by_id(self.city).send_keys(payload.city)
            # elem = self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            elem = self.driver.find_element_by_id(self.zipcode).send_keys(str(payload.zipcode))
            elem = self.driver.find_element_by_id(self.accountNo).send_keys(str(accountNo))
            elem = self.driver.find_element_by_id(self.zipcode).click()
            # elem = self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            elem =self.driver.find_element_by_id(self.continue_button).click()




    def get_confirmation_number(self):
        # time.sleep(2)
        WebDriverWait(self.driver, 200).until(EC.presence_of_all_elements_located((By.ID, self.confirmation_number)))
        ConfirmationNumber = self.driver.find_element_by_id(self.confirmation_number).text
        print('ConfirmationNumber is: ' + ConfirmationNumber)

    time.sleep(1)