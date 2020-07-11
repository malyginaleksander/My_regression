from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from Regression import config
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'header'])

local_path = "./Inbound/FAQ/Regression/faqs_data.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('EP-SOP')

faq_data = [
    Payload(tc = worksheet.row(current_row)[0].value,
    header = worksheet.row(current_row)[1].value,
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
    
@pytest.mark.skipif('os.environ.get("HUDSON_URL")=="http://ci.nrgpl.us:8080/"')
@pytest.mark.parametrize("payload", faq_data, ids=[
    p.tc.lower() for p in faq_data
])
def test_state(driver, payload):
    print(payload.tc, ' - Brand = EP-SOP, FAQ = ', payload.header)

    driver.get(config.INBOUND_LOGIN_URL)

    #login
    elem = driver.find_element_by_name("email").send_keys(config.INBOUND_LOGIN_EMAIL)
    elem = driver.find_element_by_name("password").send_keys(config.INBOUND_LOGIN_PASSWORD)
    elem = driver.find_element_by_id("button").click()

    if  "Start a manual call" in driver.page_source:
        elem = driver.find_element_by_link_text("Start a manual call").click()
        elem = driver.find_element_by_id("phoneNumber").send_keys(config.INBOUND_STARTMANUALCALL_PHONENUMBER)
        elem = driver.find_element_by_id("reason").send_keys(config.INBOUND_STARTMANUALCALL_REASON)
        elem = driver.find_element_by_id("brand_id")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("Energy Plus"):
        	    option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/form/input[3]").click() #Start Call Button
        driver.switch_to.alert.accept()

    else:
        elem = driver.find_element_by_id("brandId_1").click()
        elem = driver.find_element_by_id("btn_continue").click()
    time.sleep(2)

    #Get Started Tab
    elem = driver.find_element_by_id("sop-button").click()
    elem = driver.find_element_by_id("save-and-continue").click()
    time.sleep(2)

    elem = driver.find_element_by_class_name("campaigns")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == "6666 - Rate Class RS - Residential Service":
            option.click()
    elem = driver.find_element_by_class_name("promos-dropdown")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == "000 - PA Standard Offer":
            option.click()
    elem = driver.find_element_by_id("btn_continue").click()
    time.sleep(5)
    elem = driver.find_element_by_link_text("FAQs").click()
    time.sleep(5)

    assert payload.header in driver.page_source
