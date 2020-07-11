from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'tc_description', 'field_1', 'field_2', 'field_3', 'expected_xpath', 'expected_text_1', 'expected_text_2', 'expected_text_3'])

award = [
    ['tc-01', 'search award by Partner, Utility Account Number and Account Number', 'AccountID', 'Acct', 'PartnerCode', '/html/body/div[1]/div[3]/div/div[1]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]', '136', '0084915159', 'CON'],
]

award_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
    	    field_1 = current_row[2],
            field_2 = current_row[3],
            field_3 = current_row[4],
    	    expected_xpath = current_row[5],
    	    expected_text_1 = current_row[6],
            expected_text_2 = current_row[7],
            expected_text_3 = current_row[8],
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
    print(payload.tc, ' - ', payload.tc_description)

    driver.get("http://epnet2.pt.nrgpl.us/awards")
    driver.implicitly_wait(10)
    
    elem = driver.find_element_by_id(payload.field_1).send_keys(payload.expected_text_1)
    elem = driver.find_element_by_id(payload.field_2).send_keys(payload.expected_text_2)
    elem = driver.find_element_by_id(payload.field_1)
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == payload.expected_text_3:
            option.click()
    elem = driver.find_element_by_id("awardsSearchButton").click()
    driver.implicitly_wait(10)

    element = driver.find_element_by_xpath(payload.expected_xpath)
    assert element.text == (payload.expected_text_1)
    assert "Unexpected Error" not in driver.page_source

    elem = driver.find_element_by_id("awardsSeachClearButton").click()