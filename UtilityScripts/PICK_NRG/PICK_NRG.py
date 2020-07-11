from __future__ import print_function
import csv
import time
from datetime import datetime
from selenium import webdriver
import xlrd
import os
from collections import namedtuple

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Regression.NRG.ConfirmationPage import ConfirmationPage
from Regression.PageFactory.VerificationPage import VerificationPage
import pytest
from selenium.webdriver.support import expected_conditions as EC
from UtilityScripts.PICK_NRG.NrgEnroll import NrgEnroll

env = 'qa'
# env = 'gme-plus'
test_name = 'PICK_NRG'
local_path = "./inbox_files/database.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('Sheet1')

electric_enrollment = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

start_test=1

for current_row in range(start_test, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    electric_enrollment.append(Payload(**value_dict))

@pytest.fixture(scope='module')
def test_setup(request):
    global driver
    driver = webdriver.Firefox()
    def resource_a_teardown():
        driver.quit()
    request.addfinalizer(resource_a_teardown)



@pytest.mark.parametrize("payload", electric_enrollment, ids=[p.ts for p in electric_enrollment])

def test_state(test_setup, payload):

     try:
        _state_test_internals(driver, payload)
     except Exception as ae:
        import uuid
        filename = "./failed/test_email_fail_{}_{}.png".format(payload.ts,uuid.uuid4())
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.ts)
        print("filename:", filename)
        print(str(ae))
        now = datetime.now()
        time_for_csv_report = now.strftime("_%m_%d_%Y_%I_%M_%S_%p")
        date = now.strftime("_%m_%d_%Y_")
        # csv_filename = (
        #         "./outbox_folder/" + str(date) + "_FAILED_tests_results.csv")
        # f = open(csv_filename, 'a', newline='')
        # csv_a = csv.writer(f)
        # csv_a.writerow(
        #     [payload.ts,	payload.PremiseType,	payload.sku,	payload.BrandSlug,	payload.ChannelSlug,
        #      payload.ProductName,	payload.TermsOfServiceTyp,	payload.account_no,	payload.first_name,	payload.last_name,
        #      payload.UtilitySlug,	payload.Commodity,	payload.ServiceAddress1,	payload.ServiceAddress2,	payload.city,
        #      payload.StateSlug,	payload.zip_code,	payload.email,	payload.emailmarketing,
        #      str(time_for_csv_report),
        #      "Passed"])

        raise ae
     except: pass



def _state_test_internals(driver, payload):
        url = payload.URL
        print( " getting url: " +url )


        driver.get(url)
        # driver.maximize_window( )
        # driver.implicitly_wait(3)

        ## Personal Information
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='zip']")))


        driver.find_element_by_xpath("//input[@id='zip']").send_keys(int(payload.Zip_Code))
        driver.find_element_by_xpath("//span[contains(text(),'Get started') ][1]").click()
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "showTitle")))
        driver.switch_to_alert()
        electric_utilitites_list = []
        try:
            elem = driver.find_element_by_xpath("//div[@id= 'showelectric']")
            for span in elem.find_elements_by_class_name("util"):
                electric_utilitity = span.text
                electric_utilitites_list.append(electric_utilitity)
                print(electric_utilitity)

        except:
            pass

        gas_utilitites_list = []
        try:
            elem = driver.find_element_by_xpath("//div[@id= 'showgas']")
            for span in elem.find_elements_by_class_name("util"):
                gas_utilitity = span.text
                gas_utilitites_list.append(gas_utilitity)
                print(gas_utilitity)
        except:
            pass

        # time.sleep(1)
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "goToProductChart")))
        driver.find_element_by_id('goToProductChart').click()
        # time.sleep(2)
        #if added:
        # WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "electButtonSelect")))
        # driver.find_elements_by_id('electButtonSelect').click()
        # time.sleep(2)
        WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.ID, "electButtonSignUpButton")))
        driver.find_element_by_id('electButtonSignUpButton').click()
        time.sleep(2)
        # alert = driver.switch_to.alert
        # print('switched')
        # NrgEn= NrgEnroll(driver)
        # NrgEn.fill_personalinformation(payload)
        #
        # # Verification
        # vp = VerificationPage(driver)
        # vp.scroll_termsandconditions_and_agree()
        # # time.sleep(2)
        #
        # ## Grab Confirmation Code
        # cop = ConfirmationPage(driver)
        # cop.get_confirmation_number(env, payload)
        # # confirmationNum = cop.get_confirmation_number(payload)
        # print("Confirmation number generated")
        # # time.sleep(2)
        #
        # # ##Selecting all Preferences
        # # print("Selecting Preferences")
        # # NrgEn.select_preferences_and_save()
