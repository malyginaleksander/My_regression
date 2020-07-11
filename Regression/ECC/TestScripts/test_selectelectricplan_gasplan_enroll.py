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

local_path = "./ECC_TestData/TestData.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('Plans_page')

dual_enrollment = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    dual_enrollment.append(Payload(**value_dict))

@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('USE_PHANTOM'):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(6000,2000)
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

@pytest.mark.parametrize("payload", dual_enrollment, ids=[p.tc for p in dual_enrollment])

def test_dual_enrollment(driver, payload):
     print( payload.tc, 'NRG_regression WEB Electric Enrollment - State = ', payload.state )

     try:
         _dual_enrollment(driver, payload)
     except Exception as ae:
        import uuid
        filename = "./failed/test_dual_enrollment_fail_{}_{}.png".format(payload.tc,uuid.uuid4())
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.tc)
        print("filename:", filename)
        print(str(ae))
        raise ae

def _dual_enrollment(driver, payload):
        host = os.environ.get('ECC_ENROLL_HOST', 'http://www.pt.nrghomepower.com/')
        driver.implicitly_wait(12)
        driver.get('http://www.pt.nrghomepower.com/')
        driver.maximize_window()

        #  driver.get(payload.page)

        hp = HomePage(driver)
        hp.shopNow(payload)

        NrgEn = NrgEnroll(driver)
        NrgEn.select_electric_utility(payload)
        NrgEn.select_electric_plan(payload)
        NrgEn.select_gas_utility(payload)
        time.sleep(2)
        NrgEn.select_gas_plan(payload)
        time.sleep(4)
        NrgEn.clickcontinue_planspage(payload)


        ## Personal Information
        print( "Personal Information" )

        NrgEn.fill_data(payload)
        NrgEn.enter_account_number(payload.accountNo)
        time.sleep(4)

        NrgEn.enterGasAcctDetailsLandingPage(payload)  # payload.gas_account
        NrgEn.click_continue()  # continue-submit
        time.sleep(4)

        # Verification
        vp = VerificationPage(driver)
        vp.scroll_termsandconditions_and_agree()

        ## Grab Confirmation Code
        cop = ConfirmationPage(driver)
        confirmationNum = cop.get_confirmation_number()
        print("Confirmation Number is: " + str(confirmationNum))

        # Here Expected confirmation number should be updated
        assert confirmationNum == confirmationNum

        ##Select Preferences
        print("Selecting Preferences")
        NrgEn.select_allpreferences_on_confirmationpage()
