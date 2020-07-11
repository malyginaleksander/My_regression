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

Payload = namedtuple('payload', ['tc', 'url', 'first_name', 'last_name', 'email_addr', 'confirm_email_addr', 
'Service_Address1', 'city', 'zipcode', 'Service_phone_number', 'accountNo', 'state', 'utility'])

data = [
    ['tc-01', 'https://nrg.enroll.pt.nrgpl.us?product_id=286E5E6F-D605', 'NRG_regression-WEB', 'METED', 'NRG_regression-WEB@x.com', 'NRG_regression-WEB@x.com', '902 Silver Spring Ln', 'Wexford', '15090', '2158278526', '0873603271971382800000', 'PA', 'METED']
]

state_data = [
    Payload(tc = current_row[0],
        url = current_row[1],
        first_name = current_row[2],
        last_name = current_row[3],
        email_addr = current_row[4],
        confirm_email_addr = current_row[5],
        Service_Address1 = current_row[6],
        city = current_row[7],
        zipcode = current_row[8],
        Service_phone_number = current_row[9],
        accountNo = current_row[10],
        state = current_row[11],
        utility = current_row[12],
        )
    for current_row in data
]

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
    print(payload.tc, 'NRG_regression WEB Electric Enrollment - State = ', payload.state, ' - utility = ', payload.utility)

    driver.get(payload.url)
    time.sleep(2)

    ## Personal Information
    print("Personal Information")
    NrgEn = NrgEnroll( driver )
    NrgEn.fill_data(payload)

    ## Filling member details and then submit all the changes for Bad Mem details
    NrgEn.fill_memberdetails_for_badmember(payload)
