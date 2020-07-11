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
worksheet = workbook.sheet_by_name('EP NJ Landing')

price_data = []
headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    price_data.append(Payload(**value_dict))

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

@pytest.mark.parametrize("payload", price_data, ids=[p.tc.lower() for p in price_data])

def test_state(driver, payload):
    print(payload.tc, 'Ep Web Production NJ Landing Page Price Check for', payload.utility, payload.price)
 
    # driver.get(payload.url)
    # driver.implicitly_wait(30)

    driver.get("http://www.energypluscompany.com/combined/cashback/nj/?apptype=WE&cellcode=01&campaign=0000&pc=015&pcb=015")
    driver.implicitly_wait(9)
    energyPlusFill = EnergyPlusPage(driver)

    energyPlusFill.ep_nj_check_offer()

    energyPlusFill.ep_nj_landing_page(payload)
