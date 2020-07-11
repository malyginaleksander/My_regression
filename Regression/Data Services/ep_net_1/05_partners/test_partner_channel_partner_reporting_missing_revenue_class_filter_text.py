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

Payload = namedtuple('payload', ['tc', 'tc_description', 'field', 'expected_xpath', 'entered_text', 'expected_text'])

missing = [
    ['tc-01', 'filter Channel Partner Reporting Missing Revenue Class by Utility Account Number', 'gs_UtilityAccountNumber', '/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[1]', '13009400014', '13009400014'],
    ['tc-02', 'filter Channel Partner Reporting Missing Revenue Class by Partner Code', 'gs_PartnerCode', '/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[3]', 'Qtr 3 2015', 'Qtr 3 2015'],
    ['tc-03', 'filter Channel Partner Reporting Missing Revenue Class by Sender Transaction Id', 'gs_SenderTransactionId', '/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[5]', 'DROP', 'DROP'],
    ['tc-04', 'filter Channel Partner Reporting Missing Revenue Class by Invoice Total', 'gs_InvoiceTotal', '/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[6]', 'ENROLL-ACCEPT', 'ENROLL-ACCEPT'],
]

missing_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
            field = current_row[2],
            expected_xpath = current_row[3],
            entered_text = current_row[4],
            expected_text = current_row[5],
            )
    for current_row in missing
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

@pytest.mark.parametrize("payload", missing_data, ids=[
    p.tc.lower() for p in missing_data
])
def test_missing(driver, payload):
    print(payload.tc, ' - ', payload.tc_description)

    driver.get("http://epnet2.pt.nrgpl.us/ChannelPartnerReporting#missing-revenue-classes")
    driver.implicitly_wait(30)

    elem = driver.find_element_by_id(payload.field).send_keys(payload.entered_text)
    elem = driver.find_element_by_id(payload.field).send_keys(Keys.ENTER);
    element = driver.find_element_by_xpath(payload.expected_xpath)
    assert element.text == (payload.expected_text)
    assert "Unexpected Error" not in driver.page_source 

