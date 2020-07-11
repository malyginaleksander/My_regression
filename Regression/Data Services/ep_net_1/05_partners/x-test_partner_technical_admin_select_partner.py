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

technical = [
    ['tc-01'],
]

technical_data = [
    Payload(tc = current_row[0],
            )
    for current_row in technical
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

@pytest.mark.parametrize("payload", technical_data, ids=[
    p.tc.lower() for p in technical_data
])
def test_technical(driver, payload):
    print(payload.tc, ' - ', 'Select Partner')

    driver.get("http://epnet1.pt.nrgpl.us/Partners/PartnerTechnicalAdministration.aspx")
    driver.implicitly_wait(10)
    
    elem = driver.find_element_by_id("ctl00_MainContent_ucPartnerFileAdministrationSearch_ucPartnerSelectionDropDownList_ddlPartner")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == "(AAL) American Airlines":
            option.click()
            time.sleep(10)
    
    driver.switch_to_window(driver.window_handles[1])

    elem = driver.find_element_by_id('menucontainer').send_keys(Keys.TAB);


    elem = driver.find_element_by_id('ctl00_MainContent_ucPartnerFileAdministrationSearch_gvFileLayouts_ctl02_lBtnViewDetails'),click()