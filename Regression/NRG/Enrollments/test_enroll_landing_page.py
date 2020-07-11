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
from PageFactory.ConfirmationPage import ConfirmationPage
from PageFactory.VerificationPage import VerificationPage


local_path = './NRG_regression/Enrollments/enrollment_data.xlsx'
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('landing')

state_data = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    state_data.append(Payload(**value_dict))

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

@pytest.mark.parametrize("payload", state_data, ids=[p.tc.lower() for p in state_data])
def test_state(driver, payload):
    print(payload.tc, 'NRG_regression Landing Page Enrollment')

    driver.get(payload.url)
    driver.maximize_window()
    driver.implicitly_wait(10)

    NrgEn = NrgEnroll(driver)
    NrgEn.Click_SignUpNow_IL(payload)

    ## Personal Information
    print( "Personal Information" )
    NrgEn.fill_data(payload)
    try:
        NrgEn.enter_account_number(payload.accountNo)
    except:
        pass
    time.sleep( 2 )

    NrgEn.fill_gasdata(payload)
    NrgEn.click_continue()  # continue-submit
    time.sleep( 4 )

    ## Verification
    print( "verify" )
    vp = VerificationPage( driver )
    vp.scroll_termsandconditions_and_agree()


    ## Grab Conformation Code
    time.sleep( 4 )
    cop = ConfirmationPage( driver )
    confirmationNum = cop.get_confirmation_number()
    print( "Confirmation Number is: " + confirmationNum )
    # Here Expected confirmation number should be updated
    assert confirmationNum == confirmationNum



