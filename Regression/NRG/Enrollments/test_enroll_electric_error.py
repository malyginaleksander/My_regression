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

local_path = './NRG_regression/Enrollments/enrollment_data.xlsx'
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('electric error')

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
        _driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
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
    print(payload.tc, 'NRG_regression WEB Electric UAN error Check - State = ', payload.state, ' - utility = ', payload.utility)

    print("getting url: %s" % payload.url)

    try:
        _state_test_internals(driver, payload)
    except Exception as ae:
        import uuid
        filename = "./failed/test_enroll_electric_error_fail_{}_{}.png".format(
            payload.tc,
            uuid.uuid4())
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.tc)
        print("filename:", filename)
        print(str(ae))
        raise ae


def _state_test_internals(driver, payload):
    driver.get(payload.url)
    driver.maximize_window()
    driver.implicitly_wait(30)


    ## Personal Information
    print( "Personal Information" )

    NrgEn = NrgEnroll(driver)
    NrgEn.fill_data(payload)
    NrgEn.enter_account_number(payload.accountNo)
    NrgEn.click_continue()
    time.sleep(4)
    assert driver.find_element_by_id("id_electric-uan-error").is_displayed

