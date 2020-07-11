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

Payload = namedtuple('payload', ['tc', 'tc_description', 'field', 'expected_xpath', 'expected_text'])

segment = [
    ['tc-01', 'filter Price Segment by Price Segment', 'gs_PriceSegment', '/html/body/div[1]/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[1]', '00004'],
    ['tc-02', 'filter Price Segment Log by Adder', 'gs_Adder', '/html/body/div[1]/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[3]', '0.78417'],
    ['tc-03', 'filter Price Segment Log by Demand Adder', 'gs_DemandAdder', '/html/body/div[1]/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[4]', '0.089'],
    ['tc-04', 'filter Price Segment Log by Description', 'gs_Description', '/html/body/div[1]/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[7]', 'D2D Ongoing'],
]

segment_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
            field = current_row[2],
            expected_xpath = current_row[3],
            expected_text = current_row[4],
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
        _driver.set_window_size(1600, 1150)
        
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

    elem = driver.find_element_by_id(payload.field).send_keys(payload.expected_text)
    elem = driver.find_element_by_id(payload.field).send_keys(Keys.ENTER);
    element = driver.find_element_by_xpath(payload.expected_xpath)
    assert element.text == (payload.expected_text)
    assert "Unexpected Error" not in driver.page_source