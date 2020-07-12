from __future__ import print_function
from datetime import datetime
import csv
from selenium import webdriver
import time
import xlrd
from collections import namedtuple
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import  expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from Regression.helpers.common.create_data_for_test import create_data_for_test
from Regression.helpers.GME.GmeEnroll import GmeEnroll



test_list=[1]
start_test = 1

test_name = "test_GME_WebEnroll"
chosen_driver = "chrome"  #choose "firefox" or "chrome"
env = 'pt'
url_1 = "http://gme.enroll."+env+".nrgpl.us/?product_id="
API_link = "http://nerf.api."+env+".nrgpl.us/api/v1/orders/?enrollment_number="
workbook_name = "./inbox_data_files/TestData.xlsx"
# workbook_name = "././GME_regression_new/inbox_data_files/TestData.xlsx"
data_sheet_name = 'GME_regression' # FOR REGRESSION
make_report = "1" # If you need to feel full report - enter "1", if no - enter "0"
sap_list=[]
completed_list =[]
error_list = []
backend_list = []
epnet_file_sent_list=[]
test_count = 0
local_path = workbook_name
workbook = xlrd.open_workbook(local_path)
worksheet = workbook.sheet_by_name(data_sheet_name)
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
def driver(request):
    _driver = webdriver.Firefox()


    def resource_a_teardown():
        if len(sap_list)>0:
            min_sap =min(sap_list)
            max_sap = max(sap_list)


            print('_'*50)
            print('Completed: ', len(completed_list))
            print('Backand_processing: ', len(backend_list))
            print('Errors: ', len(error_list))
            print('Epnet_file_sent_list: ', len(epnet_file_sent_list))

            print('_'*50)
            print('SAP numbers: ', len(sap_list))
            print('min_sap: ', min_sap)
            print('max_sap: ', max_sap)
        if _driver:
            _driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver



@pytest.mark.parametrize("payload", electric_enrollment, ids=[p.ts for p in electric_enrollment])


def test_state(driver, payload):
    global test_count, errors_count
    try:
        _state_test_internals(driver, payload, test_name, env)
    except Exception as ae:
        now = datetime.now()
        current_time = now.strftime("_%m_%d_%Y_%I_%M_%S_%p_")
        filename = "./outbox_data_files/failed/"+ test_name+"_{}_"+ current_time+ ".png".format(payload.ts)
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.ts)
        print("filename:", filename)
        f = open(filename, 'a', newline='')
        csv_a = csv.writer(f)
        print(str(ae))
        csv_a.writerow(
            ["FAILED", time, payload.ts, payload.sku, str(url_1 + str(payload.sku)), payload.StateSlug, payload.UtilitySlug ])
        raise ae




def _state_test_internals(driver, payload, test_name, env):

        full_url = str(url_1 + str(payload.sku))
        driver.get( full_url)
        print( " getting url: %s" %  full_url, payload.UtilitySlug )

        driver.implicitly_wait(3)

        WebDriverWait(driver, 20).until(expected_conditions.visibility_of_element_located((By.ID, 'id_first_name')))
        firstname, lastname, address, zipcode_, city, accountNo, email, account_number, phonenumber = create_data_for_test(
            payload)
        ## Personal Information

        GMEEn= GmeEnroll(driver)
        GMEEn.fill_personalinformation(payload, firstname, lastname, address, zipcode_, city, accountNo, email, account_number, phonenumber )

        # Verification
        GMEEn.gme_scroll_termsandconditions_and_agree(payload)

        # Grab Confirmation Code
        GMEEn.get_confirmation_number(payload, env, firstname, lastname, address, zipcode_, city, accountNo, email, account_number, phonenumber, sap_list, test_name, completed_list, error_list, backend_list, epnet_file_sent_list)

