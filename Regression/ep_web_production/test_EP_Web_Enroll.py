from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import xlrd
import os
import pytest
from collections import namedtuple
from States.EnergyPlusEnroll import EnergyPlusEnroll

local_path = './ep_web_production/prod_data.xlsx'
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('EP Web Enrollment')

enroll_data = []
headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    enroll_data.append(Payload(**value_dict))


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


@pytest.mark.parametrize("payload", enroll_data, ids=[p.tc.lower() for p in enroll_data])
def test_state(driver, payload):
    print(payload.tc, 'EP Web New Jersey Enrollment -', 'utility =', payload.LocalUtility, '- account type =',
          payload.account_type, '- greenopt =', payload.greenopt_check)

    driver.get(payload.site_one)
    driver.implicitly_wait(9)
    elem = driver.find_element_by_link_text("Enroll").click()

    EPEnroll = EnergyPlusEnroll(driver)

    # Personal Information
    EPEnroll.fill_personal_info_EP_web(payload)

    # Utility Information
    # check gas
    EPEnroll.check_gas(payload)

    # Electric
    EPEnroll.fillElectricForEPWeb(payload ,"Less than 10,000 kWh","No, I'm non-exempt")


    ## Gas
   # EPEnroll.fill_Gas_EP_WebEnroll(payload,"123","July","No,I'm non-exempt")

    # submit data
    EPEnroll.submitData()

    #Rewards Information
    EPEnroll.fillRewardsInfo(payload)

    #Submit
    EPEnroll.clickSubmit()


    #Grab Conformation Code
    EPEnroll.EP_Confirmation()
