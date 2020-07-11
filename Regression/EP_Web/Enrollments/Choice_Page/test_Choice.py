from __future__ import print_function
from PageFactory.ConfirmationPage import ConfirmationPage
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
from selenium import webdriver
import time
import os
import pytest
from openpyxl import load_workbook
from States.EnergyPlusHome import EnergyPlusHome
from States.EnergyPlusEnroll import EnergyPlusEnroll
from collections import namedtuple

local_path = "./EP_Web/Enrollments/Choice_Page/Choice_Data.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('Choice')

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
    print(payload.tc, 'EP Web Page Choice Page Enrollment - ', payload.state, ' - ', payload.LocalUtility)

    driver.get("http://www.pt.energypluscompany.com/sywr/choice/")
    EPHome = EnergyPlusHome(driver)
    EPHome.selectState(payload)
    EPHome.clickEnroll( )


    EPEnroll = EnergyPlusEnroll(driver)
    # personal info fill
    EPEnroll.fillEnrollDetails(payload,"apt 2a",payload.Service_City)


    # Utility Information
    # check gas
    EPEnroll.clickGasNo(payload)

    # Electric  and submission as well
    EPEnroll.fillElectricDetails_EPWeb_ChoicePage(payload)

    ## Gas  and submission as well
    #EPEnroll.fillGasLTDetails(payload, "123", "July","No, I'm non-exempt")

    EPEnroll.submitData()

    # Rewards Information
    EPEnroll.fillRewardsInfo(payload)

    # Submit
    EPEnroll.clickSubmit()

    # Grab Conformation Code
    cop = ConfirmationPage(driver)
    confcode = cop.get_ep_confirmcode("confirmationCode")
    print("Confirmation code is: " + confcode)
