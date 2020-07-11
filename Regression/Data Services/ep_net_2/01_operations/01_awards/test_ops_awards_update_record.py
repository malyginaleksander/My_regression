from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'tc_description', 'benId'])

award = [
    ['tc-01', 'Update Record', 'Id'],
]

award_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
    	    benId = current_row[2],
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

@pytest.mark.parametrize("payload", award_data, ids=[
    p.tc.lower() for p in award_data
])
def test_awards(driver, payload):
    print(payload.tc, ' - ', payload.tc_description)

    driver.get("http://epnet2.pt.nrgpl.us/awards")
    time.sleep(7)
    driver.implicitly_wait(10)
    elem = driver.find_element_by_id("Id").send_keys("549951")
    elem = driver.find_element_by_id("awardsSearchButton").click()
    driver.implicitly_wait(10)
    elem = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[1]").click() #click row
    elem = driver.find_element_by_id("edit_awardsGrid").click() #edit
    elem = driver.find_element_by_id("TypeofBenefit").send_keys(Keys.CONTROL, "a");
    elem = driver.find_element_by_id("TypeofBenefit").send_keys(Keys.DELETE);
    elem = driver.find_element_by_id("TypeofBenefit").send_keys("MILES")
    elem = driver.find_element_by_id("sData").click()
    elem = driver.find_element_by_id("cData").click()
    driver.get("http://epnet2.pt.nrgpl.us/awards")
    elem = driver.find_element_by_id("awardsSearchButton").click()
    elem = driver.find_element_by_id("Id").send_keys("549951")
    elem = driver.find_element_by_id("awardsSearchButton").click()
    driver.implicitly_wait(10)
    element = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]")
    assert element.text == ("MILES")