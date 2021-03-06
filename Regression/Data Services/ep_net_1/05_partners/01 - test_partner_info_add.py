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

partner = [
    ['tc-01']
]

partner_data = [
    Payload(tc = current_row[0],
            )
    for current_row in partner
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

@pytest.mark.parametrize("payload", partner_data, ids=[
    p.tc.lower() for p in partner_data
])
def test_partner(driver, payload):
    print(payload.tc, ' - Add Partner')

    driver.get("http://epnet1.pt.nrgpl.us/Partners/PartnerMaintenance.aspx")
    driver.implicitly_wait(10)

    elem = driver.find_element_by_id("ctl00_MainContent_btnAddNew").click()
    elem = driver.find_element_by_id("ctl00_MainContent_gvPartners_ctl02_ddlPartnerType")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == ("Co-Branded"):
            option.click()	
    elem = driver.find_element_by_name("ctl00$MainContent$gvPartners$ctl02$ctl00").send_keys("AAL2")
    elem = driver.find_element_by_id("ctl00_MainContent_gvPartners_ctl02_txtPartnerName").send_keys("American Test1")
    elem = driver.find_element_by_name("ctl00$MainContent$gvPartners$ctl02$ctl01").send_keys("AAL2")
    elem = driver.find_element_by_name("ctl00$MainContent$gvPartners$ctl02$ctl02").send_keys("www.test.com")
    elem = driver.find_element_by_id("ctl00_MainContent_gvPartners_ctl02_txtMemberCount").send_keys("6000")
    elem = driver.find_element_by_id("ctl00_MainContent_gvPartners_ctl02_txtAvgMemKwh").send_keys("1000")
    elem = driver.find_element_by_id("ctl00_MainContent_gvPartners_ctl02_txtPartnerPaymentSchedule").send_keys("CQ")
    elem = driver.find_element_by_id("ctl00_MainContent_gvPartners_ctl02_ddlDefaultAwardValueType")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == ("Cash"):
            option.click()	
    elem = driver.find_element_by_id("ctl00_MainContent_gvPartners_ctl02_UpdateButton").click()

    assert "AAL2" in driver.page_source