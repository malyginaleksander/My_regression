from __future__ import print_function
import csv
from datetime import datetime

from faker import Faker
from selenium import webdriver
import xlrd
import os
from collections import namedtuple
import pytest

from Regression.GME.GME_Migration.helpers.accountNO_generator import account_generator_accountNo_1
from Regression.PageFactory.VerificationPage import VerificationPage
from Regression.States.CirroEnroll import CirroEnroll
from Regression.sprint_regression.Cirro_regression.helpers.names_and_address_generator import \
    names_and_address_generator

test_name = "CirroTest_enrollment_process_PA"
local_path = "./inbox_folder/TestData_Cirro.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
# worksheet = workbook.sheet_by_name('Cirro_data_03_2020')
worksheet = workbook.sheet_by_name('Regression_')
make_report = "1" # If you need to feel full report - enter "1", if no - enter "0"
electric_enrollment = []
tester = "Alex"
nerf_api_link = "http://nerf.api.pt.nrgpl.us/api/v1/orders/?enrollment_number="
headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(5, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    electric_enrollment.append(Payload(**value_dict))

# log = cl.genericLogger(logging.DEBUG)


@pytest.fixture(scope='session')
def driver(request):
    print('driver_setup()')
    if os.environ.get('USE_PHANTOM'):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(6000,2000)
    else:
        _driver = webdriver.Firefox()

    _driver.get_screenshot_as_file('..\TestScripts\screenshots')
    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            _driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver

# log.info("New Test started")


@pytest.mark.parametrize("payload", electric_enrollment, ids=[p.ts for p in electric_enrollment])

def test_state(driver, payload):
    if make_report == "1":
        now = datetime.now()
        date = now.strftime("_%m_%d_%Y_")
        filename = ("./outbox_folder/" + test_name + date + "_tests_results.csv")
        if os.path.exists(filename) == True:
            pass
        else:
            f = open(filename, 'w', newline='')
            csv_a = csv.writer(f)
            #todo
            csv_a.writerow(
                ["status", "tester", "time", "payload.tc", "payload.sku1", "str(payload.url)", "InsertDate", "ConfirmationNumber", "order_status"])
            f.close()

    else:
        pass

    print( payload.ts, 'NRG WEB Electric Enrollment - State = ', payload.state, ' - utility = ', payload.utility)

    try:
        _state_test_internals(driver, payload)
    except Exception as ae:
        import uuid
        filename = "./failed/test_email_portallink_fail_{}_{}.png".format(payload.ts, uuid.uuid4())
        driver.get_screenshot_as_file(filename)
        print("Saving screenshot of failed test -- ", payload.ts)
        print("filename:", filename)
        print(str(ae))
        raise ae

def _state_test_internals(driver, payload):
        print( "getting url: %s" % payload.url )
        driver.get( payload.url )
        driver.maximize_window( )
        driver.implicitly_wait( 60 )

        ## Personal Information
        print("Personal Information")

        print("title: ", driver.title)
        address_house_street_generated, first_name_generated, last_name_generated, email_generated, \
        phone_area_code_generated, phone_last_generated, phone_prefix_generated, email_generated, \
        phone_number_generated, address_house_street_generated, member_number = names_and_address_generator()
        last_name = str(payload.ts) + "_" + payload.utility
        accountNo = account_generator_accountNo_1(payload.utility)
        CirEn= CirroEnroll(driver)
        # log.info("Getting the blacklisted_email method from the NRGEnroll page")
        CirEn.fill_personalinformation(first_name_generated, accountNo, payload)
        # Verification
        vp = VerificationPage(driver)
        vp.scroll_cirro_termsandconditions_and_agree_landingpage()
        # time.sleep(5)

        ## Grab Confirmation Code
        # time.sleep(12)

        ConfirmationNumber = driver.find_element_by_id('confirmation').text

        print('ConfirmationNumber is: ' + ConfirmationNumber)

        driver.get(nerf_api_link + str(ConfirmationNumber))
        order_status_xpath = driver.find_element_by_xpath(
            '//span[contains(text(),"order_status")] [1]/following-sibling::span[3]')
        order_status = str(order_status_xpath.text)
        try:
            assert order_status == '"completed"'
        except:
            print("!!!! FAILED status 'epnet_file_sent'")



        if make_report == "1":
            now = datetime.now()
            time = now.strftime("_%m_%d_%Y_%I_%M_%S_%p")
            date = now.strftime("_%m_%d_%Y_")
            filename = ("./outbox_folder/" + test_name + date + "_tests_results.csv")
            f = open(filename, 'a', newline='')
            csv_a = csv.writer(f)
            InsertDate = now.strftime("%Y-%m-%d")
            csv_a.writerow(
                [ payload.ts, payload.sku1, str(payload.url),first_name_generated, last_name,  payload.Service_Address1,
                  payload.city, payload.zipcode, accountNo, InsertDate, ConfirmationNumber, date, order_status[1:-1]])


