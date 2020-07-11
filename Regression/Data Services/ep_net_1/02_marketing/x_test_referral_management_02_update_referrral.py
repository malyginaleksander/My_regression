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

referral = [
    ['tc-01'],
]

referral_data = [
    Payload(tc = current_row[0],
            )
    for current_row in referral
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

@pytest.mark.parametrize("payload", referral_data, ids=[
    p.tc.lower() for p in referral_data
])
def test_referral(driver, payload):
    print(payload.tc, ' - ', 'Update referral')

    driver.get("http://epnet1.pt.nrgpl.us/Marketing/ReferralManagement.aspx")
    driver.implicitly_wait(10)
    time.sleep(5)
    elem = driver.find_element_by_id("ctl00_MainContent_gvReferrals_ctl02_EditButton").click()
    
    elem = driver.find_element_by_id("ctl00_MainContent_gvReferrals_ctl02_txtBusinessName").send_keys("business name inc")
    elem = driver.find_element_by_id("ctl00_MainContent_gvReferrals_ctl02_txtFirstName").send_keys("n")
    elem = driver.find_element_by_id("ctl00_MainContent_gvReferrals_ctl02_txtLastName").send_keys("s")
    elem = driver.find_element_by_id("ctl00_MainContent_gvReferrals_ctl02_txtAddress").send_keys("123 west")
    elem = driver.find_element_by_id("ctl00_MainContent_gvReferrals_ctl02_txtCity").send_keys("hollywood")
    elem = driver.find_element_by_id("ctl00_MainContent_gvReferrals_ctl02_txtState").send_keys("ca")
    elem = driver.find_element_by_id("ctl00_MainContent_gvReferrals_ctl02_txtZip").send_keys("90210")
    elem = driver.find_element_by_id("ctl00_MainContent_gvReferrals_ctl02_txtPhone").send_keys("7356668869")
    elem = driver.find_element_by_id("ctl00_MainContent_gvReferrals_ctl02_txtEmail").send_keys("m@m.com")
    time.sleep(2)
    elem = driver.find_element_by_id("ctl00_MainContent_gvReferrals_ctl02_UpdateButton").click()
    driver.implicitly_wait(10)
    time.sleep(10)
    elem = driver.close




    driver = webdriver.Chrome('C:\Python34\chromedriver.exe')
    driver.get("http://epnet1.pt.nrgpl.us/Marketing/ReferralManagement.aspx")
    driver.implicitly_wait(10)
    time.sleep(5)
    elem = driver.find_element_by_id("ctl00_MainContent_btnViewAll").click
    time.sleep(10)
    assert "business name inc" in driver.page_source

    elem = driver.close