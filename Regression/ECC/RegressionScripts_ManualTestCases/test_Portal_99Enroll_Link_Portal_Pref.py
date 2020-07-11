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

#
#----------------------------------------------------------------------
# Read the data in from the accompanying spreadsheet. Header columns
# become the keys of the enroll_data dictionary.
#----------------------------------------------------------------------
#

#TestData folder to be created in the folder where exactly the project is created
#local_path = "./../TestData/NRG_regression/Enrollments/enrollment_data.xlsx"
local_path = "./NRG_regression/Enrollments/enrollment_data.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('electric')

enroll_data = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    enroll_data.append(Payload(**value_dict))

@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('USE_PHANTOM'):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(1120, 550)
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


@pytest.mark.parametrize("payload", enroll_data, ids=[p.tc for p in enroll_data])

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
        print( "getting url: %s" % payload.url )
        driver.get( payload.url )
        driver.maximize_window( )
        driver.implicitly_wait( 3 )


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
        print( "Confirmation Number is: " + confirmationNum )
        #Here Expected confirmation number should be updated
        assert confirmationNum == confirmationNum
        
        ##Select Preferences
        print( "Selecting Preferences" )
        NrgEn.preferences_selection_confirmationpage()
        
        #thanksPage
        #Tp = ThanksPage( driver )
        #thanksText = Tp.getthanksText( )
        
        #Portal login
        time.sleep(5)
        tsignup= test_SignUpAccount()
        tsignup.click_portallink_signup(driver, "9769799764", "Welcome@123")

        #Delete User

        #deleteUser= test_cognito (driver)
       # deleteUser.test_user( )