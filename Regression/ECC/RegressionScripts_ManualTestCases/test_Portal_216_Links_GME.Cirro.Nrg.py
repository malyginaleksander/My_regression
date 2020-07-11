from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['page', 'xpath', 'expected', 'tc', 'Section', 'asserturl'])

local_path = "./ECC_TestData/TestData.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('links')

link_data = [
    Payload(page = worksheet.row(current_row)[0].value,
            xpath = worksheet.row(current_row)[1].value,
            expected = worksheet.row(current_row)[2].value,
            tc = worksheet.row(current_row)[4].value,
            Section = worksheet.row(current_row)[5].value,
            asserturl = worksheet.row(current_row)[5].value,
            )    
    for current_row in range(1,worksheet.nrows)] 

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

@pytest.mark.parametrize("payload", link_data, ids=[
    p.tc.lower() for p in link_data
])
def test_state(driver, payload):
    print(payload.tc, 'EP Web Page Links - ', payload.page, payload.Section)

    driver.get(payload.page)
    elem = driver.find_element_by_xpath(payload.xpath).click()
    time.sleep(2)

    if  "Not Found" in driver.page_source:
        print ("Failed - Not Found")

    if  "Server Error" in driver.page_source:
        print ("Failed - Server Error")

   # assert driver.current_url == payload.expected
   # print("Asserting xpath")
    #assert driver.find_element_by_xpath(payload.asserturl ).is_displayed( )
    #time.sleep(4)
