from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'partner', 'number', 'expected'])

local_path = "./Zookeeper/checksum/checksum.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('checksum')

checksum_data = [
    Payload(tc = worksheet.row(current_row)[0].value,
    partner = worksheet.row(current_row)[1].value,
    number = worksheet.row(current_row)[2].value,
    expected = worksheet.row(current_row)[3].value,
    )
for current_row in range(1,worksheet.nrows)
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
        _driver.set_window_size(1300, 700)

    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            _driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver

@pytest.mark.parametrize("payload", checksum_data, ids=[
    p.tc.lower() for p in checksum_data
])
def test_state(driver, payload):
    print(payload.tc, ' - ', payload.partner, ' - ', payload.number, ' - ', payload.expected)

    ## Zookeeper Log in
    driver.get("http://www.pt.energypluscompany.com/newadmin/login.php")
    elem = driver.find_element_by_name("loginusername").send_keys("mpeters")
    elem = driver.find_element_by_name("loginpassword").send_keys("energy")
    elem = driver.find_element_by_class_name("btn").click()
    time.sleep(2)
    driver.get("http://www.pt.energypluscompany.com/newadmin/partner_checksums.php")

    ## Checksum
    elem = driver.find_element_by_id(payload.partner).click()
    time.sleep(2)
    elem = driver.find_element_by_id("partner_member_number").send_keys(payload.number)
    elem = driver.find_element_by_id("checkNumber").click()
    time.sleep(2)

    assert len(driver.find_elements_by_class_name(payload.expected)) >0

    elem = driver.find_element_by_id("partner_member_number").send_keys(Keys.CONTROL, "a");
    elem = driver.find_element_by_id("partner_member_number").send_keys(Keys.DELETE);
