from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple
from States.CustomerCareHome import CustomerCareHome

local_path = "./EP_Web/Links/links.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('Page Links')


link_data = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    link_data.append(Payload(**value_dict))


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

@pytest.mark.parametrize("payload", link_data, ids=[p.tc.lower() for p in link_data])

def test_state(driver, payload):
    print(payload.tc, 'EP Web Page Links - ', payload.page, payload.Section, payload.expected)
  

    driver.get(payload.page)

    cch = CustomerCareHome(driver)
    cch.clickxpath(payload)

    time.sleep(1)
    if  "Not Found" in driver.page_source:
        print ("Failed - Not Found")

    if  "Server Error" in driver.page_source:
        print ("Failed - Server Error")
    assert driver.current_url == payload.expected
