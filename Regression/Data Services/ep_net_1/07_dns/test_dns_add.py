from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc'])

dns = [
    ['tc-01']
]

dns_data = [
    Payload(tc = current_row[0],
            )
    for current_row in dns
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

@pytest.mark.parametrize("payload", dns_data, ids=[
    p.tc.lower() for p in dns_data
])
def test_awards(driver, payload):
    print(payload.tc, ' - DNS')

    driver.get("http://epnet2.pt.nrgpl.us/DNS")
    driver.implicitly_wait(10)
    
    # Add Record
    elem = driver.find_element_by_id("doNotCall").click()
    elem = driver.find_element_by_id("fName").send_keys("33test")
    elem = driver.find_element_by_id("lName").send_keys("33test")
    elem = driver.find_element_by_id("add1").send_keys("123 west st")
    elem = driver.find_element_by_id("cityTxt").send_keys("philadelphia")
    elem = driver.find_element_by_id("dnsFormStates")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == ("PA"):
            option.click()
    elem = driver.find_element_by_id("zip").send_keys("19110")
    elem = driver.find_element_by_id("phoneTxt").send_keys("215-295-8989")
    elem = driver.find_element_by_id("emailTxt").send_keys("test@aol.com")
    elem = driver.find_element_by_id("dnsReasons")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == ("Addressee no longer resides at address"):
            option.click()
    elem = driver.find_element_by_id("brandSlugForDns")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == ("Energy Plus"):
            option.click()
    time.sleep(2)
    elem = driver.find_element_by_id("btnAdd").click()
    time.sleep(4)
    driver.switch_to.alert.accept()