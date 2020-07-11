from __future__ import print_function
from selenium import webdriver
from ECC_PageFactory.SignUpFromMail import SignUpFromMail
import time
import xlrd
import os
import pytest
from collections import namedtuple
from ECC_PageFactory.LoginPage import LoginPage
import pytest

local_path = "./ECC_TestData/TestData.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('login')

savedcorrespondence = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    savedcorrespondence.append(Payload(**value_dict))

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


@pytest.mark.parametrize("payload", savedcorrespondence, ids=[p.tc for p in savedcorrespondence])
def test_resetpwpage_errormsgs(driver, payload):
     print( )

     try:
        _test_savedcorrespondence( driver, payload )
     except Exception as ae:
        import uuid
        filename = "./failed/test_resetpwd_{}_{}.png".format(payload.tc,uuid.uuid4())
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.tc)
        print("filename:", filename)
        print(str(ae))
        raise ae

def _test_savedcorrespondence(driver, payload):

        host = os.environ.get('ECC_PORTAL_HOST', 'https://nrg.enroll.pt.nrgpl.us/portal/login')
        url = '{}'.format(host)
        print("getting url: %s" % url)
        driver.get(url)
        driver.implicitly_wait(10)

        login = LoginPage(driver)
        login.login(payload)
        time.sleep( 7 )

        driver.find_element_by_xpath("//table/tbody/tr/td/a[contains(text(),'Welcome to the NRG_regression Home Family')]").click()
        #self.driver.find_element_by_xpath("").click()

        portalPWH = driver.current_window_handle

        registerAcct = SignUpFromMail(driver)
        registerAcct.switch_to_new_window(portalPWH)


        time.sleep(3)
        driver.find_element_by_xpath("//table/tbody//tr//td//a//span[text()='link']").click()

        time.sleep(2)
        #registerAcct.switch_to_new_window_checktwo(portalPWH,linkPWH)
        time.sleep(2)

        assert driver.find_element_by_xpath("//*[contains(text(),'Create New Account')]").is_displayed()
        driver.close()

        driver.switch_to.window(portalPWH)
        time.sleep(3)
        driver.find_element_by_xpath("//table/tbody/tr/td/a[contains(text(),'Welcome to the NRG_regression Home Family')]").click()
        time.sleep(3)

        registerAcct.switch_to_new_window(portalPWH)
        driver.find_element_by_xpath("//table/tbody/tr/td/a/span[contains(text(),'Terms of Service')]").click()

        time.sleep(3)
        assert driver.find_element_by_tag_name("tbody").is_displayed()

        time.sleep(1)
        driver.close()


        driver.switch_to.window(portalPWH)
        time.sleep(3)

        login = LoginPage(driver)
        login.logout()
