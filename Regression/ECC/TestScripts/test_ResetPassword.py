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
worksheet = workbook.sheet_by_name('Reset_Password')

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


@pytest.mark.parametrize("payload", enroll_data, ids=[p.tc for p in enroll_data])
def test_ResetPassword(driver, payload):
     print( )

     try:
        _test_resetPassword( driver, payload )
     except Exception as ae:
        import uuid
        filename = "./failed/test_resetpwd_{}_{}.png".format(payload.tc,uuid.uuid4())
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.tc)
        print("filename:", filename)
        print(str(ae))
        raise ae

def _test_resetPassword(driver, payload):

        host = os.environ.get('ECC_PORTAL_HOST', 'https://nrg.enroll.pt.nrgpl.us/portal/login')
        url = '{}'.format(host)
        print("getting url: %s" % url)
        driver.get(url)
        driver.implicitly_wait(10)

        login = LoginPage( driver )
        login.click_forgot_password()
        login.enteremail_resetpasswordpage(payload)
        time.sleep(3)

        pwh = driver.current_window_handle
        driver.get( "https://mail.google.com/" )
        mailObj = SignUpFromMail(driver)
        mailObj.gmail_login(payload)
        searchText="Portal Reset Password"
        mailObj.search_email_click_signuplink_generic(searchText)
        mailObj.click_passwordresetlink_in_email()
        mailObj.switch_to_new_window(pwh)

        login = LoginPage( driver )
        login.resetpassword_resetlinkpage(payload)
        time.sleep(3)
        #assert driver.find_element_by_xpath("//div//*[contains(text(),'You have successfully reset your password.')]").is_displayed()
        #driver.close()

        #driver.switch_to.window(pwh)
        #driver.get( payload.url )

        #login = LoginPage( driver )
        login.login_after_change_password(payload)
        time.sleep(3)
        assert driver.find_element_by_xpath( "//div//*[contains(text(),'Manage Profile')]" ).is_displayed( )

        login.logout()
        time.sleep(3)