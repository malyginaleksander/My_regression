from __future__ import print_function
import pytest
import csv
from datetime import datetime
from selenium import webdriver
import xlrd
import os
from collections import namedtuple
from Regression.helpers.NRG.NrgEnroll import fill_personalinformation_pickNRG, fill_personalinformation
from Regression.helpers.NRG.VerificationPage import scroll_termsandconditions_and_agree
from Regression.helpers.NRG.ConfirmationPage import get_confirmation_number
from Regression.helpers.common.create_data_for_test import create_data_for_test

test_list = [ 140]
start_test=1

env = 'pt'
# env = 'gme-plus'
# test_name = 'Regressin_NRG_WEB'
test_name = 'August_campaign'
local_path = "./inbox_files/Regression_test_scenarios.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
# worksheet = workbook.sheet_by_name('Regression')
worksheet = workbook.sheet_by_name('August')
electric_enrollment = []
headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)
failed_list = []
sap_list = []
completed_list =[]
error_list = []
backend_list = []
epnet_file_sent_list = []

global _state_test_internals
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
        driver.quit()

    request.addfinalizer(resource_a_teardown)
    return driver

@pytest.mark.parametrize("payload", electric_enrollment, ids=[p.ts for p in electric_enrollment])
def test_state(test_setup, payload):
    print(" ", payload.ts, 'NRG WEB Enrollment - State = ', payload.StateSlug, ' - utility = ',
          payload.UtilitySlug)

    try:
        driver.delete_all_cookies()
        _state_test_internals(driver, payload, test_name)
    except Exception as ae:
        now = datetime.now()
        time_date = now.strftime("_%m_%d_%Y_")
        number_test_ = payload.ts
        number_test = number_test_.replace('ts_', "")
        failed_list.append(number_test)
        filename = "./failed/" + test_name + "_{}{}.png".format(payload.ts, time_date)
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.ts)
        print("filename:", filename)
        print(str(ae))
        failed_report_filename = ("./outbox_folder/FAILED_" + test_name + "{}.csv".format(time_date))
        # if os.path.isfile(failed_report_filename):
        failed = open(failed_report_filename, 'a', newline='')
        csv_failed = csv.writer(failed)
        csv_failed.writerow(
            [payload.ts, payload.SKU, payload.ChannelSlug, payload.BrandSlug, payload.PremiseType,
             payload.TermsOfServiceType, payload.ProductName, payload.ProductSlug, payload.StateSlug,
             payload.Commodity, payload.UtilitySlug, payload.first_name, payload.last_name,
             payload.ServiceAddress1, payload.zip_code, payload.city, payload.account_no,
             payload.email, payload.emailmarketing, str(time_date), "FAILED"])
        # else:
        #     failed= open(failed_report_filename, 'a', newline='')
        #     csv_failed = csv.writer(failed)
        #     csv_failed.writerow(
        #         ['ts', 'SKU', 'ChannelSlug', 'BrandSlug', 'PremiseType',
        #          'TermsOfServiceTyp', 'ProductName', 'ProductSlug', 'StateSlug',
        #          'Commodity', 'UtilitySlug', 'first_name', 'last_name', 'ServiceAddress1',
        #          'zip_code', 'city', 'account_no',
        #          'email', 'emailmarketing', 'time_for_csv_report', 'ae', 'status',
        #          "test_status"])
        #     csv_failed.writerow(
        #         [payload.ts, payload.SKU, payload.ChannelSlug, payload.BrandSlug, payload.PremiseType,
        #          payload.TermsOfServiceType, payload.ProductName, payload.ProductSlug, payload.StateSlug,
        #          payload.Commodity, payload.UtilitySlug, payload.first_name, payload.last_name,
        #          payload.ServiceAddress1, payload.zip_code, payload.city, payload.account_no,
        #          payload.email, payload.emailmarketing, str(time_date),  "FAILED"])
        raise ae
    except:
        pass




def _state_test_internals(driver, payload, test_name):
    url = 'https://nrg.enroll.' + env + '.nrgpl.us?product_id=' + payload.SKU
    print("getting url: " + url)

    driver.get(url)
    driver.implicitly_wait(3)
    firstname, lastname, address, zipcode_, city, accountNo, email,  account_number, phonenumber = create_data_for_test(
        payload)

    ## Personal Information
    fill_personalinformation(driver, payload, firstname, lastname, address, zipcode_, city, accountNo, email, account_number,
                                     phonenumber)

    # Verification
    scroll_termsandconditions_and_agree(driver)

    ## Grab Confirmation Code
    get_confirmation_number(driver, env, payload, test_name, firstname, lastname, address, zipcode_, city, accountNo, email, account_number, sap_list, completed_list, error_list,backend_list, epnet_file_sent_list)





