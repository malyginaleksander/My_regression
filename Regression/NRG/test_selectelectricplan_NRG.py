from __future__ import print_function

import csv
from datetime import datetime

from selenium import webdriver
import time
import xlrd
import os
from collections import namedtuple
from webdriver_manager.chrome import ChromeDriverManager
# from Regression.States.NrgEnroll import NrgEnroll
from Regression.NRG.ConfirmationPage import ConfirmationPage
from Regression.NRG.NrgEnroll import  fill_personalinformation
# from Regression.PageFactory.ConfirmationPage import ConfirmationPage
from Regression.NRG.VerificationPage import scroll_termsandconditions_and_agree
from Regression.NRG.create_data_for_test import create_data_for_test
import pytest

test_list = []
start_test=1



env = 'pt'
# env = 'gme-plus'
test_name = 'July_campaign'
# local_path = "../NRG_regression/inbox_files/regression_web_data_file.xlsx"
local_path = "./inbox_files/Apple_web_data_file.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('Sheet1')

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
    # driver = webdriver.Chrome(ChromeDriverManager("2.36").install())
    driver = webdriver.Firefox()
    # driver = webdriver.Chrome(ChromeDriverManager("2.36").install())
    def resource_a_teardown():
        driver.quit()

    request.addfinalizer(resource_a_teardown)
    return driver



@pytest.mark.parametrize("payload", electric_enrollment, ids=[p.ts for p in electric_enrollment])

def test_state(test_setup, payload):
     print( " ", payload.ts, 'NRG WEB Enrollment - State = ', payload.StateSlug, ' - utility = ', payload.UtilitySlug)

     try:
        _state_test_internals(driver, payload)
     except Exception as ae:
        now = datetime.now()
        time_date = now.strftime("_%m_%d_%Y_")
        number_test = payload.ts.replace('ts_', "")
        filename = "./failed/" + test_name + "_{}{}.png".format(payload.ts, time_date)
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.ts)
        print("filename:", filename)
        print(str(ae))
        failed_report_filename = (
                    "./outbox_folder/FAILED_" + test_name + "_{}.csv".format( time_date))

        if os.path.isfile(failed_report_filename):
            f = open(failed_report_filename, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(
                [payload.ts, payload.SKU, payload.ChannelSlug, payload.BrandSlug, payload.PremiseType,
                 payload.TermsOfServiceType, payload.ProductName, payload.account_no,	payload.first_name,	payload.last_name,
             payload.UtilitySlug,	payload.Commodity,	payload.ServiceAddress1, payload.city,
             payload.StateSlug,	payload.zip_code,	payload.email,	payload.emailmarketing,
             str(time_date),
             "Passed"])
        else:
            f = open(failed_report_filename, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(
                ['ts', 'PremiseType', 'sku', 'BrandSlug', 'ChannelSlug', 'ProductName',
                 'TermsOfServiceTyp', 'account_no', 'first_name', 'last_name',
                 'UtilitySlug', 'PartnerCode' , 'PartnerCode', 'PromoCode',  'Commodity', 'ServiceAddress1', 'ServiceAddress2',
                 'city','StateSlug', 'zip_code', 'email', 'emailmarketing',
                 'sap_conf_','uan_number', 'time_for_csv_report', 'sap_enrollment_conf_','order_status',
                 "test_status"])
            csv_a.writerow(
                [])
        raise ae






def _state_test_internals(driver, payload):
        url = 'https://nrg.enroll.'+ env + '.nrgpl.us?product_id=' + payload.SKU
        # url = 'http://nrg.enroll..nrgpl.us/?product_id='+ payload.sku
        print( "getting url: " +url )
        print(url)


        driver.get(url)
        # driver.maximize_window( )
        driver.implicitly_wait(3)
        firstname, lastname, address, zipcode_, city, accountNo, email, account_number, phonenumber = create_data_for_test(
            payload)

        # NrgEn = NrgEnroll(driver)

        ## Personal Information
        print("Personal Information")

        print("title: ", driver.title)

        # log.info("Getting the blacklisted_email method from the NRGEnroll page")
        fill_personalinformation(driver, payload, firstname, lastname, address, zipcode_, city, accountNo, email,
                                 account_number, phonenumber)

        # Verification
        scroll_termsandconditions_and_agree(driver)

        # time.sleep(2)

        ## Grab Confirmation Code
        cop = ConfirmationPage(driver)
        cop.get_confirmation_number(env, payload, firstname, lastname, address, zipcode_, city, accountNo, email,
                             account_number, phonenumber)
