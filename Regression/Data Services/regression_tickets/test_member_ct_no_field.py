from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc'])

member = [
    ['tc-01']   
]

member_data = [
    Payload(tc = current_row[0],
            )
    for current_row in member
]

@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('BUILD_ID', None):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(1120, 1200)
    else:
        print("making Firefox driver")
        #_driver = webdriver.Firefox()
        _driver = webdriver.Chrome('C:\Python34\chromedriver.exe')
        _driver.set_window_size(1200, 1000)
        
    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            _driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver

@pytest.mark.parametrize("payload", member_data, ids=[
    p.tc.lower() for p in member_data
])
def test_member(driver, payload):
    print(payload.tc, ' - CT Does Not Field Exist')

    # https://energyplus.atlassian.net/browse/COBD-65

    driver.get("http://epnet2.pt.nrgpl.us/member")
    driver.implicitly_wait(10)

    elem = driver.find_element_by_id("memberFormSearchCriteria").send_keys("0550112797957000454003")
    time.sleep(2)
    elem = driver.find_element_by_id("btnUANSearch").submit()
    elem.click()
    driver.implicitly_wait(10)
    elem = driver.find_element_by_xpath("/html/body/div/div[3]/div/div/div[4]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]").click()
    time.sleep(10)
    element = driver.find_element_by_id("communication-section") 
    if driver.find_element_by_id("communication-section").is_displayed():
        print("Failed - yes")
    else:
        print("Passed - no")    

