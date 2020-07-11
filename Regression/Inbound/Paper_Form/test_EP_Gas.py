from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple
from Regression import config
from selenium.webdriver.common.by import By


Payload = namedtuple('payload', ['brand', 'first_name','last_name','Address','city','state','zip','area_code','prefix','last','Account_Type','busname',
                                  'email_addr','Utility','Account_Number','partner','campaign','promo','tc'])

local_path = "./Inbound/Paper_Form/Form_Data.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('EP GAS')

enroll_data=[
    Payload(brand = worksheet.row(current_row)[0].value,
    first_name = worksheet.row(current_row)[1].value,
    last_name = worksheet.row(current_row)[2].value,
    Address = worksheet.row(current_row)[3].value,
    city = worksheet.row(current_row)[4].value,
    state = worksheet.row(current_row)[5].value,
    zip = worksheet.row(current_row)[6].value,
    area_code = worksheet.row(current_row)[7].value,
    prefix = worksheet.row(current_row)[8].value,
    last = worksheet.row(current_row)[9].value,
    Account_Type = worksheet.row(current_row)[10].value,
    busname = worksheet.row(current_row)[11].value,
    email_addr = worksheet.row(current_row)[12].value,
    Utility = worksheet.row(current_row)[13].value,
    Account_Number = str(worksheet.row(current_row)[14].value),
    partner = worksheet.row(current_row)[15].value,
    campaign = worksheet.row(current_row)[16].value,
    promo = worksheet.row(current_row)[17].value,
    tc = worksheet.row(current_row)[18].value)
    
for current_row in range(1,worksheet.nrows)
]

#driver_setup() and driver_teardown()    
@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if(os.environ.get('USE_PHANTOM',None)):    
        print('Making PhantomJS driver')
        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(1120,550)
    else:
        print("Making Firefox driver")
        _driver=webdriver.Firefox()
        _driver.get(config.INBOUND_LOGIN_URL)
        elem = _driver.find_element_by_name("email").send_keys(config.INBOUND_LOGIN_EMAIL)
        elem = _driver.find_element_by_name("password").send_keys(config.INBOUND_LOGIN_PASSWORD)
        elem = _driver.find_element_by_id("button").click()
        time.sleep(3)

    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            _driver.quit()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver

#Parameterization of enroll_data based on tc id
@pytest.mark.parametrize("payload",enroll_data,ids=[p.tc.lower() for p in enroll_data]) 

def test_state(driver,payload):
    print()
    
    try:
        _state_test_internals(driver, payload)
        
    except Exception as ae:
        import uuid
        filename = "./failed/test_EP_error_{}_{}.png".format(
            payload.tc,
            uuid.uuid4())
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.tc)
        print("filename:", filename)
        print(str(ae))
        raise ae

def _state_test_internals(driver,payload):
    driver.get("http://www.pt.energypluscompany.com/myinbound/paper.php")
    time.sleep(4)
    elem = driver.find_element_by_id(payload.brand)
    elem.click()
    time.sleep(3)

    #Customer information
    elem = driver.find_element_by_name("customer_first_name").send_keys(payload.first_name)
    elem = driver.find_element_by_name("customer_last_name").send_keys(payload.last_name)
    elem = driver.find_element_by_name("customer_address1").send_keys(payload.Address)
    elem = driver.find_element_by_name("customer_city").send_keys(payload.city)
    elem = driver.find_element_by_name("customer_state")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == payload.state:
            option.click()
       
    elem = driver.find_element_by_name("customer_zip5").send_keys(int(payload.zip))
    elem = driver.find_element_by_name("customer_area_code").send_keys(payload.area_code)
    elem = driver.find_element_by_name("customer_prefix").send_keys(int(payload.prefix))
    elem = driver.find_element_by_name("customer_line_number").clear()
    elem = driver.find_element_by_name("customer_line_number").send_keys(int(payload.last))
    elem = driver.find_element_by_name("account_type")
    #Check and select Account Type as per the data sheet
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == payload.Account_Type :
            option.click()
        
    if  driver.find_element_by_name("business_name").is_displayed():
        time.sleep(2)
        elem = driver.find_element_by_name("business_name").send_keys(payload.busname)
        time.sleep(1)

    #Billing Information
    elem = driver.find_element_by_name("copyinfo").click()
    elem = driver.find_element_by_name("email").send_keys(payload.email_addr)
    
    if driver.find_element_by_name("gas_utility").is_displayed():
        sel = Select(driver.find_element_by_name("gas_utility"))
        sel.select_by_visible_text(payload.Utility)
        elem = driver.find_element_by_name("gas_account_number")
        time.sleep(2)
        elem.send_keys(payload.Account_Number)
    
    #Order Information
    elem = driver.find_element_by_name("partner_code").send_keys(payload.partner)
    elem = driver.find_element_by_name("campaign_code").send_keys(payload.campaign)
    if driver.find_element_by_name("promo_code").is_displayed():
        elem = driver.find_element_by_name("promo_code").send_keys(payload.promo)
    else:
        elem = driver.find_element_by_name("elec_promo_code").send_keys(payload.promo)
    time.sleep(2)
           
    if driver.find_element_by_name("vendor_id").is_displayed():
        sel = Select(driver.find_element_by_name("vendor_id"))
        sel.select_by_visible_text("EPIB")
        time.sleep(2)    
                        
      
      
    # Grab Confirmation Code
    elem = driver.find_element_by_name("confCode")
    confCode = elem.text
    print("Passed - EP Paper - Electric, " + ' Confirmation code for ' +payload.state +' - ' +payload.Utility+" : "+confCode)
    elem = driver.find_element_by_name("submit")
    elem.click()
    #Check alert if present upon submitting the enrollment
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                   'Timed out' +
                                   'Acct Enrollment confirmation popup to appear.')

        alert = driver.switch_to_alert()
        alert.accept()
        print("alert accepted")
    except TimeoutException:
        print("no alert")



