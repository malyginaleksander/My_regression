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

Payload = namedtuple('payload', ['tc', 'tc_description', 'field', 'expected_xpath', 'expected_text'])

batch = [
    ['tc-01', 'filter Batch History by Utility Account Number', 'gs_UtilityAccountNumber', '/html/body/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]', '22701791000'],
    ['tc-02', 'filter Batch History Log by Customer Number', 'gs_CustNo', '/html/body/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]', '1169580'],
    ['tc-03', 'filter Batch History Log by Utility', 'gs_PBR_UtilityCode', '/html/body/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]', '45'],
    ['tc-04', 'filter Batch History Log by Region', 'gs_PBR_SPL', '/html/body/div[1]/div[3]/div/div[1]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]', 'BECO'],
]

batch_data = [
    Payload(tc = current_row[0],
            tc_description = current_row[1],
            field = current_row[2],
            expected_xpath = current_row[3],
            expected_text = current_row[4],
            )
    for current_row in batch
]


@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('BUILD_ID', None):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(1120, 550)
    else:
        print("making Firefox driver")
        #_driver = webdriver.Firefox()
        _driver = webdriver.Chrome('C:\Python34\chromedriver.exe')
        _driver.set_window_size(1600, 1150)
        
    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            _driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver

@pytest.mark.parametrize("payload", batch_data, ids=[
    p.tc.lower() for p in batch_data
])
def test_awards(driver, payload):
    print(payload.tc, ' - ', payload.tc_description)

    driver.get("http://epnet2.pt.nrgpl.us/Pricing#batch-history")
    driver.implicitly_wait(10)
    time.sleep(5)
    elem = driver.find_element_by_id("priceBatchHistorySelector").click()
    
    N = 15
    actions = ActionChains(driver) 
    for _ in range(N):
        actions = actions.send_keys(Keys.ARROW_DOWN)
    actions.perform()
    elem = driver.find_element_by_id("priceBatchHistorySelector").send_keys(Keys.ARROW_DOWN)
    elem = driver.find_element_by_id("priceBatchHistorySelector").send_keys(Keys.ENTER)
    driver.implicitly_wait(5)

    elem = driver.find_element_by_id(payload.field).send_keys(payload.expected_text)
    elem = driver.find_element_by_id(payload.field).send_keys(Keys.ENTER);
    element = driver.find_element_by_xpath(payload.expected_xpath)
    assert element.text == (payload.expected_text)
    assert "Unexpected Error" not in driver.page_source