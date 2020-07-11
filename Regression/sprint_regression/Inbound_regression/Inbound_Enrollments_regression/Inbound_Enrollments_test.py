import csv
import os
from collections import namedtuple
from datetime import datetime
import pytest
import xlrd
from webdriver_manager.chrome import ChromeDriverManager

from Regression.helpers.Inbound.Inbound_BrandPage import choose_brand
from Regression.helpers.common.create_data_for_test import create_data_for_test
from Regression.helpers.common.create_data_for_test_2 import create_data_for_test_2
from Regression.helpers.Inbound.Inbound_CustomerInfoPage import \
    fill_CustomerInfoPage
from Regression.sprint_regression.Inbound_regression.Inbound_Enrollments_regression.Inbound_BillingInfoPage import \
    fill_billing_info_page
from Regression.sprint_regression.Inbound_regression.Inbound_Enrollments_regression.Inbound_GetStartedPage import \
    fill_GetStartedPage
from Regression.helpers.Inbound.Inbound_OfferPage import \
    fill_offer_page
from Regression.helpers.Inbound.Inbound_loginPage import *
from Regression.helpers.Inbound.Inbound_GrabCode import grab_code
from Regression.sprint_regression.Inbound_regression.Inbound_Enrollments_regression.Inbound_UtilityNameGenarator import \
    UtilityNameGenerator, UtilityNameGenerator_2
from  Regression.sprint_regression.Inbound_regression.Inbound_Enrollments_regression.Inbound_pages_methods import *
from  Regression.sprint_regression.Inbound_regression.Inbound_Enrollments_regression.Inbound_tags import *

test_list=[5,11,15,18,19]
start_test =1
env = "pt"
# env = "GME_en"

test_name = 'Regressin_Inbound'

data_sheet_name = 'Inbound_Test_Data _regression19'
chosen_driver = "chrome"
# chosen_driver = "firefox"

# URL = "http://www.gme-plus.energypluscompany.com/myinbound/login.php"
# URL = "http://www.energypluscompany.com/myinbound/login.php"
URL = "http://www.pt.energypluscompany.com/myinbound/login.php"

start_page = 'http://www.pt.energypluscompany.com/myinbound/tab_brand.php'
# start_page = 'http://www.gme-plus.energypluscompany.com/myinbound/login.php/tab_brand.php'

login_email_data = "aleksandr.malygin@nrg.com"
# login_email_data = "gurjeet.saini@nrg.com"
login_password_data = "energy"



local_path = "./inbox_files/Regression_test_scenarios.xlsx"
full_path = os.path.abspath(local_path)
workbook = xlrd.open_workbook(full_path)
worksheet = workbook.sheet_by_name(data_sheet_name)
headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)
tests_values = []
if len(test_list) > 0:
    for current_row in test_list:
        values = [cell.value for cell in worksheet.row(current_row)]
        value_dict = dict(zip(headers, values))
        tests_values.append(Payload(**value_dict))
else:
    for current_row in range(start_test, worksheet.nrows):
        values = [cell.value for cell in worksheet.row(current_row)]
        value_dict = dict(zip(headers, values))
        tests_values.append(Payload(**value_dict))




@pytest.fixture(scope='session')
def test_setup(request):
    global driver

    if chosen_driver == "firefox":
        driver = webdriver.Firefox()
    elif chosen_driver == "chrome":
        driver = webdriver.Chrome(ChromeDriverManager("2.36").install())
    else:
        driver = webdriver.Chrome(ChromeDriverManager("2.36").install())
    def resource_a_teardown():
        driver.quit()
    request.addfinalizer(resource_a_teardown)
    return driver


@pytest.mark.parametrize("payload", tests_values, ids=[p.ts for p in tests_values])
def test_state(test_setup, payload):
    now = datetime.now()
    time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")

    try:
        Inbound_start_test(driver, payload)
    except Exception as ae:

        filename = ("./failed/" + test_name + "_fail_{}_{}.png").format(payload.ts, time)
        driver.get_screenshot_as_file(filename)
        print("Saving screenshot of failed test -- ", payload.ts)
        print("filename:", filename)
        print(str(ae))
        f = open("./Inbound_Enrollments_tests_results.csv", 'a', newline='')
        now = datetime.now()
        time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
        csv_a = csv.writer(f)
        csv_a.writerow(
            ["FAILED",  time, payload.ts, payload.brand, payload.account_type_1, payload.account_type_2,
             payload.first_name, payload.state, payload.city, payload.UtilitySlug, payload.partner_1,
             payload.campaign_1, payload.categorie_1,payload.promo_1, payload.zip_code])


        raise ae
    except:
        pass


def Inbound_start_test(test_setup, payload):

    global accountNo_2
    firstname, lastname, address, zipcode_, city, accountNo, email, account_number,  phonenumber = create_data_for_test(payload)

    if len(payload.account_type_2)>0:
        accountNo_2 = create_data_for_test_2(payload)
    else:
        accountNo_2=''
    utility  = UtilityNameGenerator(payload)

    if len (payload. UtilitySlug_2)>0:
        utility_2 = UtilityNameGenerator_2(payload)
    else:
        utility_2 = ''


    if driver.current_url == start_page:
        pass
    else:
        driver.get(URL)
        ### Login page
        fill_login(driver, login_email_data, login_password_data )

    ### Brand page
    choose_brand(payload, driver)

    ### Get Started page:
    wait_get_started_page(driver)
    fill_GetStartedPage(payload, driver,  firstname, lastname, utility, utility_2)

    ###  Offer page
    wait_offer_page(driver)
    time.sleep(1)
    fill_offer_page(payload, driver)

    ### Customer Info page
    fill_CustomerInfoPage(driver, payload, accountNo, accountNo_2,  address, city, firstname, lastname,
                          phonenumber, zipcode_)


    ### Billing Info
    wait_billing_page(driver)
    fill_billing_info_page(driver, payload, firstname, lastname, address, zipcode_, city, accountNo, email,  phonenumber)

    ## Summary:
    summary(driver)

    ## Disclosure:
    if env == "GME_en":
        declouser_GreenME_GME_env(driver)
    elif env.upper() == 'PT':
        if payload.brand == Green_ME:
            declouser_GreenME(driver)
        elif payload.brand == 'NRG':
            declouser_NRG(driver)
        else:
            declouser_EP(driver)

    ### Grab Conformation Code

    grab_code(driver, payload, test_name, firstname, lastname, address, zipcode_, city, accountNo, email, accountNo_2, phonenumber)

    ## Submit
    try:
        driver.find_element_by_id(submit_enroll_id).click()
    except:
        pass

    wait_finish_page(driver)
    driver.find_element_by_id(start_new_call_id).click()


