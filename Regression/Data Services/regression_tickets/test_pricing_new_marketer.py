from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'tc_description', 'marketer_code', 'channel', 'business_name'])

marketer = [
    ['tc-01', 'new marketer is added', '5150', 'Door-to-Door', 'VH'],
]

marketer_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
            marketer_code = current_row[2],
            channel = current_row[3],
            business_name = current_row[4],
            )
    for current_row in marketer
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

@pytest.mark.parametrize("payload", marketer_data, ids=[
    p.tc.lower() for p in marketer_data
])
def test_marketer(driver, payload):
    print(payload.tc, ' - ', payload.tc_description)

    #https://energyplus.atlassian.net/browse/SMALL-2207

    driver.get("http://eppricing.pt.nrgpl.us/DataServices/MarketersIndex")
    driver.implicitly_wait(10)

    elem = driver.find_element_by_id("btnAddMarketer").click()
    time.sleep(5)
    elem = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td/table/tbody/tr[1]/td/input").send_keys("5150")
    elem = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td/table/tbody/tr[1]/td/input").send_keys(Keys.TAB);

    elem = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/select").send_keys(Keys.ARROW_DOWN);
    elem = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/select").send_keys(Keys.TAB);
    time.sleep(2)

    elem = driver.find_element_by_xpath("//html/body/div[3]/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td/table/tbody/tr[3]/td/input").send_keys("vh")
    elem = driver.find_element_by_id("btnAddMarketerSubmit").click()
    time.sleep(3)
    
    elem = driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/div[2]/i").click()
    time.sleep(2)
    elem = driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]").click()
    elem = driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]").click()
    driver.implicitly_wait(5)
    time.sleep(5)
    assert "5150" in driver.page_source
    elem = driver.close