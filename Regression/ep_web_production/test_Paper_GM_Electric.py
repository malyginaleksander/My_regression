from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'brand', 'first_name', 'last_name', 'address', 'city', 'state', 'zipcode', 'area_code', 
    'prefix', 'last', 'email', 'spanish', 'utility', 'account_number', 'rate_class', 'zone', 'product'])

local_path = './ep_web_production/prod_data.xlsx'
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('Paper GM')

paper_data = [
    Payload(tc = worksheet.row(current_row)[0].value,
    brand = worksheet.row(current_row)[1].value,
    first_name = worksheet.row(current_row)[2].value,
    last_name = worksheet.row(current_row)[3].value,
    address = worksheet.row(current_row)[4].value,
    city = worksheet.row(current_row)[5].value,
    state = worksheet.row(current_row)[6].value,
    zipcode = worksheet.row(current_row)[7].value,
    area_code = worksheet.row(current_row)[8].value,
    prefix = str(worksheet.row(current_row)[9].value),
    last = str(worksheet.row(current_row)[10].value),
    email = worksheet.row(current_row)[11].value,
    spanish = worksheet.row(current_row)[12].value,
    utility = worksheet.row(current_row)[13].value,
    account_number = str(worksheet.row(current_row)[14].value),
    rate_class = worksheet.row(current_row)[15].value,
    zone = worksheet.row(current_row)[16].value,
    product = worksheet.row(current_row)[17].value,
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

@pytest.mark.parametrize("payload", paper_data, ids=[
    p.tc.lower() for p in paper_data
])
def test_state(driver, payload):
    print(payload.tc, 'Production Paper App, Brand = GME, Type = Electric - ', 'state =', payload.state, '- utility =', payload.utility)

    driver.get("http://www.pt.energypluscompany.com/myinbound/login.php")
    driver.implicitly_wait(30)

   #login
    elem = driver.find_element_by_name("email").send_keys("mpeters@energypluscompany.com")
    elem = driver.find_element_by_name("password").send_keys("energy")
    elem = driver.find_element_by_id("button").click()
    time.sleep(2)

    driver.get("http://www.pt.energypluscompany.com/myinbound/paper.php")
    time.sleep(2)

    elem = driver.find_element_by_id(payload.brand).click()
    time.sleep(3)

    #Customer Information
    elem = driver.find_element_by_name("customer_first_name").send_keys(payload.first_name)
    elem = driver.find_element_by_name("customer_last_name").send_keys(payload.last_name)
    elem = driver.find_element_by_name("customer_address1").send_keys(payload.address)
    elem = driver.find_element_by_name("customer_city").send_keys(payload.city)
    elem = driver.find_element_by_name("customer_state")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == payload.state:
            option.click()
    elem = driver.find_element_by_name("customer_zip5").send_keys(payload.zipcode)
    elem = driver.find_element_by_name("customer_area_code").send_keys(payload.area_code)
    elem = driver.find_element_by_name("customer_prefix").send_keys(payload.prefix)
    elem = driver.find_element_by_name("customer_line_number").clear()
    elem = driver.find_element_by_name("customer_line_number").send_keys(payload.last)

    elem = driver.find_element_by_name("account_type")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == ("Residential"):
            option.click()
    time.sleep(1)
    
    #Billing Information
    elem = driver.find_element_by_name("copyinfo").click()
    elem = driver.find_element_by_name("email").send_keys(payload.email)

    #Electric
    elem = driver.find_element_by_name("electric_utility")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == payload.utility:
            option.click()
    elem = driver.find_element_by_name("electric_account_number").send_keys(payload.account_number)
    if driver.find_element_by_name("electric_extra_account_number").is_displayed():
        element = driver.find_element_by_name("electric_extra_account_number").send_keys(payload.service_ref)
    if driver.find_element_by_name("coned_zone").is_displayed():
        element = driver.find_element_by_name("coned_zone").click()
    if  driver.find_element_by_name("spanishbill").is_displayed():	
        elememt = driver.find_element_by_name("spanishbill").click()
 
    #Order Information
    time.sleep(4)
    elem = driver.find_element_by_name("electric_products_gme")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == payload.product:
    	    option.click()

    #Vendor ID
    elem = driver.find_element_by_name("vendor_id")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == ("EPIB"):
            option.click()

    # Grab Conformation Code
    elem = driver.find_element_by_name("confCode")
    confCode = elem.text
    print("Confirmation = " +confCode)

    elem = driver.find_element_by_name("submit").click()
