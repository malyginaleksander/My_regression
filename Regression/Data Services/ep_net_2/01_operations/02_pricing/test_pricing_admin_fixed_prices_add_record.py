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

fixed = [
    ['tc-01', 'Add Record'],
]

fixed_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
            )
    for current_row in fixed
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

@pytest.mark.parametrize("payload", fixed_data, ids=[
    p.tc.lower() for p in fixed_data
])
def test_awards(driver, payload):
    print(payload.tc, ' - ', payload.tc_description)

    driver.get("http://epnet2.pt.nrgpl.us/Pricing#admin")
    driver.implicitly_wait(10)
    time.sleep(1)
    elem = driver.find_element_by_id("pricingAdminComboBox").click()
    elem = driver.find_element_by_id("pricingAdminComboBox").send_keys(Keys.ARROW_DOWN);
    elem = driver.find_element_by_id("pricingAdminComboBox").send_keys(Keys.ARROW_DOWN);
    elem = driver.find_element_by_id("pricingAdminComboBox").send_keys(Keys.ENTER);
    driver.implicitly_wait(10)

    elem = driver.find_element_by_id("add_pricingAdminGrid").click()
    
    elem = driver.find_element_by_id('EffectiveDate').send_keys("12/15/2016")
    elem = driver.find_element_by_id('EffectiveDate').send_keys(Keys.ENTER);
    elem = driver.find_element_by_id("FixedPrice").click()
    elem = driver.find_element_by_id('FixedPrice').send_keys("0.9991")
    time.sleep(2)
    elem = driver.find_element_by_id('editmodpricingAdminGrid').click()
    elem = driver.find_element_by_id('editmodpricingAdminGrid').click()
    elem = driver.find_element_by_id("editmodpricingAdminGrid").send_keys(Keys.ENTER);
    elem = driver.find_element_by_id("UtilityCode")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == ("40"):
            option.click()
    time.sleep(2)
    elem = driver.find_element_by_id("sData").click()
    elem = driver.find_element_by_id("cData").click()