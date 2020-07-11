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

quarter = [
    ['tc-01'],
]

quarter_data = [
    Payload(tc = current_row[0],
            )
    for current_row in quarter
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

@pytest.mark.parametrize("payload", quarter_data, ids=[
    p.tc.lower() for p in quarter_data
])
def test_quarter(driver, payload):
    print(payload.tc, ' - ', 'Process a Quarter')

    driver.get("http://epnet2.pt.nrgpl.us/ChannelPartnerReporting#process-quarter")
    driver.implicitly_wait(30)

    elem = driver.find_element_by_id("ProcessQuarterId")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == ("Quarter 3 2016"):
            option.click()
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[6]/form/fieldset/div/input").click()
    time.sleep(5)
    element = driver.find_element_by_id("info")
    assert "successfully" in driver.page_source