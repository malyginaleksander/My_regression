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

base = [
    ['tc-01', 'filter Admin Pricing Base Cost by Ancillary', 'gs_Ancillary', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]', '0.005', '0.00500'],
    ['tc-02', 'filter Admin Pricing Base Cost by Base Supply', 'gs_BaseSupply', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]', '0.0422', '0.04220'],
    ['tc-03', 'filter Admin Pricing Base Cost by Demand', 'gs_Demand', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]', '0.0286', '0.02860'],
    ['tc-04', 'filter Admin Pricing Base Cost by Green', 'gs_Green', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]', '0.009', '0.00990'],
    ['tc-05', 'filter Admin Pricing Base Cost by Line Loss', 'gs_LineLoss', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]', '0.0041', '0.00410'],
    ['tc-06', 'filter Admin Pricing Base Cost by Revenue Class', 'gs_RevenueClass', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[8]', '3', '3'],
    ['tc-07', 'filter Admin Pricing Base Cost by Total Base Cost', 'gs_TotalBaseCost', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[9]', '0.0627', '0.06270'],
    ['tc-08', 'filter Admin Pricing Base Cost by UFE', 'gs_UFE', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]', '0.006', '0.00600'],
    ['tc-08', 'filter Admin Pricing Base Cost by SPL', 'gs_SPL', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[11]', 'I', 'I'],
]

base_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
            field = current_row[2],
            expected_xpath = current_row[3],
            entered_text = current_row[4],
            expected_text = current_row[5],
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
            _driver.close()
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
    elem = driver.find_element_by_id(payload.field).send_keys(payload.entered_text)
    elem = driver.find_element_by_id(payload.field).send_keys(Keys.ENTER);
    element = driver.find_element_by_xpath(payload.expected_xpath)
    assert element.text == (payload.expected_text)
    assert "Unexpected Error" not in driver.page_source