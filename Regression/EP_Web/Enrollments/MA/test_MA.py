from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
import os
import pytest
from openpyxl import load_workbook
from States.EnergyPlusHome import EnergyPlusHome
from States.EnergyPlusEnroll import EnergyPlusEnroll
from PageFactory.ConfirmationPage import ConfirmationPage
from collections import namedtuple

local_path = "./EP_Web/Enrollments/MA/MA_Data.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('MA')

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

@pytest.mark.parametrize("payload", enroll_data, ids=[p.tc for p in enroll_data])
def test_state(driver, payload):
    print( payload.tc, 'EP Web Massachusetts Enrollment -', 'utility =', payload.LocalUtility,'- account type =', payload.account_type, '- greenopt =', payload.greenopt_check )

    driver.get( payload.site_one )
    EPHome = EnergyPlusHome( driver )

    #EPHome.selectState( payload )
    EPHome.clickEnroll( )

    EPEnroll = EnergyPlusEnroll( driver )

    # personal info fill
    # imp note: fillEnrollDetails() should be updated to use parameter as data dictionary as shown for selectState()
    EPEnroll.fillEnrollDetails(payload,"apt 2a", "boston")

    # Utility Information
    # check gas
    EPEnroll.clickGasNo( payload )

    # Electric  and submission as well
    EPEnroll.fillElectricDetails_EPWeb_MA_MD_NJ_PA(payload, "Less than 10,000 kWh", "No, I'm non-exempt")

    ## Gas  and submission as well
    #EPEnroll.fillGasLTDetails( payload, "123", "July", "No, I'm non-exempt" )

    EPEnroll.submitData()

    # Rewards Information
    EPEnroll.fillRewardsInfo( payload )

    # Submit
    EPEnroll.clickSubmit()
    time.sleep(4)

    # Grab Confirmation Code
    cop = ConfirmationPage( driver )
    confcode = cop.get_ep_confirmcode("confirmationCode")
    time.sleep(4)
    print( "Confirmation code is: " + confcode )
    time.sleep(2)
