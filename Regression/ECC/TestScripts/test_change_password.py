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
from selenium.webdriver.chrome.options import Options


local_path = "./ECC_TestData/TestData.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('Change_Password')

change_pw = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    change_pw.append(Payload(**value_dict))

@pytest.fixture(scope='module')
def driver(request):
   _driver = None
   print('driver_setup()')
   if os.environ.get('USE_CHROMEDRIVER'):
       print("using Chrome")
       _driver = webdriver.Chrome('/usr/local/bin/chromedriver')
   elif os.environ.get('USE_CHROMEDRIVER'):
       print("using headless Chrome")
       chrome_options = Options()
       chrome_options.add_argument("--headless")
       chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
       _driver = webdriver.Chrome(executable_path=os.path.abspath("/usr/local/bin/chromedriver"), chrome_options=chrome_options)
   elif os.environ.get('USE_PHANTOM'):
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


@pytest.mark.parametrize("payload", change_pw, ids=[p.tc for p in change_pw])
def test_login(driver, payload):
     print( )
     try:
        _test_change_pw( driver, payload )
     except Exception as ae:
        import uuid
        filename = "./failed/test_change_pw_{}_{}.png".format(payload.tc,uuid.uuid4())
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.tc)
        print("filename:", filename)
        print(str(ae))
        raise ae

def _test_change_pw(driver, payload):

    host = os.environ.get('ECC_PORTAL_HOST', 'https://nrg.enroll.pt.nrgpl.us/portal/login')
    url = '{}'.format(host)
    print("getting url: %s" % url)
    driver.get(url)
    driver.implicitly_wait(10)

    login = LoginPage(driver)
    login.login(payload)
    time.sleep(3)
    assert driver.find_element_by_xpath("//*[contains(text(),'Manage Profile')]").is_displayed()
    print("Asserting if logged in the portal")

    login.change_password(payload)
    time.sleep(4)
    actText = driver.find_element_by_xpath("//div//*[@id='change-password-confirmation']/div").text
    expText = "Password successfully changed."
    assert expText in actText
    print("Verifying the text Password successfully changed")

    driver.find_element_by_xpath("//div//*[@id='change-password-confirmation']/div/button[text()='Close']").click()
    print(" Closing the change password confirmation box")

    time.sleep(2)
    login.logout()
    print(" Logging out")