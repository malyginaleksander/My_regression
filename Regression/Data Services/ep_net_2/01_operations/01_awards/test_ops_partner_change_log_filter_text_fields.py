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

partner = [
    ['tc-01', 'filter Partner Change Log by Id', 'gs_Id', '/html/body/div[1]/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]', '147288'],
    ['tc-02', 'filter Partner Change Log by Ben ID', 'gs_BenID', '/html/body/div[1]/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]', '4195991'],
    ['tc-03', 'filter Partner Change Log by Utility Account Number', 'gs_UtilityAccountNumber', '/html/body/div[1]/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]', '629152009'],
    ['tc-04', 'filter Partner Change Log by Member Number', 'gs_MemberID', '/html/body/div[1]/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]', '512040304'],
    ['tc-05', 'filter Partner Change Log by Member Last Name', 'gs_MemberLastName', '/html/body/div[1]/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]', 'WILLIAMS'],
    ['tc-06', 'filter Partner Change Log by Member First Name', 'gs_MemberFirstName', '/html/body/div[1]/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[8]', 'Yoel'],
    ['tc-07', 'filter Partner Change Log by Partner Member Number', 'gs_PartnerMemberNumber', '/html/body/div[1]/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[9]', '2428534966'],
    ['tc-08', 'filter Partner Change Log by Partner Last Name', 'gs_PartnerLastName', '/html/body/div[1]/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]', "NEWMAN"],
    ['tc-09', 'filter Partner Change Log by Partner First Name', 'gs_PartnerFirstName', '/html/body/div[1]/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[11]', "SANDRA"],
    ['tc-10', 'filter Partner Change Log by NY', 'gs_AwardID', '/html/body/div[1]/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[12]', "1591514"],
]

partner_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
    	    field = current_row[2],
    	    expected_xpath = current_row[3],
    	    expected_text = current_row[4],
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

@pytest.mark.parametrize("payload", partner_data, ids=[
    p.tc.lower() for p in partner_data
])
def test_awards(driver, payload):
    print(payload.tc, ' - ', payload.tc_description)

    driver.get("http://epnet2.pt.nrgpl.us/awards#partner_change_log")
    driver.implicitly_wait(10)

    elem = driver.find_element_by_id(payload.field).send_keys(payload.expected_text)
    elem = driver.find_element_by_id(payload.field).send_keys(Keys.ENTER);
    element = driver.find_element_by_xpath(payload.expected_xpath)
    assert element.text == (payload.expected_text)
    assert "Unexpected Error" not in driver.page_source