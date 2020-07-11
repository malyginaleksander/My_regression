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

base = [
    ['tc-01', 'filter Admin Pricing Base Cost by Utility', 'gs_UtilityCode', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[12]', '40'],
]

base_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
            field = current_row[2],
            expected_xpath = current_row[3],
            expected_text = current_row[4],
            )
    for current_row in base
]

@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('BUILD_ID', None):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(1820, 550)
    else:
        print("making Firefox driver")
        #_driver = webdriver.Firefox()
        _driver = webdriver.Chrome('C:\Python34\chromedriver.exe')
        _driver.set_window_size(1800, 1150)
        
    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            #_driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver

@pytest.mark.parametrize("payload", base_data, ids=[
    p.tc.lower() for p in base_data
])
def test_awards(driver, payload):
    print(payload.tc, ' - ', payload.tc_description)

    driver.get("http://epnet2.pt.nrgpl.us/Pricing#admin")
    driver.implicitly_wait(10)
    time.sleep(1)
    elem = driver.find_element_by_id("pricingAdminComboBox").click()
    elem = driver.find_element_by_id("pricingAdminComboBox").send_keys(Keys.ARROW_DOWN);
    elem = driver.find_element_by_id("pricingAdminComboBox").send_keys(Keys.ENTER);
    driver.implicitly_wait(10)
    driver.implicitly_wait(10)
    time.sleep(1)
    elem = driver.find_element_by_id(payload.field)
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == payload.expected_text:
            option.click()      
    time.sleep (1)
    element = driver.find_element_by_xpath(payload.expected_xpath)
    assert element.text == (payload.expected_text)
    assert "Unexpected Error" not in driver.page_source


