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

base = [
    ['tc-01', 'Add Record'],
]

base_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
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

    elem = driver.find_element_by_id("add_pricingAdminGrid").click()

    elem = driver.find_element_by_id('Ancillary').send_keys("0.9991")
    elem = driver.find_element_by_id('BaseSupply').send_keys("0.9991")
    elem = driver.find_element_by_id('Demand').send_keys("0.9991")
    elem = driver.find_element_by_id('EffectiveDate').send_keys("01/31/2012")
    elem = driver.find_element_by_id('Green').send_keys("0.01000")
    elem = driver.find_element_by_id('LineLoss').send_keys("0.00000")
    elem = driver.find_element_by_id('UFE').send_keys("0.00000")
    elem = driver.find_element_by_id("UtilityCode")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == ("02"):
            option.click()
    elem = driver.find_element_by_id("sData").click()
    time.sleep(3)
    elem = driver.find_element_by_id("cData").click()