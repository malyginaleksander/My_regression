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

award = [
    ['tc-01']   
]

award_data = [
    Payload(tc = current_row[0],
            )
    for current_row in award
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

@pytest.mark.parametrize("payload", award_data, ids=[
    p.tc.lower() for p in award_data
])
def test_awards(driver, payload):
    print(payload.tc, ' - Paging')

    driver.get("http://epnet2.pt.nrgpl.us/awards")
    driver.implicitly_wait(10)
    elem = driver.find_element_by_id("awardsSearchButton").click()
    driver.implicitly_wait(10)

    elem = driver.find_element_by_id("next_awardsPager").click()
    assert "View 51 - 100" in driver.page_source
    print ("next");
    
    elem = driver.find_element_by_id("prev_awardsPager").click()
    assert "View 1 - 50" in driver.page_source
    print ("previous");

    elem = driver.find_element_by_class_name("ui-pg-input").send_keys(Keys.CONTROL, "a");
    elem = driver.find_element_by_class_name("ui-pg-input").send_keys(Keys.DELETE);    
    elem = driver.find_element_by_class_name("ui-pg-input").send_keys("5")
    elem = driver.find_element_by_class_name("ui-pg-input").send_keys(Keys.ENTER);
    assert "View 201 - 250" in driver.page_source
    print ("select");

    elem = driver.find_element_by_id("first_awardsPager").click()
    assert "View 1 - 50" in driver.page_source
    print ("first");

