from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os
import pytest
from collections import namedtuple
from PageFactory.ConfirmPlanPage import ConfirmPlanPage
from States.NrgEnroll import NrgEnroll
from ECC_PageFactory.test_SignUpAccount import test_SignUpAccount
from PageFactory.ConfirmationPage import ConfirmationPage
from PageFactory.VerificationPage import VerificationPage
from PageFactory.ThanksPage import ThanksPage
import pytest
import logging
import ConfigFiles.logger as cl
from selenium.webdriver.chrome.options import Options

local_path = "./ECC_TestData/TestData.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name('Blacklisted_Email')

blacklisted_email = []

headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)

for current_row in range(1, worksheet.nrows):
    values = [cell.value for cell in worksheet.row(current_row)]
    value_dict = dict(zip(headers, values))
    blacklisted_email.append(Payload(**value_dict))

log = cl.genericLogger(logging.DEBUG)

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


# @pytest.fixture(scope='module')
# def driver(request):
#    _driver = None
#    print('driver_setup()')
#    if os.environ.get('USE_CHROMEDRIVER'):
#        print("using headless Chrome")
#        chrome_options = Options()
#        chrome_options.add_argument("--headless")
#        chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
#        _driver = webdriver.Chrome(executable_path=os.path.abspath("/usr/local/bin/chromedriver"), chrome_options=chrome_options)
#        _driver.maximize_window()
#    else:
#        print("no chromium")

   def resource_a_teardown():
       print('driver_setup teardown()')
       if _driver:
           print(_driver.current_url)
           _driver.close()
       else:
           assert False, "can't close driver"
   request.addfinalizer(resource_a_teardown)
   return _driver

log.info("New Test started")

@pytest.mark.parametrize("payload", blacklisted_email, ids=[p.tc for p in blacklisted_email])

def test_blacklisted_email(driver, payload):
     print( payload.tc, 'NRG_regression WEB Electric Enrollment - State = ', payload.state, ' - utility = ', payload.utility, ' Going to the Confirmation Page = ', payload.VerifyConfNo, ' Displaying Error Msg = ', payload.VerifyErrMsg, )

     try:
        _blacklisted_email(driver, payload)
     except Exception as ae:
        import uuid
        filename = "./failed/test_blacklisted_email_fail_{}_{}.png".format(payload.tc,uuid.uuid4())
        driver.save_screenshot(filename)
        print("Saving screenshot of failed test -- ", payload.tc)
        print("filename:", filename)
        print(str(ae))
        raise ae

def _blacklisted_email(driver, payload):
        host = os.environ.get('ECC_ENROLL_HOST', 'https://nrg.enroll.pt.nrgpl.us/')
        url = '{}{}'.format(host, payload.query_string)
        print("getting url: %s" % url)
        driver.implicitly_wait(15)
        driver.get(url)

        ## Personal Information
        print("Personal Information")

        print("title: ", driver.title)

        NrgEn= NrgEnroll(driver)
        log.info("Getting the blacklisted_email method from the NRGEnroll page")
        NrgEn.blacklisted_email(payload)

        if "Yes" in payload.VerifyConfNo:

            # Verification
            vp = VerificationPage( driver )
            log.info("Getting the scroll_termsandconditions_and_agree method from the VerificationPage ")
            vp.scroll_termsandconditions_and_agree()

            ## Grab Confirmation Code
            cop = ConfirmationPage( driver )
            log.info("Getting the confirmation number")
            confirmationNum = cop.get_confirmation_number()
            print( "Confirmation Number is: " + str(confirmationNum))

            #Here Expected confirmation number should be updated
            log.info("Asserting the confirmation number")
            assert confirmationNum == confirmationNum

            ##Select Preferences
            print( "Selecting Preferences" )
            log.info("Getting the select_allpreferences_on_confirmationpage method from the Confirmationpage ")
            NrgEn.select_allpreferences_on_confirmationpage()
            log.info("Test Case Ended ")
            log.info("****************************")
