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
worksheet = workbook.sheet_by_name('IB GMEX2')

state_data = []
headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    state_data.append(Payload(**value_dict))

	
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

@pytest.mark.parametrize("payload", state_data, ids=[
    p.tc.lower() for p in state_data
])
def test_state(driver, payload):
    print(payload.tc, 'GM Inbound Production Multiple Electric Enrollment - State = ', payload.state, ' - utility = ', payload.utility)

    driver.get("http://www.energypluscompany.com/myinbound/login.php")
    driver.implicitly_wait(30)


    driver.get("http://www.energypluscompany.com/myinbound/login.php")
    driver.implicitly_wait(30)

    energyPlusFill = EnergyPlusPage(driver)

    #login
    energyPlusFill.login(payload)

    ##call process
    energyPlusFill.start_call_GM_electric()

    ### Get Started:
    energyPlusFill.get_started_in_call(payload)

    energyPlusFill.gm_electric_multiple_acct_steps(payload)

    ## Offer:
    energyPlusFill.green_mountain_elec_multiple_offer(payload)

    ## Customer Info:
    energyPlusFill.nrg_multi_electric_customer_info(payload)
    #energyPlusFill.fill_green_mountain_cust_info_2(payload)
    energyPlusFill.fill_green_mountain_elec_cust_info_3_submit(payload)

    ## Billing Info:
    energyPlusFill.billing_Info_Multi_Electric(payload)

    ## Summary:
    energyPlusFill.inbound_Summary()

    ## Disclosure:
    energyPlusFill.GM_elec_disclosure_activity(payload)

    # Grab Conformation Code
    confcode = energyPlusFill.getConfirmCode()
    print("Confirmation = " + confcode)

    ## Submit:
    energyPlusFill.submitEnrollData()
