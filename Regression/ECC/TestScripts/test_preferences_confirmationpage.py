from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple
from PageFactory.ConfirmPlanPage import ConfirmPlanPage
from States.NrgEnroll import NrgEnroll
from ECC_PageFactory.test_SignUpAccount import test_SignUpAccount
from PageFactory.ConfirmationPage import ConfirmationPage
from PageFactory.VerificationPage import VerificationPage
from PageFactory.ThanksPage import ThanksPage
import pytest
from PageFactory.cognito_services import get_pool_id, get_user, delete_user

local_path = "./ECC_TestData/TestData.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('Confirmation_Preferences')

conf_pref = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    conf_pref.append(Payload(**value_dict))

@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('USE_PHANTOM'):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(1400,1000)
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


@pytest.mark.parametrize("payload", conf_pref, ids=[p.tc for p in conf_pref])

def test_state(driver, payload):
     print( payload.tc, 'NRG_regression WEB Electric Enrollment - State = ', payload.state, ' - utility = ', payload.utility )

     try:
        _state_test_internals(driver, payload)
     except Exception as ae:
        import uuid
        filename = "./failed/test_enroll_electric_fail_{}_{}.png".format(payload.tc,uuid.uuid4())
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.tc)
        print("filename:", filename)
        print(str(ae))
        raise ae


def _state_test_internals(driver, payload):
        host = os.environ.get('ECC_ENROLL_HOST', 'https://nrg.enroll.pt.nrgpl.us/')
        url = '{}{}'.format(host, payload.query_string)
        print("getting url: %s" % url)
        driver.get(url)
        driver.implicitly_wait(3)

        ## Personal Information
        print( "Personal Information" )
        
        NrgEn= NrgEnroll(driver)
        NrgEn.fill_data(payload)

        ## Filling member details and then submit all the changes
        NrgEn.fill_memberdetails(payload)

        # Verification
        vp = VerificationPage( driver )
        vp.scroll_termsandconditions_and_agree()

        ## Grab Confirmation Code
        cop = ConfirmationPage( driver )
        confirmationNum = cop.get_confirmation_number()
        print( "Confirmation Number is: " + str(confirmationNum))
        #Here Expected confirmation number should be updated
        assert confirmationNum == confirmationNum
        
        ##Select Preferences
        print( "Preferences" )
        NrgEn.preferences_selection_confirmationpage(payload)
