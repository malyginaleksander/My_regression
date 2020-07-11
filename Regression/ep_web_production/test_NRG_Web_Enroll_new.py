from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from States.NrgEnroll import NrgEnroll
from PageFactory.VerificationPage import VerificationPage
from collections import namedtuple
from PageFactory.ConfirmationPage import ConfirmationPage

local_path = './ep_web_production/prod_data.xlsx'
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('NRG_regression Web Enroll')

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

@pytest.mark.parametrize("payload", state_data, ids=[
    p.tc.lower() for p in state_data
])
def test_state(driver, payload):
    print(payload.tc, 'NRG_regression WEB Electric Production Enrollment - Utility = ', payload.utility)

    driver.get(payload.url)
    driver.implicitly_wait(30)

    nrg = NrgEnroll(driver)

    nrg.clickImage()
    nrg.enter_personal_information(payload)
    nrg.select_ElectricUtility_and_submit(payload)

    verification = VerificationPage(driver)
    verification.scroll_termsandconditions_and_agree()

    cop = ConfirmationPage(driver)
    confirmationNum = cop.get_confirmation_number()
    print("Confirmation Number is: " + confirmationNum)
