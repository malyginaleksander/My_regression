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

marketers = [
    ['tc-01'],
]

marketers_data = [
    Payload(tc = current_row[0],
            )
    for current_row in marketers
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

@pytest.mark.parametrize("payload", marketers_data, ids=[
    p.tc.lower() for p in marketers_data
])
def test_marketers(driver, payload):
    print(payload.tc, ' - ', 'Add marketer')

    driver.get("http://epnet2.pt.nrgpl.us/MarketingDataServices/MarketersIndex")
    driver.implicitly_wait(10)
    elem = driver.find_element_by_id("btnAddMarketer").click()
    time.sleep(5)
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/select").send_keys(Keys.TAB);
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/select")
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td/table/tbody/tr[1]/td/input").send_keys("5152")
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td/table/tbody/tr[1]/td/input").send_keys(Keys.TAB);
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/select").send_keys(Keys.ARROW_DOWN);
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/select").send_keys(Keys.TAB);
    time.sleep(2)
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td/table/tbody/tr[2]/td/select").send_keys(Keys.TAB);
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div[3]/div/div/table/tbody/tr[1]/td/table/tbody/tr[3]/td/input").send_keys("vh")
    elem = driver.find_element_by_id("btnAddMarketerSubmit").click()
    time.sleep(3)
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div[2]/i").click()
    time.sleep(2)
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]").click()
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[1]/div[1]").click()
    driver.implicitly_wait(5)
    time.sleep(5)
    assert "5152" in driver.page_source
    elem = driver.close