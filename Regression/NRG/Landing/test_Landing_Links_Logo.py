from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple


local_path = "./NRG_regression/Landing/nrg_links.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('Landing')

landing_data = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    landing_data.append(Payload(**value_dict))

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

@pytest.mark.parametrize("payload", landing_data, ids=[
    p.tc.lower() for p in landing_data])

def test_state(driver, payload):
    print(payload.tc, 'NRG_regression WEB landing page link check = ', payload.expected, ' - expected = ', payload.expected)
    print(payload.page)
    driver.get(payload.page)
    time.sleep(4)

    driver.find_element_by_xpath(payload.xpath1).click()
    if payload.footer_type== "footer - home":
        driver.switch_to.alert.accept()
 
    assert driver.current_url.startswith(payload.expected)
