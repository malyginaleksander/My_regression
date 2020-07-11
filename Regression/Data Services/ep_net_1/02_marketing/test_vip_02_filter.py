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

Payload = namedtuple('payload', ['tc', 'tc_description', 'field', 'expected_xpath', 'select', 'expected_text'])

vip = [
    ['tc-01', 'Filter Partner Code', 'ctl00_MainContent_TabContainer1_ctl00_ddlPartnerCode', '/html/body/form/div[3]/div[2]/div/div[2]/div[1]/table[2]/tbody/tr/td/div/div/div/div[2]/div/div/div/table/tbody/tr[2]/td[8]', '(AAL) American Airlines', 'AAL'],
    ['tc-02', 'Filter Priority', 'ctl00_MainContent_TabContainer1_ctl00_ddlPriorityLevel', '/html/body/form/div[3]/div[2]/div/div[2]/div[1]/table[2]/tbody/tr/td/div/div/div/div[2]/div/div/div/table/tbody/tr[2]/td[7]', 'VIP003 (003)', 'VIP003'],
    ['tc-03', 'Filter Partner Code', 'ctl00_MainContent_TabContainer1_ctl00_ddlState', '/html/body/form/div[3]/div[2]/div/div[2]/div[1]/table[2]/tbody/tr/td/div/div/div/div[2]/div/div/div/table/tbody/tr[2]/td[9]', 'MD', 'MD'],
]

vip_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
            field = current_row[2],
            expected_xpath = current_row[3],
            select = current_row[4],
            expected_text = current_row[5],           
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
    print(payload.tc, ' - ', 'Filter VIP')

    driver.get("http://epnet1.pt.nrgpl.us/Marketing/VIPMaintenance.aspx")
    driver.implicitly_wait(10)
    time.sleep(5)
    elem = driver.find_element_by_id(payload.field)
    for option in elem.find_elements_by_tag_name('option'):
        if option.text.strip() == payload.select:
            option.click()
            time.sleep(10)
    elem = driver.find_element_by_id("ctl00_MainContent_TabContainer1_ctl00_btnFilterAll01").click()
    element = driver.find_element_by_xpath(payload.expected_xpath) 
    assert element.text == (payload.expected_text)
    elem = driver.close