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
import pytest
from selenium.webdriver.support import expected_conditions as EC

from Regression.helpers.NRG.ConfirmationPage import get_confirmation_number
from Regression.helpers.NRG.NrgEnroll import fill_personalinformation_pickNRG
from Regression.helpers.NRG.VerificationPage import scroll_termsandconditions_and_agree
from Regression.helpers.common.accountNO_generator import account_generator_accountNo

test_list = []# test_list = [4,11,16]
start_test=1
env = 'prod'
test_name = 'PICK_NRG'
workbook = xlrd.open_workbook("./inbox_files/database_.xlsx")
worksheet = workbook.sheet_by_name('Sheet1')

firstname = 'test'
lastname = 'test'
address = 'test'
zipcode_  ='99999'
city = 'test'
email = 'test@nrg.com'
phonenumber = '9999999999'
RewardsNumber = '9999999999999999'

sap_list= []
completed_list=[]
error_list = []
backend_list = []
epnet_file_sent_list = []



electric_enrollment = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

if len(test_list) > 0:
    for current_row in test_list:
        values = [cell.value for cell in worksheet.row(current_row)]
        value_dict = dict(zip(headers, values))
        electric_enrollment.append(Payload(**value_dict))
else:
    for current_row in range(start_test, worksheet.nrows):
        values = [cell.value for cell in worksheet.row(current_row)]
        value_dict = dict(zip(headers, values))
        electric_enrollment.append(Payload(**value_dict))

@pytest.fixture(scope='module')
def test_setup(request):
    global driver
    driver = webdriver.Firefox()
    driver.implicitly_wait(2)
    def resource_a_teardown():
        driver.quit()
    request.addfinalizer(resource_a_teardown)
    return driver


@pytest.mark.parametrize("payload", electric_enrollment, ids=[p.ts for p in electric_enrollment])

def test_state(test_setup, payload):

     try:
        _state_test_internals(driver, payload)
     except Exception as ae:
        now = datetime.now()
        time_for_csv_report = now.strftime("_%m_%d_%Y_%I_%M_%S_%p")
        filename = "./failed/failed_{}_{}{}.png".format(test_name, payload.ts, time_for_csv_report)
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.ts)
        print("filename:", filename)
        print(str(ae))
        date = now.strftime("_%m_%d_%Y_")
        csv_filename = (
                "./outbox_folder/" + str(date) + "_FAILED_tests_results.csv")
        f = open(csv_filename, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow([payload.ts, payload.StateSlug, payload.Vanity, payload.LandingPageURL, payload.ZipCode,
                            payload.UtilitySlug, time_for_csv_report])

        raise ae
     except: pass



def _state_test_internals(driver, payload):
        url = payload.LandingPageURL
        print( " getting url: " +url )


        driver.get(url)


        ## Personal Information
        try:
            zip = str(payload.ZipCode("'", ''))
        except:
            zip = str(payload.ZipCode)
        if len(zip) < 5:
            zip = str("0" + str(zip))


        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='zip']")))

        driver.find_element_by_xpath("//input[@id='zip']").send_keys(zip)
        driver.find_element_by_xpath("//span[contains(text(),'Get started') ][1]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "showTitle")))
        time.sleep(1)
        driver.switch_to_alert()
        time.sleep(1)
        # WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id= 'showelectric']")))
        try:
            elem = driver.find_element_by_xpath("//div[@id= 'showelectric']")
            for span in elem.find_elements_by_class_name("util"):
                electric_utilitity = span.text
                if electric_utilitity[:3].upper() == payload.UtilitySlug[:3].upper():
                    span.click()


        except:
            pass

        # gas_utilitites_list = []
        # try:
        #     elem = driver.find_element_by_xpath("//div[@id= 'showgas']")
        #     for span in elem.find_elements_by_class_name("util"):
        #         gas_utilitity = span.text
        #         gas_utilitites_list.append(gas_utilitity)
        #         print(gas_utilitity)
        # except:
        #     pass

        # time.sleep(1)
        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "goToProductChart")))
            driver.find_element_by_id('goToProductChart').click()
        except:
            pass

        time.sleep(2)

        try:
            driver.find_element_by_id('electButtonSignUpButton').click()
        except:
            pass
        try:
            driver.find_element_by_id('electButtonSelect').click()
            time.sleep(1)
        except:
            pass
        try:
            driver.switch_to_alert()
            driver.find_element_by_id("closeModal").click()
        except:
            pass
        try:
            driver.find_element_by_id("submitProductChartButton").click()
        except:
            pass




        time.sleep(2)

        account_number = account_generator_accountNo(payload.UtilitySlug)
        accountNo = str("'" + str(account_generator_accountNo(payload.UtilitySlug)))



        fill_personalinformation_pickNRG(driver, payload, test_name, firstname, lastname, address, zipcode_, city, accountNo, email,
                                         account_number, phonenumber)

        scroll_termsandconditions_and_agree(driver)

        ## Grab Confirmation Code

        get_confirmation_number(driver,  env, payload, test_name, firstname, lastname, address, zipcode_, city, accountNo, email, account_number,
                            sap_list, completed_list, error_list,backend_list, epnet_file_sent_list)

