from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple
from States.NrgEnroll import NrgEnroll
from ECC_PageFactory.test_SignUpAccount import test_SignUpAccount
from PageFactory.ConfirmationPage import ConfirmationPage
from PageFactory.VerificationPage import VerificationPage
from PageFactory.ThanksPage import ThanksPage
import pytest
from PageFactory.HomePage import HomePage
from PageFactory.PlansPage import PlansPage
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pytest
import logging
import ConfigFiles.logger as cl


local_path = "./ECC_TestData/TestData.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('PAUtilities')

electric_enrollment = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    electric_enrollment.append(Payload(**value_dict))

log = cl.genericLogger(logging.DEBUG)

@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('USE_PHANTOM'):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(6000,2000)
    else:
        print("making Chrome driver")
        Caps= DesiredCapabilities.CHROME
        Caps["pageLoadStrategy"]= "none"
        _driver = webdriver.Chrome('/usr/local/bin/chromedriver', desired_capabilities= Caps)


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
        filename = "./failed/test_email_portallink_fail_{}_{}.png".format(payload.tc,uuid.uuid4())
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.tc)
        print("filename:", filename)
        print(str(ae))
        raise ae

def _state_test_internals(driver, payload):
        print( "getting url: %s" % payload.url )
        driver.get( payload.url )
        driver.maximize_window( )
        driver.implicitly_wait( 3 )


        NrgEn = NrgEnroll(driver)

        ## Personal Information
        print("Personal Information")

        print("title: ", driver.title)

        NrgEn= NrgEnroll(driver)
        log.info("Getting the blacklisted_email method from the NRGEnroll page")
        NrgEn.fill_personalinformation_with_SWAP(payload)

        # Verification
        vp = VerificationPage(driver)
        vp.scroll_termsandconditions_and_agree()
        time.sleep(2)

        ## Grab Confirmation Code
        cop = ConfirmationPage(driver)
        confirmationNum = cop.get_confirmation_number()
        print("Confirmation number generated")
        time.sleep(2)

        ##Selecting all Preferences
        print("Selecting Preferences")
        NrgEn.select_preferences_and_save()
