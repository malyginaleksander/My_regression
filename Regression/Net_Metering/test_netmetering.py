from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'url', 'res_name', 'prime_contact', 'prime_phone', 'prime_email', 
'name', 'address', 'city', 'state', 'zipcode', 'phone', 'email', 'location', 'description', 'mover', 'fuel', 'period', 'contract', 'expected'])

local_path = "./Net_Metering/net_data.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('net')

net_data = [
    Payload(tc = worksheet.row(current_row)[0].value,
    url = worksheet.row(current_row)[1].value,
    res_name = worksheet.row(current_row)[2].value,
    prime_contact = worksheet.row(current_row)[3].value,
    prime_phone = str(worksheet.row(current_row)[4].value),
    prime_email = worksheet.row(current_row)[5].value,
    name = worksheet.row(current_row)[6].value,
    address = worksheet.row(current_row)[7].value,
    city = worksheet.row(current_row)[8].value,
    state = str(worksheet.row(current_row)[9].value),
    zipcode = str(worksheet.row(current_row)[10].value),
    phone = str(worksheet.row(current_row)[11].value),
    email = worksheet.row(current_row)[12].value,
    location = worksheet.row(current_row)[13].value,
    description = worksheet.row(current_row)[14].value,
    mover = worksheet.row(current_row)[15].value,
    fuel = worksheet.row(current_row)[16].value,
    period = worksheet.row(current_row)[17].value,
    contract = worksheet.row(current_row)[18].value,
    expected = worksheet.row(current_row)[19].value,
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

@pytest.mark.parametrize("payload", net_data, ids=[
    p.tc.lower() for p in net_data
])
def test_state(driver, payload):
    print(payload.tc, payload.res_name, ' - ', payload.mover, ' - ', payload.fuel,  ' - ', payload.period, ' - ', payload.contract)

    driver.get(payload.url)
    driver.implicitly_wait(30)

    elem = driver.find_element_by_id("res_name").send_keys(payload.res_name)
    elem = driver.find_element_by_id("res_contact").send_keys(payload.prime_contact)
    elem = driver.find_element_by_id("res_phone").send_keys(payload.prime_phone)
    elem = driver.find_element_by_id("res_email").send_keys(payload.prime_email)
    elem = driver.find_element_by_id("ci_name").send_keys(payload.name)
    elem = driver.find_element_by_id("ci_addr").send_keys(payload.address)
    elem = driver.find_element_by_id("ci_city").send_keys(payload.city)
    elem = driver.find_element_by_id("ci_state").send_keys(payload.state)
    elem = driver.find_element_by_id("ci_zip").send_keys(payload.zipcode)
    elem = driver.find_element_by_id("ci_phone").send_keys(payload.phone)
    elem = driver.find_element_by_id("ci_email").send_keys(payload.email)
    elem = driver.find_element_by_id("nmi_acct").send_keys(payload.location)
    elem = driver.find_element_by_id("same_address").click
    elem = driver.find_element_by_id("nameplate").send_keys(payload.description)
    elem = driver.find_element_by_id(payload.mover)
    elem.click()
    elem = driver.find_element_by_id(payload.fuel)
    elem.click()
    elem = driver.find_element_by_id(payload.period)
    elem.click()
    elem = driver.find_element_by_id(payload.contract)
    elem.click()
    time.sleep(2)
    elem = driver.find_element_by_name("_submit")
    elem.click()

    assert driver.current_url == payload.expected
