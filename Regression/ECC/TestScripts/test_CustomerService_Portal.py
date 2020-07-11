from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple
from ECC_PageFactory.LoginPage import LoginPage
import pytest
from ECC_PageFactory.SignUpFromMail import SignUpFromMail


local_path = "./ECC_TestData/TestData.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('CustomerService_PortalAccess')

CustomerService_CustomerPortal = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    CustomerService_CustomerPortal.append(Payload(**value_dict))

@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('USE_PHANTOM'):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(1400,1000)
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


@pytest.mark.parametrize("payload", CustomerService_CustomerPortal, ids=[p.tc for p in CustomerService_CustomerPortal])
def test_login(driver, payload):
     print( )
     try:
        _test_login( driver, payload )
     except Exception as ae:
        import uuid
        filename = "./failed/test_CustomerService_CustomerPortal_{}_{}.png".format(payload.tc,uuid.uuid4())
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.tc)
        print("filename:", filename)
        print(str(ae))
        raise ae

def _test_login(driver, payload):

        driver.get("http://epnet2.qa.nrgpl.us/member?accountId=1959808")
        driver.maximize_window( )
        driver.implicitly_wait( 10 )
        time.sleep(10)
        driver.find_element_by_xpath("//*[@id='memberFormTabs']//a[contains(text(),'Portal')]").click()
        time.sleep(7)
        driver.find_element_by_xpath("//*[@id='memberFormTabContainer']//*[contains(text(),'"+payload.UserMail+"')]").click()


        pwh = driver.current_window_handle

        mailObj = SignUpFromMail(driver)
        mailObj.switch_to_new_window(pwh)

        login = LoginPage(driver)
        login.switch_account_generic(payload)

        driver.close()
        time.sleep(3)
        driver.switch_to.window(pwh)
        time.sleep(3)
        # for reset password
        driver.find_element_by_xpath("//*[@id='memberFormTabContainer']//*[contains(text(),'reset password')]").click()
        mailObj = SignUpFromMail(driver)
        mailObj.switch_to_new_window(pwh)


        # login.login(payload)
        time.sleep(3)




