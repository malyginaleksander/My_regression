from __future__ import print_function
import csv
import random
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

from Regression.helpers.NRG.ConfirmationPage import  get_confirmation_number_PICK_NRG
from Regression.helpers.NRG.NrgEnroll import fill_personalinformation_pickNRG
from Regression.helpers.NRG.VerificationPage import scroll_termsandconditions_and_agree
from Regression.helpers.common.accountNO_generator import account_generator_accountNo

test_list = []# test_list = [4,11,16]
start_test=1
env = 'prod'
test_name = 'PICK_NRG_el_and_gas'
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
report = "./database_.csv"
sap_list= []
completed_list=[]
error_list = []
backend_list = []
epnet_file_sent_list = []

scenarios = []
headers = [ 'StateSlug', 'Vanity', 'LandingPageURL', 'ZipCode', 'ElectricUtility', 'GasUtility']

list_ts = []

ts_=0
headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

if len(test_list) > 0:
    for current_row in test_list:
        values = [cell.value for cell in worksheet.row(current_row)]
        value_dict = dict(zip(headers, values))
        list_ts.append(Payload(**value_dict))
else:
    for current_row in range(start_test, worksheet.nrows):
        values = [cell.value for cell in worksheet.row(current_row)]
        value_dict = dict(zip(headers, values))
        list_ts.append(Payload(**value_dict))

@pytest.fixture(scope='module')
def test_setup(request):
    global driver
    driver = webdriver.Firefox()
    driver.implicitly_wait(2)

    def resource_a_teardown():
        driver.quit()
    request.addfinalizer(resource_a_teardown)
    return driver

# def test_number(ts_):
#     ts_ += 1
#     return ts_
@pytest.mark.parametrize("payload", list_ts,  ids=[p.ts for p in list_ts])

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
                            payload.ElectricUtility, time_for_csv_report])

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
            # WebDriverWait(driver, 3).until(EC.alert_is_present())
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH,  '//h4[contains(text(), "Multiple utilities service your zip code.")]')))
            time.sleep(1)
            electric_enrollment = []
            gas_enrollment = []
            try:
                elem = driver.find_element_by_xpath("//div[@id= 'showelectric']")
                for span in elem.find_elements_by_class_name("util"):
                    electric_utilitity = span.text
                    electric_enrollment.append(electric_utilitity)

            except:
                pass

            try:
                elem = driver.find_element_by_xpath("//div[@id= 'showgas']")
                for span in elem.find_elements_by_class_name("util"):
                    gas_utilitity = span.text
                    gas_enrollment.append(gas_utilitity)
            except:
                pass

            print(payload.ts, "Electric", electric_enrollment)
            print(payload.ts, "Gas", gas_enrollment)

            merged_list = []
            for i in range(max((len(electric_enrollment), (len(gas_enrollment))))):

                while True:
                    try:
                        tup = (electric_enrollment[i], gas_enrollment[i])
                    except IndexError:
                        if len(electric_enrollment) > len(gas_enrollment):
                            gas_enrollment.append('')
                            tup = (electric_enrollment[i], gas_enrollment[i])
                        elif len(electric_enrollment) < len(gas_enrollment):
                            electric_enrollment.append(random.choice(electric_enrollment))
                            tup = (electric_enrollment[i], gas_enrollment[i])
                        continue

                    merged_list.append(tup)
                    break

            for i in merged_list:
                if os.path.isfile(report):
                    f = open(report, 'a', newline='')
                    csv_a = csv.writer(f)
                    csv_a.writerow([ payload.StateSlug, payload.Vanity, payload.LandingPageURL, zip,i[0], i[1] ])
                else:
                    f = open(report, 'a', newline='')
                    csv_a = csv.writer(f)
                    csv_a.writerow(headers)
                    csv_a.writerow(
                        [ payload.StateSlug, payload.Vanity, payload.LandingPageURL, zip, i[0], i[1]])

                    f.close()



        except:
            j = driver.find_element_by_xpath("//span[@class='plan-name']").text
            if os.path.isfile(report):
                f = open(report, 'a', newline='')
                csv_a = csv.writer(f)
                csv_a.writerow([ payload.StateSlug, payload.Vanity, payload.LandingPageURL, zip, j])
            else:
                f = open(report, 'a', newline='')
                csv_a = csv.writer(f)
                csv_a.writerow(headers)
                csv_a.writerow(
                    [ payload.StateSlug, payload.Vanity, payload.LandingPageURL, zip, j])


                f.close()
