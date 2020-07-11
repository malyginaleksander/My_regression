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

disable = [
    ['tc-01']
]

disable_data = [
    Payload(tc = current_row[0],
            )
    for current_row in disable
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

@pytest.mark.parametrize("payload", disable_data, ids=[
    p.tc.lower() for p in disable_data
])
def test_state(driver, payload):
    print(payload.tc, 'Zookeeper Disable Partner check')

    #Zookeeper Clear Brand
    driver.get("http://www.pt.energypluscompany.com/newadmin/login.php")
    driver.implicitly_wait(30)

    elem = driver.find_element_by_name("loginusername").send_keys("mpeters")
    elem = driver.find_element_by_name("loginpassword").send_keys("energy")
    elem = driver.find_element_by_class_name("btn").click()
    time.sleep(2)

    ## Disable Partner
    driver.get("http://www.pt.energypluscompany.com/newadmin/partner_management.php")
    time.sleep(2)
    elem = driver.find_element_by_id("state_4").click() #PA
    time.sleep(2)
    elem = driver.find_element_by_id("pid_9440").click() #Virgin America
    time.sleep(2)
    elem = driver.find_element_by_id("partner_status_3").click() #disable
    time.sleep(2)

    elem = driver.find_element_by_id("savePartner").send_keys(Keys.ENTER);
    time.sleep(3)

    ## Verify Partner Does Not Exist
    driver.get("http://www.pt.energypluscompany.com/virginamerica/pa/")

    assert "The offer you are looking for is no longer available." in driver.page_source
    time.sleep(2)
    ## Verify Partner Does Not Exists
    driver.get("http://staging.devepc.com/combined/virginamerica/pa")

    assert "The offer you are looking for is no longer available." in driver.page_source

    # Enable Partner
    driver.get("http://www.pt.energypluscompany.com/newadmin/login.php")
    driver.implicitly_wait(30)

    elem = driver.find_element_by_name("loginusername").send_keys("mpeters")
    elem = driver.find_element_by_name("loginpassword").send_keys("energy")
    elem = driver.find_element_by_class_name("btn").click()
    time.sleep(2)

    ## Activate Partner
    driver.get("http://www.pt.energypluscompany.com/newadmin/partner_management.php")
    time.sleep(2)
    elem = driver.find_element_by_id("state_4").click() #PA
    time.sleep(2)
    elem = driver.find_element_by_id("pid_9440").click() #Virgin America
    time.sleep(2)
    elem = driver.find_element_by_id("partner_status_1").click() #Active
    time.sleep(2)

    elem = driver.find_element_by_id("savePartner").send_keys(Keys.ENTER);
    time.sleep(3)