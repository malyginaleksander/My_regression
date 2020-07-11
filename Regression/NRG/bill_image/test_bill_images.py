from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'url'])

local_path = "./NRG_regression/bill_image/bill_images.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('bill image urls')

image_data = [
    Payload(tc = worksheet.row(current_row)[0].value,
    url = worksheet.row(current_row)[1].value,
    )
for current_row in range(1,worksheet.nrows)
]

@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('USE_PHANTOM'):
        print("making PhantomJS driver")

        #_driver = webdriver.PhantomJS()
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

@pytest.mark.parametrize("payload", image_data, ids=[
    p.tc.lower() for p in image_data
])
def test_state(driver, payload):
    print(payload.tc, 'Bill Image URL = ', payload.url)
    print("getting url: %s" % payload.url)

    try:
        _state_test_internals(driver, payload)
    except Exception as ae:
        import uuid
        filename = "./failed/test_bill_image_fail_{}_{}.png".format(
            payload.tc,
            uuid.uuid4())
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.tc)
        print("filename:", filename)
        print(str(ae))
        raise ae


def _state_test_internals(driver, payload):

    driver.get(payload.url)
    driver.implicitly_wait(30)
    assert driver.current_url == payload.url
    assert "NoSuchKey" not in driver.page_source
