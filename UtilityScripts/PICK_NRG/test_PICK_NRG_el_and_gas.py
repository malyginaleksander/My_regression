from __future__ import print_function
import csv
import time
from datetime import datetime
from selenium import webdriver
import xlrd
from collections import namedtuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pytest
from selenium.webdriver.support import expected_conditions as EC
from Regression.helpers.NRG.ConfirmationPage import  get_confirmation_number_PICK_NRG
from Regression.helpers.NRG.NrgEnroll import fill_personalinformation_pickNRG
from Regression.helpers.NRG.VerificationPage import scroll_termsandconditions_and_agree
from Regression.helpers.common.accountNO_generator import account_generator_accountNo

test_list = []# test_list = [4,11,16]
start_test=51
env = 'prod'
test_name = 'PICK_NRG_el_and_gas'
workbook = xlrd.open_workbook("./inbox_files/database.xlsx")
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
    driver.implicitly_wait(4)
    def resource_a_teardown():
        driver.quit()
    request.addfinalizer(resource_a_teardown)
    return driver


@pytest.mark.parametrize("payload", electric_enrollment, ids=[p.ts for p in electric_enrollment])

def test_state(test_setup, payload):

    try:
        _state_test_internals(driver, payload)
    except:
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
                                payload.ElectricUtility, time_for_csv_report])

            raise ae



def _state_test_internals(driver, payload):
        url = ''
        url = payload.LandingPageURL
        print( " getting url: " +url )


        driver.get(url)


        ## Personal Information
        #todo
        try:
            zip = str(payload.ZipCode.replace("'", ''))
        except:
            zip = str(payload.ZipCode)
        if len(zip) < 5:
            zip = str("0" + str(zip))


        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='zip']")))

        driver.find_element_by_xpath("//input[@id='zip']").send_keys(zip)
        driver.find_element_by_xpath("//span[contains(text(),'Get started') ][1]").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "showTitle")))
        time.sleep(2)
        driver.switch_to_alert()
        time.sleep(2)
        try:
            elem = driver.find_element_by_xpath("//div[@id= 'showelectric']")
            for span in elem.find_elements_by_class_name("util"):
                electric_utilitity = span.text
                if electric_utilitity[:3].upper() == payload.ElectricUtility[:3].upper():
                    span.click()

        except:
            pass

        try:
            elem = driver.find_element_by_xpath("//div[@id= 'showgas']")
            for span in elem.find_elements_by_class_name("util"):
                gas_utilitity = span.text
                if gas_utilitity[:3].upper() == payload.GasUtility[:3].upper():
                    span.click()
        except:
            pass

        time.sleep(1)
        #POPUP Continue

        try:
            WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, "goToProductChart")))
            driver.find_element_by_id('goToProductChart').click()
        except:
            pass

        # if payload.StateSlug.upper() == "MA":
        try:
            time.sleep(2)
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "electButtonSignUpButton")))
            driver.find_element_by_id('electButtonSignUpButton').click()
        except:
            pass
        else:
            pass


        # time.sleep(2)
        #"Select" button on electric page
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, "electButtonSelect")))
            time.sleep(3)
            driver.find_element_by_id('electButtonSelect').click()
        except:
            pass


        if len(str(payload.GasUtility))>0:
            time.sleep(2)
            driver.switch_to_alert()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Yes')]")))
            driver.find_element_by_xpath("//span[contains(text(), 'Yes')]").click()
            WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "gasButtonSelect")))
            time.sleep(1)
            driver.find_element_by_id('gasButtonSelect').click()
        else:
            try:
                driver.switch_to_alert()
                driver.find_element_by_id("closeModal").click()
            except:
                pass
        try:
            # WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "submitProductChartButton")))
            time.sleep(2)
            driver.find_element_by_id("submitProductChartButton").click()
        except:
            pass



        time.sleep(2)

        el_account_number = account_generator_accountNo(payload.ElectricUtility)
        el_accountNo = str("'" + str(el_account_number))

        if  len(str(payload.GasUtility))>0:
            gas_account_number = account_generator_accountNo(payload.GasUtility)
            gas_accountNo = str("'" + str(gas_account_number))
        else:
            gas_account_number = ''
            gas_accountNo=''


        fill_personalinformation_pickNRG(driver, payload, test_name, firstname, lastname, address, zipcode_, city, email, phonenumber,
                                         el_account_number, el_accountNo, gas_account_number, gas_accountNo)

        scroll_termsandconditions_and_agree(driver)

        ## Grab Confirmation Code

        get_confirmation_number_PICK_NRG(driver, payload, test_name )
        time.sleep(2)

