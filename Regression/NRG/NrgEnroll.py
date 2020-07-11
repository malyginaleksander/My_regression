from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time




def fill_personalinformation(driver, payload, firstname, lastname, address, zipcode_, city, accountNo, email,
                             account_number, phonenumber):
    try:
        driver.switch_to_alert()
        driver.find_element_by_class_name('close').click()
    except:
        pass
    time.sleep(1)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'id_first_name')))
    driver.find_element_by_id('id_first_name').click()
    driver.find_element_by_id('id_first_name').send_keys(firstname)
    driver.find_element_by_id('id_last_name').send_keys(lastname)
    driver.find_element_by_id('id_email').send_keys(email)
    driver.find_element_by_id('id_ver_email').send_keys(email)
    driver.find_element_by_id('id_phone').send_keys(str(phonenumber))
    driver.find_element_by_id('id_service_address_zip').click()
    driver.find_element_by_id('id_service_address_city').send_keys(str(city))
    driver.find_element_by_id('id_service_address_zip').send_keys(str(zipcode_))
    driver.find_element_by_id('id_electric-uan').send_keys(account_number)
    driver.find_element_by_id('id_service_address_1').send_keys(str(address), Keys.ENTER)
    try:
        time.sleep(1)
        driver.find_element_by_xpath("//a[text()='Use as it is']").click().send_keys(Keys.ENTER)
    except:
        pass

    if payload.StateSlug == "PA":
        try:
            driver.find_element_by_id('id_electric-billing_uan').send_keys(account_number)
        except:
            pass

    try:
        driver.find_element_by_id('id_partner_member_number').send_keys(account_number)
    except:
        pass
    try:
        driver.find_element_by_id('continue-submit').click()
    except:
        pass



#
# def fill_personalinformation_with_SWAP(self, payload):
#
#     try:
#         self.driver.switch_to_alert()
#         self.driver.find_element_by_class_name('btn-large-magenta').click()
#     except:
#         pass
#     utility = payload.utility
#     address_house_street_generated, first_name_generated, last_name_generated, email_generated, \
#     phone_area_code_generated, phone_last_generated, phone_prefix_generated, email_generated, \
#     phone_number_generated, address_house_street_generated, member_number= names_and_address_generator()
#     city, generated_zipCode = generator_zip_city(payload)
#     accountNo = account_generator_accountNo(utility)
#     WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'id_first_name')))
#     # time.sleep(5)
#
#     self.enter_firstname(payload.first_name)
#     self.enter_lastname(payload.last_name)
#     self.enter_email(payload.email)
#     self.enter_verifyemail(payload.email)
#     self.enter_phonenumber(str(phone_number_generated))
#     self.enter_streetaddress(payload.ServiceAddress1)
#     self.driver.find_element_by_id('id_service_address_2').send_keys(payload.ServiceAddress2)
#     self.enter_city(payload.city)
#     self.enter_state(payload.StateSlug)
#     time.sleep(1)
#     try:
#         self.click_useasitis()
#         self.driver.find_element_by_id('id_service_address_1').send_keys(Keys.ENTER)
#     except:
#         pass
#     # time.sleep(2)
#     try:
#         self.click_useasitis()
#     except:
#         pass
#     self.driver.find_element_by_id(self.zipcode_loc).click()
#     self.driver.find_element_by_id(self.zipcode_loc).send_keys(str(payload.zip_code))
#     self.enter_agreementdetails(payload.UAN)
#     try:
#         self.enter_member_firstname(payload.first_name)
#         self.enter_member_lastname(payload.last_name)
#         member = int(random.randint (89000,89999))
#         self.enter_member_number(member)
#     except:
#         pass
#     try:
#          # time.sleep(3)
#          account_details_loc = self.driver.find_element_by_xpath("//div//div//*[contains(text(),'Account Details')]")
#          # time.sleep(4)
#          self.driver.execute_script("return arguments[0].scrollIntoView();", account_details_loc)
#          # time.sleep(2)
#     except:
#          pass
#
#     try:
#          # time.sleep(3)
#          United_MileagePlusMiles_loc = self.driver.find_element_by_xpath("//div//div//*[contains(text(),'United MileagePlus Miles')]")
#          # time.sleep(4)
#          self.driver.execute_script("return arguments[0].scrollIntoView();", United_MileagePlusMiles_loc)
#          # time.sleep(2)
#     except:
#         pass
#
#     try:
#         self.driver.find_element_by_id('id_electric-billing_uan').send_keys(payload.account_no)
#     except:pass
#
#     self.click_continue()
#     # time.sleep(10)
#
