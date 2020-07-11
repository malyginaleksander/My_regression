from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'tc_description', 'uan'])

member = [
    ['tc-01', 'No Unexpected Error', '386535599990'],
]

member_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
            uan = current_row[2],
            )
    for current_row in member
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

@pytest.mark.parametrize("payload", member_data, ids=[
    p.tc.lower() for p in member_data
])
def test_member(driver, payload):
    print(payload.tc, ' - ', payload.tc_description)

    # https://energyplus.atlassian.net/browse/PROD-1318

    driver.get("http://epnet2.pt.nrgpl.us/member")
    driver.implicitly_wait(10)

    elem = driver.find_element_by_id("memberFormSearchCriteria").send_keys(payload.uan)
    driver.implicitly_wait(10)
    elem = driver.find_element_by_xpath("/html/body/div/div[3]/div/div/div[4]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]").click()
    time.sleep(10)
    assert "Unexpected Error" not in driver.page_source