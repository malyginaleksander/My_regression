from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import xlrd
import os
import pytest
from Regression import config
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'source_phone', 'brand', 'state', 'sop', 'is_sop'])

local_path = "./Inbound/800_Enrollment/s4_enrollment_data.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('call info')

call_data = [
    Payload(tc = worksheet.row(current_row)[0].value,
    source_phone = worksheet.row(current_row)[1].value,
    brand = worksheet.row(current_row)[2].value,
    state = worksheet.row(current_row)[3].value,
    sop = worksheet.row(current_row)[4].value,
    is_sop = worksheet.row(current_row)[5].value,
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

    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            _driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver

@pytest.mark.parametrize("payload", call_data, ids=[
    p.tc.lower() for p in call_data
])
def test_state(driver, payload):
    print(payload.tc, ' - Brand =', payload.brand, ' - expected state dropdown results = ',payload.state, '- is SOP = ', payload.is_sop)    

    driver.get(config.INBOUND_RESETSESSION_URL)
    driver.get(config.INBOUND_LOGIN_URL)

    #login
    elem = driver.find_element_by_name("email").send_keys(config.INBOUND_LOGIN_EMAIL)
    elem = driver.find_element_by_name("password").send_keys(config.INBOUND_LOGIN_PASSWORD)
    elem = driver.find_element_by_id("button").click()
    time.sleep(2)

    driver.get("http://www.pt.energypluscompany.com/ajax/services/rdi/testcall.php")
    elem = driver.find_element_by_id("source_phone").send_keys(Keys.CONTROL, "a");
    elem = driver.find_element_by_id("source_phone").send_keys(Keys.DELETE);
    elem = driver.find_element_by_id("source_phone").send_keys(payload.source_phone)
    elem = driver.find_element_by_xpath("/html/body/form/div[19]/input").click() #Submit - S4 way button
    time.sleep(1)
    
    assert payload.brand in driver.page_source

    elem = driver.find_element_by_name("state-list")
    for option in elem.find_elements_by_tag_name('selected_option'):
        assert selected_option.text == payload.state

    assert driver.find_element_by_class_name(payload.sop).is_displayed()
