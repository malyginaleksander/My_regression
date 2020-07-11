import csv
from collections import namedtuple
from datetime import datetime
import pytest
import xlrd
from webdriver_manager.chrome import ChromeDriverManager

from Regression.Inbound.Inbound_Enrollments_promo_test.InboundPromo_tests_Settings import *
from Regression.Inbound.Inbound_Enrollments_promo_test.helpers.Inbound_BrandPage import BrandPage
from Regression.Inbound.Inbound_Enrollments_promo_test.helpers.Inbound_accountNO_generator import account_generator_accountNo_1, \
    account_generator_accountNo_2, servicereference_generator
from Regression.Inbound.Inbound_Enrollments_promo_test.helpers.Inbound_generator_names_and_address import generaot_names_and_address_work
from Regression.Inbound.Inbound_Enrollments_promo_test.helpers.Inbound_generator_zip_city import generator_zip_city
from Regression.Inbound.Inbound_Enrollments_promo_test.helpers.Inbound_loginPage import LoginPage
# from Regression.Inbound.Inbound_Enrollments_promo_test.InboundPromo_tests_Settings import tester, chosen_driver, workbook_name, \
#     start_string, \
#     data_sheet_name, start_page, test_name
from Regression.Inbound.Inbound_Enrollments_promo_test.helpers.Inbound_pages_methods import *
from Regression.Inbound.Inbound_Enrollments_promo_test.helpers.Inbound_tags import *

sheet_name = data_sheet_name
workbook = xlrd.open_workbook(workbook_name)
worksheet = workbook.sheet_by_name(sheet_name)
tests_values = []
headers = [cell.value for cell in worksheet.row(0)]
Payload = namedtuple('payload', headers)
for current_row in range(int(start_string), worksheet.nrows):
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
        request.addfinalizer(resource_a_teardown)
        driver.close()
        driver.quit()
        return driver


def grab_code(accountNo_1, payload, promo_offer_portal_1, promo_offer_portal_2, no_offer_message):
    try:
    # wait_grab_code_page(driver)
        elem = driver.find_element_by_id("confcode")
    except:
        pass
        # confcode = elem.text
    # print(
    #     "Passed " + " " + payload.test_name + ", Conformation =  " + confcode + ' for ' + payload.state + ' - ' + payload.utility_1)
    city, generated_zipCode = generator_zip_city(payload)
    now = datetime.now()
    date = now.strftime("_%m_%d_%Y_")

    f = open("./outbox_files/" + test_name + date + "_tests_results.csv", 'a', newline='')
    time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
    csv_a = csv.writer(f)

    csv_a.writerow(
            [payload.ts, payload.state, 	payload.Partner, 	payload.Product, 	payload.Commodity, 	payload.Bonus,
             payload.Ongoing_Earn, 	payload.Campaign_Code, 	payload.Promo_Code, 	payload.Slug, 	payload.URL,
             payload.Utility, 	 payload.LP_Test_Confirmation_number, 	payload.SKU, promo_offer_portal_1, "Passed",  ])


@pytest.mark.parametrize("payload", tests_values, ids=[p.ts for p in tests_values])
def test_state(test_setup, payload):
    now = datetime.now()
    time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")

    try:
        Inbound_start_test(driver, payload)
    except Exception as ae:
        filename = ("./failed/" + data_sheet_name + "_fail_{}_{}.png").format(payload.ts, time)
        driver.get_screenshot_as_file(filename)
        # print("Saving screenshot of failed test -- ", payload.ts)
        # print("filename:", filename)
        # print(str(ae))
        city, generated_zipCode = generator_zip_city(payload)

        now = datetime.now()
        date = now.strftime("_%m_%d_%Y_")

        f = open("./outbox_files/" + test_name + date + "_tests_results.csv", 'a', newline='')
        now = datetime.now()
        time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
        csv_a = csv.writer(f)
        address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generaot_names_and_address_work()

        raise ae


def Inbound_start_test(test_setup, payload):
    accountNo_1 = account_generator_accountNo_1(payload)
    # address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generaot_names_and_address_work()
    # city, generated_zipCode = generator_zip_city(payload)
    # random_zip = generated_zipCode
    # first_name_generated_ = first_name_generated
    # last_name_generated_ = last_name_generated
    # servicereference = servicereference_generator(payload)
    # if payload.account_type_2 == 'Gas' or payload.account_type_2 == 'Electric':
    #     accountNo_2 = account_generator_accountNo_2(payload)
    # else:
    #     pass

    link = "http://products.nrgpl.us/api/v1/products/?sku=" + str(payload.SKU)
    driver.get(link)
    # print(link)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'Return all the published Products (paginated)')]")))
    # time.sleep(5)

    # driver.find_element_by_xpath("//*[@id='content']/div[1]/div[4]/pre/a[1]").click()

    # time.sleep(2)
    # address = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/div[4]/pre/span[43]').text()
    commodity = driver.find_element_by_xpath(
        "//span[contains(text(),'commodity')]/following-sibling::span[3]").text
    utility_slug = driver.find_element_by_xpath(
        "//span[contains(text(),'utility_slug')]/following-sibling::span[3]").text
    print(payload.ts, payload.SKU, commodity[1:-1], utility_slug[1:-1])




