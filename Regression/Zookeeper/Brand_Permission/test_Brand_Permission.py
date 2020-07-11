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

brand = [
    ['tc-01']
]

brand_data = [
    Payload(tc = current_row[0],
            )
    for current_row in brand
]

@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('USE_PHANTOM'):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(1120, 550)
    else:
        print("making Firefox driver")
        _driver = webdriver.Firefox()
        _driver.set_window_size(1320, 750)

    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            _driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver

@pytest.mark.parametrize("payload", brand_data, ids=[
    p.tc.lower() for p in brand_data
])
def test_state(driver, payload):
    print(payload.tc, 'Zookeeper Brand Permissions check')

    #Zookeeper Clear Brand
    driver.get("http://www.pt.energypluscompany.com/newadmin/login.php")
    driver.implicitly_wait(30)

    elem = driver.find_element_by_name("loginusername").send_keys("mpeters")
    elem = driver.find_element_by_name("loginpassword").send_keys("energy")
    elem = driver.find_element_by_class_name("btn").click()
    time.sleep(2)

    elem = driver.find_element_by_xpath("/html/body/div[4]/div[4]/div[2]/ul/li[4]/a").click()
    time.sleep(5)
    elem = driver.find_element_by_id("prependedInput").send_keys("michael peters")
    elem = driver.find_element_by_id("374").click()
    time.sleep(2)
    elem = driver.find_element_by_name("brand_permissions_green_mountain_energy").click()
    elem = driver.find_element_by_id("save_button").click()
    time.sleep(2)

    #Inbound Check Brand
    driver.get("http://www.pt.energypluscompany.com/myinbound/login.php")
    driver.implicitly_wait(30)

    #login
    elem = driver.find_element_by_name("email").send_keys('mpeters@energypluscompany.com')
    elem = driver.find_element_by_name("password").send_keys('energy')
    elem = driver.find_element_by_id("button").click()
    time.sleep(2)

    if len(driver.find_elements_by_id('brandId_5')) > 0:
        print("Brand Permission - Failed")
    else:
        print("Brand Permission - Passed")    

    #Zookeeper set Brand
    driver.get("http://www.pt.energypluscompany.com/newadmin/login.php")
    driver.implicitly_wait(30)

    elem = driver.find_element_by_name("loginusername").send_keys("mpeters")
    elem = driver.find_element_by_name("loginpassword").send_keys("energy")
    elem = driver.find_element_by_class_name("btn").click()
    time.sleep(2)

    elem = driver.find_element_by_xpath("/html/body/div[4]/div[4]/div[2]/ul/li[4]/a").click()
    time.sleep(5)
    elem = driver.find_element_by_id("prependedInput").send_keys("michael peters")
    elem = driver.find_element_by_id("374").click()
    time.sleep(2)
    elem = driver.find_element_by_name("brand_permissions_green_mountain_energy").click()
    elem = driver.find_element_by_id("save_button").click()
    time.sleep(2)