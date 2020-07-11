from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple
from selenium.webdriver.common.action_chains import ActionChains

Payload = namedtuple('payload', ['tc', 'tc_description', 'field', 'expected_xpath', 'entered_text', 'expected_text'])

missing = [
    ['tc-01', 'filter Admin Missing Utility Codes by Utility Account Number', 'gs_UtilityAccountNumber', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]', '3427591181', '3427591181'],
    ['tc-02', 'filter Admin Missing Utility Codes by Last Name', 'gs_LastName', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]', 'BOULDIN', 'BOULDIN'],
    ['tc-03', 'filter Admin Missing Utility Codes by First Name', 'gs_FirstName', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]', 'SHAHANA', 'SHAHANA'],
    ['tc-04', 'filter Admin Missing Utility Codes by VIP', 'gs_Vip', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]', '018', '018'],
    ['tc-05', 'filter Admin Missing Utility Codes by SPL', 'gs_Spl', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]', 'KNY', 'KNY'],
    ['tc-06', 'filter Admin Missing Utility Codes by Revenue Class', 'gs_RevenueClass', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[9]', '1', '1'],
    ['tc-07', 'filter Admin Missing Utility Codes by Partner Code', 'gs_PartnerCode', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]', 'NRR', 'NRR'],
    ['tc-08', 'filter Admin Missing Utility Codes by Utility Billing City', 'gs_UtilityBillingCity', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[14]', 'BAYSIDE', 'BAYSIDE'],
    ['tc-09', 'filter Admin Missing Utility Codes by Utility Billing State', 'gs_UtilityBillingSt', '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[15]', 'PA', 'PA'],
]

missing_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
            field = current_row[2],
            expected_xpath = current_row[3],
            entered_text = current_row[4],
            expected_text = current_row[5],
            )
    for current_row in missing
]

@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('BUILD_ID', None):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(1820, 550)
    else:
        print("making Firefox driver")
        #_driver = webdriver.Firefox()
        _driver = webdriver.Chrome('C:\Python34\chromedriver.exe')
        _driver.set_window_size(1800, 1550)
        
    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            _driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver

@pytest.mark.parametrize("payload", missing_data, ids=[
    p.tc.lower() for p in missing_data
])
def test_awards(driver, payload):
    print(payload.tc, ' - ', payload.tc_description)

    driver.get("http://epnet2.pt.nrgpl.us/Pricing#admin")
    driver.implicitly_wait(10)
    time.sleep(1)
    elem = driver.find_element_by_id("pricingAdminComboBox").click()
    elem = driver.find_element_by_id("pricingAdminComboBox").send_keys(Keys.ARROW_DOWN);
    elem = driver.find_element_by_id("pricingAdminComboBox").send_keys(Keys.ARROW_DOWN);
    elem = driver.find_element_by_id("pricingAdminComboBox").send_keys(Keys.ARROW_DOWN);
    elem = driver.find_element_by_id("pricingAdminComboBox").send_keys(Keys.ARROW_DOWN);
    elem = driver.find_element_by_id("pricingAdminComboBox").send_keys(Keys.ARROW_DOWN);
    elem = driver.find_element_by_id("pricingAdminComboBox").send_keys(Keys.ARROW_DOWN);
    elem = driver.find_element_by_id("pricingAdminComboBox").send_keys(Keys.ARROW_DOWN);
    elem = driver.find_element_by_id("pricingAdminComboBox").send_keys(Keys.ARROW_DOWN);
    elem = driver.find_element_by_id("pricingAdminComboBox").send_keys(Keys.ENTER);
    driver.implicitly_wait(10)
    elem = driver.find_element_by_id(payload.field).send_keys(payload.entered_text)
    elem = driver.find_element_by_id(payload.field).send_keys(Keys.ENTER);
    element = driver.find_element_by_xpath(payload.expected_xpath)
    assert element.text == (payload.expected_text)
    assert "Unexpected Error" not in driver.page_source 