from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple
from selenium.webdriver.common.action_chains import ActionChains
import utils

Payload = namedtuple('payload', ['tc','url', 'rev_class', 'account', 'state', 'utility'])

worksheet = utils.worksheet('vendor_input.xlsx','vendor')

vendor_data = [
    Payload(tc = worksheet.row(current_row)[0].value,
    url = worksheet.row(current_row)[1].value,
    rev_class = worksheet.row(current_row)[2].value,
    account = worksheet.row(current_row)[3].value,
    state = worksheet.row(current_row)[4].value,
    utility = worksheet.row(current_row)[5].value,
    )
for current_row in range(1,worksheet.nrows)
]

@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('BUILD_ID', None):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(1120, 550)
    else:
        print("making Firefox driver")
        #_driver = webdriver.Firefox()
        _driver = webdriver.Chrome('C:\Python34\chromedriver.exe')
        _driver.set_window_size(1200, 700)
        
    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            _driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver

@pytest.mark.parametrize("payload", vendor_data, ids=[
    p.tc.lower() for p in vendor_data
])
def test_vendor(driver, payload):
    print(payload.tc, 'update vendor -','utility =', payload.utility, '- account number =', payload.account, '- state =', payload.state)

    #https://energyplus.atlassian.net/browse/PROD-1757
    driver.get(payload.url)
    driver.implicitly_wait(10)

    elem = driver.find_element_by_id("RevenueClass")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == payload.rev_class:
            option.click()
            time.sleep(1)
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/form/p/input").click()
    driver.implicitly_wait(10)
    assert "Runtime Error" not in driver.page_source
    driver.implicitly_wait(10)
