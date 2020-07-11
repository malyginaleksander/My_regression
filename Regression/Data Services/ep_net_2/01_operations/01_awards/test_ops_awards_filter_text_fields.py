from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'tc_description', 'field', 'expected_xpath', 'expected_text'])

award = [
    ['tc-01', 'filter award by Ben Id', 'gs_Id', '/html/body/div[1]/div[3]/div/div[1]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[1]', '2'],
    ['tc-02', 'filter award by utility account number', 'gs_Acct', '/html/body/div[1]/div[3]/div/div[1]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]', '2333733110'],
    ['tc-03', 'filter award by Account id', 'gs_AccountId', '/html/body/div[1]/div[3]/div/div[1]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]', '34032'],
    ['tc-04', 'filter award by Partner Code', 'gs_PartnerCode', '/html/body/div[1]/div[3]/div/div[1]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]', 'USA'],
    ['tc-05', 'filter award by Promo Code', 'gs_PromoCode', '/html/body/div[1]/div[3]/div/div[1]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]', '004'],
    ['tc-06', 'filter award by Member Number', 'gs_MemNum', '/html/body/div[1]/div[3]/div/div[1]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[8]', 'N232B86'],
    ['tc-07', 'filter award by partner indicator', 'gs_PartnerIndicator', '/html/body/div[1]/div[3]/div/div[1]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[9]', '01'],
    ['tc-08', 'filter award by Benefit', 'gs_TypeofBenefit', '/html/body/div[1]/div[3]/div/div[1]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]', "MILES"],
    ['tc-09', 'filter award by Award Type', 'gs_Award', '/html/body/div[1]/div[3]/div/div[1]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[11]', "CHANGE RATE CLASS"],
    ['tc-10', 'filter award by Miles', 'gs_BenefitMiles', '/html/body/div[1]/div[3]/div/div[1]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[13]', "211"],
    ['tc-11', 'filter award by Invoice Number', 'gs_InvoiceNumber', '/html/body/div[1]/div[3]/div/div[1]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[14]', "0015827373"],
]

award_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
    	    field = current_row[2],
    	    expected_xpath = current_row[3],
    	    expected_text = current_row[4],
            )
    for current_row in award
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
        _driver.set_window_size(1600, 1150)
        
    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            _driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver

@pytest.mark.parametrize("payload", award_data, ids=[
    p.tc.lower() for p in award_data
])
def test_awards(driver, payload):
    print(payload.tc, ' - ', payload.tc_description)

    driver.get("http://epnet2.pt.nrgpl.us/awards")
    driver.implicitly_wait(10)
    elem = driver.find_element_by_id("awardsSearchButton").click()
    driver.implicitly_wait(10)

    elem = driver.find_element_by_id(payload.field).send_keys(payload.expected_text)
    elem = driver.find_element_by_id(payload.field).send_keys(Keys.ENTER);
    element = driver.find_element_by_xpath(payload.expected_xpath)
    assert element.text == (payload.expected_text)
    assert "Unexpected Error" not in driver.page_source
    elem = driver.find_element_by_id(payload.field).send_keys(Keys.CONTROL, "a");
    elem = driver.find_element_by_id(payload.field).send_keys(Keys.DELETE);