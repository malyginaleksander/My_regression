from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple
from States.EnergyPlusPage import EnergyPlusPage


local_path = './ep_web_production/prod_data.xlsx'
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('Paper NRG_regression Electric')

paper_data = []
headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    paper_data.append(Payload(**value_dict))

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
    print(payload.tc, 'Production Paper App, Brand = NRG_regression, Type = Electric - ', 'state =', payload.state, '- utility =', payload.utility)

    driver.get(payload.url)
    driver.implicitly_wait(30)

    ep_web_production = EnergyPlusPage(driver)
    ep_web_production.login(payload)
    ep_web_production.load_url(payload)
    ep_web_production.fill_cust_info(payload)
    ep_web_production.fill_billing_info_electric(payload)
    ep_web_production.fill_electric_info(payload)
    ep_web_production.fill_order_info_electric(payload)
    ep_web_production.fill_vendor_info(payload)

    confCode = ep_web_production.getConfirmCode()
    print("Confirmation = " + confCode)

    ep_web_production.submitData()
