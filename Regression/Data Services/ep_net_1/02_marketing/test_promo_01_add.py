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

Payload = namedtuple('payload', ['tc'])

promo = [
    ['tc-01'],
]

promo_data = [
    Payload(tc = current_row[0],
            )
    for current_row in promo
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

@pytest.mark.parametrize("payload", promo_data, ids=[
    p.tc.lower() for p in promo_data
])
def test_promo(driver, payload):
    print(payload.tc, ' - ', 'Add Promo')

    driver.get("http://epnet1.pt.nrgpl.us/Marketing/Promotions.aspx")
    driver.implicitly_wait(10)
    time.sleep(5)
    elem = driver.find_element_by_id("ctl00_MainContent_btnAddNew").click()
    time.sleep(5)
    elem = driver.find_element_by_xpath("ctl00_MainContent_gvPromotions_ctl02_txtPromoCode").send_keys("0001")
    elem = driver.find_element_by_id("ctl00_MainContent_gvPromotions_ctl02_txtPromoName").send_keys("1a")
    elem = driver.find_element_by_id("ctl00_MainContent_gvPromotions_ctl02_ddlBrand")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text.strip() == "NRG_regression Home":
            option.click()
            time.sleep(10)
    elem = driver.find_element_by_id("ctl00_MainContent_gvPromotions_ctl02_UpdateButton").click(()
    elem = driver.close