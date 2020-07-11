from __future__ import print_function
from selenium import webdriver
import time
import xlrd
import os
from collections import namedtuple
from Regression.States.CirroEnroll import CirroEnroll
from Regression.PageFactory.VerificationPage import VerificationPage
import pytest
import logging
import Regression.ConfigFiles.logger as cl


local_path = "../../ECC_TestData/TestData_Cirro.xlsx"
full_path = os.path.abspath(local_path)
# workbook = xlrd.open_workbook('C:/Users/AMALYGIN/Downloads/Regression-master (5)/Regression-master/Regression/ECC_TestData/TestData_Cirro.xlsx')
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('Cirro_data')

electric_enrollment = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    electric_enrollment.append(Payload(**value_dict))

log = cl.genericLogger(logging.DEBUG)

@pytest.fixture(scope='session')
def driver(request):
    print('driver_setup()')
    if os.environ.get('USE_PHANTOM'):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(6000,2000)
    else:
        print("making Chrome driver")
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

log.info("New Test started")


@pytest.mark.parametrize("payload", electric_enrollment, ids=[p.tc for p in electric_enrollment])

def test_state(driver, payload):
     print( payload.tc, 'NRG_regression WEB Electric Enrollment - State = ', payload.state, ' - utility = ', payload.utility)

     try:
        _state_test_internals(driver, payload)
     except Exception as ae:
        import uuid
        filename = "./failed/test_email_portallink_fail_{}_{}.png".format(payload.tc, uuid.uuid4())
        driver.get_screenshot_as_file(filename)
        print("Saving screenshot of failed test -- ", payload.tc)
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

        CirEn= CirroEnroll(driver)
        log.info("Getting the blacklisted_email method from the NRGEnroll page")
        CirEn.fill_personalinformation(payload)




        # Verification
        vp = VerificationPage(driver)
        vp.scroll_cirro_termsandconditions_and_agree_landingpage()
        # time.sleep(5)

        ## Grab Confirmation Code
        # time.sleep(12)

        ConfirmationNumber = driver.find_element_by_id('confirmation').text
        print('ConfirmationNumber is: ' + ConfirmationNumber)
        time.sleep(2)


