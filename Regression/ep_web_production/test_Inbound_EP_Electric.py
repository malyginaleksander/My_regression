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
worksheet = workbook.sheet_by_name('IB-EP')

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
    print(payload.tc, 'EP Inbound Production Electric Enrollment - State = ', payload.state, ' - utility = ', payload.utility)

    driver.get("http://www.energypluscompany.com/myinbound/login.php")
    driver.implicitly_wait(15)

    energyPlusFill = EnergyPlusPage(driver)


    #login
    energyPlusFill.login(payload)

    # start manual call
    energyPlusFill.start_call_EP_electric()

    ### Get Started:
    energyPlusFill.get_started_in_call(payload)

    # EP Electric Account steps
    energyPlusFill.inbound_ep_electric_steps(payload)

    ## Offer:
    energyPlusFill.ep_elec_offer1_new(payload)

    ## Customer Info: part 1
    energyPlusFill.customer_info(payload)

    ## Billing Info:
    energyPlusFill.billing_info_Inbound(payload)

    ## Summary:
    energyPlusFill.inbound_Summary()

    # ## Disclosure:
    # elem = driver.find_element_by_id("toggle_1_no").click()
    # elem = driver.find_element_by_id("toggle_2_no").click()

    ## Disclosure:
#   energyPlusFill.disclosure_activity_Inbound_new(payload)
    energyPlusFill.disclosure_toggle()
    energyPlusFill.disclosure_PA1_new(payload)

    # Grab Conformation Code
    confcode = energyPlusFill.getConfirmCode()
    print("Confirmation = " + confcode)

    ## Submit:
    energyPlusFill.submitEnrollData()

