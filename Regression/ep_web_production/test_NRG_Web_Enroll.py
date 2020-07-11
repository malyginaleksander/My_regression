from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'url', 'first_name', 'last_name', 'email_addr', 'confirm_email_addr', 
'Service_Address1', 'city', 'zipcode', 'Service_phone_number', 'accountNo', 'utility'])

local_path = './ep_web_production/prod_data.xlsx'
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('NRG_regression Web Enroll')

state_data = [
    Payload(tc = worksheet.row(current_row)[0].value,
    url = worksheet.row(current_row)[1].value,
    first_name = worksheet.row(current_row)[2].value,
    last_name = worksheet.row(current_row)[3].value,
    email_addr = worksheet.row(current_row)[4].value,
    confirm_email_addr = worksheet.row(current_row)[5].value,
    Service_Address1 = worksheet.row(current_row)[6].value,
    city = worksheet.row(current_row)[7].value,
    zipcode = worksheet.row(current_row)[8].value,
    Service_phone_number = str(worksheet.row(current_row)[9].value),
    utility = worksheet.row(current_row)[10].value,
    accountNo = worksheet.row(current_row)[11].value,
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

@pytest.mark.parametrize("payload", state_data, ids=[
    p.tc.lower() for p in state_data
])
def test_state(driver, payload):
    print(payload.tc, 'NRG_regression WEB Electric Production Enrollment - Utility = ', payload.utility)

    driver.get(payload.url)
    driver.implicitly_wait(30)

    elem = driver.find_element_by_xpath("/html/body/div/div[2]/center[2]/span/a/img").click()
    time.sleep(2)    

    ## Personal Information
    elem = driver.find_element_by_id("id_first_name").send_keys(payload.first_name)
    elem = driver.find_element_by_id("id_last_name").send_keys(payload.last_name)
    elem = driver.find_element_by_id("id_email").send_keys(payload.email_addr)
    elem = driver.find_element_by_id("id_ver_email").send_keys(payload.confirm_email_addr)
    elem = driver.find_element_by_id("id_phone").send_keys(payload.Service_phone_number)
    elem = driver.find_element_by_id("id_service_address_1").send_keys(payload.Service_Address1)
    elem = driver.find_element_by_id("id_service_address_city").send_keys(payload.city)
    elem = driver.find_element_by_id("id_service_address_zip").send_keys(payload.zipcode)
    time.sleep(2)
    
    elem = driver.find_element_by_name("electric-utility_slug")
    if elem.is_displayed():
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == payload.utility:
                option.click()
                break  

    elem = driver.find_element_by_id("id_electric-uan").send_keys(payload.accountNo)
    
    try:
        elem = driver.find_element_by_id("id_electric-billing_uan").send_keys(payload.accountNo)
    except:
        pass    
    time.sleep(2)
    elem = driver.find_element_by_id("continue-submit").click()
    time.sleep(4)

    ## Verification
    elem = driver.find_element_by_class_name("tos-section").send_keys(Keys.CONTROL, Keys.ARROW_DOWN);
    elem = driver.find_element_by_class_name("tos-section").send_keys(Keys.CONTROL, Keys.ARROW_DOWN);
    elem = driver.find_element_by_class_name("tos-section").send_keys(Keys.CONTROL, Keys.ARROW_DOWN);
    elem = driver.find_element_by_class_name("tos-section").send_keys(Keys.CONTROL, Keys.ARROW_DOWN);
    elem = driver.find_element_by_class_name("tos-section").send_keys(Keys.CONTROL, Keys.ARROW_DOWN);
    elem = driver.find_element_by_class_name("tos-section").send_keys(Keys.CONTROL, Keys.ARROW_DOWN);        
    elem = driver.find_element_by_id("id_order_authorization").click()

    if driver.find_element_by_id("id_affiliate_consent").is_displayed():
        driver.find_element_by_id("id_affiliate_consent").click()

    elem = driver.find_element_by_id("agree").click()

    ## Grab Conformation Code
    time.sleep(2)
    elem = driver.find_element_by_id("confirmation")
    confirmation = elem.text
    print("Confirmation =  " +confirmation)
