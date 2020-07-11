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

Payload = namedtuple('payload', ['tc'])

vip = [
    ['tc-01'],
]

vip_data = [
    Payload(tc = current_row[0],
            )
    for current_row in vip
]

@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('BUILD_ID', None):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(1700, 1100)
    else:
        print("making Firefox driver")
        #_driver = webdriver.Firefox()
        _driver = webdriver.Chrome('C:\Python34\chromedriver.exe')
        _driver.set_window_size(1800, 1150)
        
    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            _driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver

@pytest.mark.parametrize("payload", vip_data, ids=[
    p.tc.lower() for p in vip_data
])
def test_vip(driver, payload):
    print(payload.tc, ' - ', 'Add VIP')

    driver.get("http://epnet1.pt.nrgpl.us/Marketing/VIPMaintenance.aspx")
    driver.implicitly_wait(10)
    time.sleep(5)
    elem = driver.find_element_by_id("ctl00_MainContent_TabContainer1_ctl00_btnAddNew").click()
    elem = driver.find_element_by_id("ctl00_MainContent_TabContainer1_ctl00_gvVips_ctl02_txtFirstName").send_keys("a1")
    elem = driver.find_element_by_id("ctl00_MainContent_TabContainer1_ctl00_gvVips_ctl02_txtLastName").send_keys("a1")
    elem = driver.find_element_by_id("ctl00_MainContent_TabContainer1_ctl00_gvVips_ctl02_UpdateButton").click()
    assert "a1" in driver.page_source
    elem = driver.close