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


Payload = namedtuple('payload', ['tc', 'url', 'zipcode'])

results_data = [
    ['tc-01', 'http://enroll.pt.nrghomepower.com/', '90210']
]

zip_data = [
    Payload(tc = current_row[0],
            url = current_row[1],
            zipcode = current_row[2],
            )
    for current_row in results_data
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

@pytest.mark.parametrize("payload", zip_data, ids=[
    p.tc.lower() for p in zip_data
])
def test_state(driver, payload):
    print(payload.tc, 'NRG_regression Landing Page Zip Check ', payload.zipcode)

    driver.get(payload.url)
    driver.implicitly_wait(10)

    NrgEn = NrgEnroll(driver)
    NrgEn.landing_invalid_zip(payload)
