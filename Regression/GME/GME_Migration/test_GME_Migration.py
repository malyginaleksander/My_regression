from __future__ import print_function
import csv
from datetime import datetime

from selenium import webdriver
import time
import xlrd
import os
from collections import namedtuple

from webdriver_manager.chrome import ChromeDriverManager

# from Regression.Migration.GME_Migration.GME_WebEnroll_settings import *
from Regression.GME.GME_Migration.helpers.GmeEnroll import fill_personalinformation, gme_scroll_termsandconditions_and_agree, get_confirmation_number
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import  expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Regression.GME.GME_Migration.GME_WebEnroll_settings import workbook_name, data_sheet_name, start_string, \
    make_report, url
# from Regression.GME.GME_Migration.helpers.GmeEnroll import fill_personalinformation

local_path = workbook_name
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name(data_sheet_name)

electric_enrollment = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(int(start_string), worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    electric_enrollment.append(Payload(**value_dict))

# log = cl.genericLogger(logging.DEBUG)

@pytest.fixture(scope='module')
def driver(request, chosen_driver='chrome'):
    print('driver_setup()')
    if os.environ.get('USE_PHANTOM'):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(6000, 2000)
    else:
        print("making Firefox driver")
        _driver = webdriver.Firefox()


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
    # if payload.StateSlug=='ma':
    #     pass
    # else:
    #     if payload.status_3 =='IDOC Processed Sucessfully.':
    #         pass
    #     else:

            try:
                _state_test_internals(driver, payload)
            except Exception as ae:
                import uuid
                now = datetime.now()
                current_time = now.strftime("_%m_%d_%Y_%I_%M_%S_%p_")
                filename = "./failed/test_email_portallink_fail__"+payload.ts+"_"+ current_time+ ".png"
                driver.save_screenshot(filename)
                print("Saving screenshot of failed test -- ", payload.ts)
                print("filename:", filename)
                print(str(ae))
                f = open( "./outbox_files/failed.csv", 'a', newline='')
                csv_a = csv.writer(f)
                if make_report == "1":
                    csv_a.writerow(
                        ["FAILED",  time, payload.ts, payload.sku, str(url + str(payload.sku)),
                         payload.StateSlug ])
                raise ae


def _state_test_internals(driver, payload):

        full_url = str(url + str(payload.sku))
        driver.get(full_url)
        print( "getting url: %s" %  full_url )

        # driver.maximize_window( )
        driver.implicitly_wait(3)
        if payload.StateSlug.upper() == "IL":
            try:
                driver.switch_to_alert()
                driver.find_element_by_id('close-uds').click()
                time.sleep(2)
            except:
                pass
        WebDriverWait(driver, 20).until(expected_conditions.visibility_of_element_located((By.ID, 'id_first_name')))

        ## Personal Information
        print("Personal Information")
        print("title: ", driver.title)
        now = datetime.now()

        fill_personalinformation(driver, payload)

        # Verification
        gme_scroll_termsandconditions_and_agree(driver, payload)
        # time.sleep(2)

        # Grab Confirmation Code
        get_confirmation_number(driver,payload)

        print("Confirmation number generated")
        # time.sleep(5)

