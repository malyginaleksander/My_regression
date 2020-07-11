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

Payload = namedtuple('payload', ['tc', 'Dispositions'])

local_path = "./Inbound/Dispositions/disposition_data.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('GM-Log Dispo')

dispo_data = [
    Payload(tc = worksheet.row(current_row)[0].value,
    Dispositions = worksheet.row(current_row)[1].value,
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
@pytest.mark.parametrize("payload", dispo_data, ids=[
    p.tc.lower() for p in dispo_data
])
def test_state(driver, payload):
    print(payload.tc, 'GME Dispo - ', payload.Dispositions)

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
            if option.text == ("Green Mountain Energy"):
        	    option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/form/input[3]").click() #Start Call Button
        driver.switch_to.alert.accept()

    else:
        elem = driver.find_element_by_id("brandId_5").click()
        elem = driver.find_element_by_id("btn_continue").click()
    time.sleep(2)

    elem = driver.find_element_by_id("log-dispo").click()
    time.sleep(2)

    elem = driver.find_element_by_id("log-dispo")
    time.sleep(4)
    elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div/div/div[2]/div[1]/select") #dispo list
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == payload.Dispositions:
            option.click()  	
    time.sleep (1)

    if 	driver.find_element_by_name("dispo-comments").is_displayed():
        time.sleep(1)
        elem = driver.find_element_by_name("dispo-comments").send_keys(config.INBOUND_LOGDISP_DISPOCOMMENTS)
        time.sleep(1)
    else:
        elem = driver.find_element_by_id("dispo-start-new").click()
    elem = driver.find_element_by_id("dispo-start-new").click()
