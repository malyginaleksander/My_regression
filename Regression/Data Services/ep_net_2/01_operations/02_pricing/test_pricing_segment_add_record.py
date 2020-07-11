from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'tc_description'])

segment = [
    ['tc-01', 'Add Record'],
]

segment_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
            )
    for current_row in segment
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

@pytest.mark.parametrize("payload", segment_data, ids=[
    p.tc.lower() for p in segment_data
])
def test_awards(driver, payload):
    print(payload.tc, ' - ', payload.tc_description)

    driver.get("http://epnet2.pt.nrgpl.us/Pricing#segments")
    driver.implicitly_wait(10)
    elem = driver.find_element_by_id("add_priceSegmentsGrid").click()
    elem = driver.find_element_by_id("PriceSegment").send_keys("R2D2C3P0")
    elem = driver.find_element_by_id("Adder").send_keys("0.1140")
    elem = driver.find_element_by_id("DemandAdder").send_keys("0.1140")
    elem = driver.find_element_by_id("RoundingMethod").send_keys("NONE")
    elem = driver.find_element_by_id("Description").send_keys("Test")
    elem = driver.find_element_by_id("sData").click()
    elem = driver.find_element_by_id("cData").click()
    driver.get("http://epnet2.pt.nrgpl.us/Pricing#segments")
    driver.implicitly_wait(10)
    elem = driver.find_element_by_id("gs_PriceSegment").send_keys("R2D2C3P0")
    elem = driver.find_element_by_id("gs_PriceSegment").send_keys(Keys.ENTER);
    element = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[1]")
    assert element.text == ("R2D2C3P0")