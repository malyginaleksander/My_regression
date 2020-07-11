from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc', 'page', 'zipcode', 'expected_plan_page', 'expected_compare_page_1'])

zipcode = [
    ['tc-01', 'http://www.pt.nrghomepower.com/', '19030', "We're showing Electric plans for", "2 plans"],
]

zipcode_data = [
    Payload(tc = current_row[0],
            page = current_row[1],
            zipcode = current_row[2],
            expected_plan_page = current_row[3],
            expected_compare_page_1 = current_row[4],
            )
    for current_row in zipcode
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

@pytest.mark.parametrize("payload", zipcode_data, ids=[
    p.tc.lower() for p in zipcode_data
])
def test_state(driver, payload):
    print(payload.tc, 'NRG_regression WEB Compare checkbox check')

    driver.get(payload.page)
    driver.maximize_window()
    driver.implicitly_wait(13)

    elem = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/form/div/input").send_keys(payload.zipcode)
    elem = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[1]/form/div/button").click() #shop now button

    assert  payload.expected_plan_page in driver.page_source # plans page


    driver.find_element_by_xpath(".//*[@id='plan-utility-header-electric']/div/div/a").click()
    driver.find_element_by_xpath(".//*[@id='plan-utility-header-electric']/div/div/div/a[1]").click()

    #elem = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[5]/div[1]/div[2]/div[2]/div/div/div[2]/label").click() #Learn and conserve compare checkbox


    elem = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[5]/div[1]/div[1]/div[2]/div/div/div[2]/label").click() #cash back compare checkbox
    time.sleep(3)

    #elem = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[5]/div[1]/div[2]/div[2]/div/div/div[2]/label").click() #Learn and conserve compare checkbox
    end_tos = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[5]/div[1]/div[2]/div[2]/div/div/div[2]/label")
    driver.execute_script("return arguments[0].scrollIntoView();", end_tos)

    elem = driver.find_element_by_xpath("//div//div//div//label[contains(text(),'Compare')]").click() #Learn and conserve compare checkbox

    assert driver.find_element_by_class_name("plans-to-compare").is_displayed()


    elem = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[5]/div[2]/button").click() #compare button

    assert driver.current_url == "https://www.pt.nrghomepower.com/plans/pa/"
    assert payload.expected_compare_page_1 in driver.page_source

    elem = driver.find_element_by_class_name("compare-back-btn").click()
    assert driver.current_url == "https://www.pt.nrghomepower.com/plans/pa/#"


