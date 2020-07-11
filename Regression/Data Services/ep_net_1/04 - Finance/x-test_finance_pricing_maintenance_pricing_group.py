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

finance = [
    ['tc-01'],
]

finance_data = [
    Payload(tc = current_row[0],
            )
    for current_row in finance
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

@pytest.mark.parametrize("payload", finance_data, ids=[
    p.tc.lower() for p in finance_data
])
def test_finance(driver, payload):
    print(payload.tc, ' - ', 'Add Price Group')

    driver.get("http://epnet1.pt.nrgpl.us/Finance/InitialOfferPricing.aspx")
    driver.implicitly_wait(30)

    elem = driver.find_element_by_id("ctl00_MainContent_ddlPricingGroup")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == ("CPUV11 / IL Affinity"):
            option.click()
            time.sleep(5)
    elem = driver.find_element_by_id("ctl00_MainContent_ddlInitialOffer")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text.strip() == ("02A83B / Commercial"):
            option.click()
            time.sleep(3)
    elem = driver.find_element_by_id("ctl00_MainContent_ddlState")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text.strip() == ("Illinois"):
            option.click()
            time.sleep(3)     
    elem = driver.find_element_by_id("ctl00_MainContent_ddlUtils")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text.strip() == ("Commonwealth Edison"):
            option.click()
            time.sleep(3) 
    elem = driver.find_element_by_id("ctl00_MainContent_ddlFixedSupplyCharge")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text.strip() == ("0.07900"):
            option.click()
            time.sleep(3) 
    elem = driver.find_element_by_id("ctl00_MainContent_txtSelectedEffectiveDate").send_keys("12/01/2017")
    elem = driver.find_element_by_id("ctl00_MainContent_btnSavePrice").click()
    element = driver.find_element_by_id("ctl00_MainContent_Feedback2_lblMessage")
    assert element.text == "A new pricing record has been added for Commonwealth Edison" 

    elem = driver.find_element_by_id("ctl00_MainContent_lbCustGroup").click()
    elem = driver.find_element_by_id("ctl00_MainContent_txtCustGroupVal").send_keys("1.00")
    elem = driver.find_element_by_id("ctl00_MainContent_btnAddCustGroup").click()
    element = driver.find_element_by_id("ctl00_MainContent_Feedback2_lblMessage")
    assert element.text == "A new pricing group has been added"

    elem = driver.find_element_by_id("ctl00_MainContent_lbPricingCode").click()
    elem = driver.find_element_by_id("ctl00_MainContent_txtInternalName").send_keys("asdf")
    elem = driver.find_element_by_id("ctl00_MainContent_ddlCustomerGroup")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text.strip() == ("00003 /"):
            option.click()
            time.sleep(3)
    element = driver.find_element_by_id("ctl00_MainContent_Feedback2_lblMessage")
    assert element.text == "A New pricing code has been added"



