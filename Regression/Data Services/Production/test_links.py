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

Payload = namedtuple('payload', ['tc','url'])

worksheet = utils.worksheet('links.xlsx','Links')

link_data = [
    Payload(tc = worksheet.row(current_row)[0].value,
    url = worksheet.row(current_row)[1].value,
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

@pytest.mark.parametrize("payload", link_data, ids=[
    p.tc.lower() for p in link_data
])
def test_link(driver, payload):
    print(payload.tc, payload.url)
    
    driver.get ("http://epnet1.nrgpl.us/login.aspx")
    driver.implicitly_wait(10)
    elem = driver.find_element_by_id("ctl00_MainContent_txtUsername").send_keys("mpetersqa")
    elem = driver.find_element_by_id("ctl00_MainContent_txtPassword").send_keys("Welcome19")
    elem = driver.find_element_by_id("ctl00_MainContent_btnLogin").click()
    driver.implicitly_wait(10)

    driver.get(payload.url)
    driver.implicitly_wait(10)
    assert "Access Denied" not in driver.page_source
    assert "Page Not Found" not in driver.page_source
    driver.implicitly_wait(10)
