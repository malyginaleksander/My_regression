from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'offer'])

offer = [
    ['tc-01', 'ny-mp001']
]

offer_data = [
    Payload(tc = current_row[0],
            offer = current_row[1],
            )
    for current_row in offer
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

@pytest.mark.parametrize("payload", offer_data, ids=[
    p.tc.lower() for p in offer_data
])
def test_state(driver, payload):
    print(payload.tc, 'NY Consent emaill field check')

    driver.get("http://www.pt.energypluscompany.com/specialoffer")
    driver.implicitly_wait(30)
    elem = driver.find_element_by_name("customer_code").send_keys(payload.offer)
    elem = driver.find_element_by_class_name("btn").click()
    elem = driver.find_element_by_class_name("btn").click()

    assert "Thank you for signing up!" not in driver.page_source