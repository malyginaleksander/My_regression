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
import logging
import ConfigFiles.logger as cl

local_path = "./ECC_TestData/TestData.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('Blank_friendlyname')

blank_friendlyname = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    blank_friendlyname.append(Payload(**value_dict))

log = cl.genericLogger(logging.DEBUG)

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

log.info("New Test started ")

@pytest.mark.parametrize("payload", blank_friendlyname, ids=[p.tc for p in blank_friendlyname])
def test_login(driver, payload):
     print( )
     log.info("Making Firefox driver")

     try:
        _test_blank_friendlyname( driver, payload )
        print(payload.tc, 'Username = ', payload.userName, 'Password = ', payload.password, 'Save/Cancel = ', payload.Action, )
     except Exception as ae:
        import uuid
        filename = "./failed/test_blank_friendlyname_{}_{}.png".format(payload.tc,uuid.uuid4())
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.tc)
        print("filename:", filename)
        print(str(ae))
        raise ae

def _test_blank_friendlyname(driver, payload):
          host = os.environ.get('ECC_PORTAL_HOST','https://nrg.enroll.pt.nrgpl.us/portal/login')
          url = '{}'.format(host)
          print("getting url: %s" % url)
          driver.get(url )
          driver.implicitly_wait( 10 )

          login = LoginPage(driver)
          log.info("Getting the login method from the login page")
          login.login(payload)
          time.sleep( 3 )
          print("Verifying if the manage profile page is displayed")
          assert driver.find_element_by_xpath(".//*[@id='NRG_regression']//div//h2").is_displayed()

          log.info("Getting the blank_friendlyname method from the login page")
          login.blank_friendlyname(payload)
          time.sleep(2)

          log.info("Getting the logout method from the login page")
          login.logout()
          log.info("Test Case Ended ")
          log.info("****************************")