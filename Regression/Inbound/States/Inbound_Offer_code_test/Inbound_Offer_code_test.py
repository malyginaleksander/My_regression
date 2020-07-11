import csv
from collections import namedtuple
from datetime import datetime
import pytest
import xlrd
from webdriver_manager.chrome import ChromeDriverManager
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_BrandPage import BrandPage
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_generator_names_and_address import names_and_address_generator
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_generator_zip_city import generator_zip_city
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_loginPage import LoginPage
from Inbound.States.Inbound_Enrollments_4brands_test.InboundEnrollments_tests_Settings import tester, chosen_driver, workbook_name, start_string, \
    data_sheet_name, start_page
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_pages_methods import *
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags import *

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


# def grab_code(accountNo_1, payload):
#     wait_grab_code_page(driver)
#     elem = driver.find_element_by_id("confcode")
#     confcode = elem.text
#     # print(
#     #     "Passed " + " " + payload.test_name + ", Conformation =  " + confcode + ' for ' + payload.state + ' - ' + sap_UtilitySlug)
#     # city, generated_zipCode = generator_zip_city(payload)
#     # f = open("./Inbound_Enrollments_tests_results.csv", 'a', newline='')
#     # now = datetime.now()
#     # time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
#     # csv_a = csv.writer(f)
#     # address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generaot_names_and_address_work()
#     # csv_a.writerow(
#     #     ["Passed", tester, time, payload.test_name, payload.brand, payload.state])


@pytest.mark.parametrize("payload", tests_values, ids=[p.first_name for p in tests_values])
def test_state(test_setup, payload):
    now = datetime.now()
    time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")

    try:
        Inbound_start_test(driver, payload)
    except Exception as ae:
        filename = ("./failed/" + sheet_name + "_fail_{}_{}.png").format(payload.first_name, time)
        driver.get_screenshot_as_file(filename)
        print("Saving screenshot of failed test -- ", payload.first_name)
        print("filename:", filename)
        print(str(ae))
        city, generated_zipCode = generator_zip_city(payload)
        f = open("./Inbound_Enrollments_tests_results.csv", 'a', newline='')
        now = datetime.now()
        time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
        csv_a = csv.writer(f)
        address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = names_and_address_generator()
        csv_a.writerow(
            ["FAILED", tester, time, payload.test_name, payload.brand, payload.account_type_1, payload.account_type_2,
             payload.first_name,
             first_name_generated, last_name_generated, payload.state, city, payload.utility_1, payload.partner_1,
             payload.campaign_1, payload.categorie_1,
             payload.promo_1, generated_zipCode, " ", " "])
        raise ae


def Inbound_start_test(test_setup, payload):
    # accountNo_1 = account_generator_accountNo_1(payload)
    address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = names_and_address_generator()
    # city, generated_zipCode = generator_zip_city(payload)
    # random_zip = generated_zipCode
    first_name_generated_ = first_name_generated
    last_name_generated_ = last_name_generated
    # servicereference = servicereference_generator(payload)
    # if payload.account_type_2 == 'Gas' or payload.account_type_2 == 'Electric':
    #     accountNo_2 = account_generator_accountNo_2(payload)
    # else:
    #     pass

    if driver.current_url == start_page:
        pass
    else:
        driver.get(URL)
        ###         Login page        #################################################################################
        login = LoginPage(driver)
        login.fill_login()
    ###         Brand page        #################################################################################
    choose_brand = BrandPage(driver)
    if payload.brand == Energy_plus :
        choose_brand.click_EP_brand()
    elif payload.brand == NRG:
        choose_brand.click_NRG_brand()
    elif payload.brand == Green_ME:
        choose_brand.click_GME_brand()
    elif payload.brand == Cirro:
        choose_brand.click_Cirro_brand()
    choose_brand.click_save_and_continue_button()

    ### Get Started page       #################################################################################:
    wait_get_started_page(driver)
    # May I please have your name?
    fill_get_started_page(first_name_generated_, last_name_generated_, payload)

    ###     Offer page           #################################################################################:

    wait_offer_page(driver)
    elem = driver.find_element_by_xpath("//div[@id='offer_code_entry']").text
    grab_text = elem
    assert elem == 'Did you receive an offer code from Energy Plus?'
    if elem == 'Did you receive an offer code from Energy Plus?':
        print(payload.first_name + " - " + "the message exists " )
        f = open("./Inbound_Enrollments_tests_results.csv", 'a', newline='')
        now = datetime.now()
        time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
        csv_a = csv.writer(f)
        csv_a.writerow(
            ["Passed", tester, time, payload.test_name, payload.brand, payload.state, payload.utility_1, grab_text])
    else:
        print(payload.first_name + " - " + "the message doesn't exists ")




def fill_get_started_page(first_name_generated_, last_name_generated_, payload):
    driver.find_element_by_id(get_started_First_name_id).send_keys(tester + "_" + first_name_generated_)
    driver.find_element_by_id(get_started_last_name_id).send_keys(last_name_generated_)
    wait_get_started_page_state_list(driver)
    # What state are you are calling from?
    elem = driver.find_element_by_name(get_started_state_list_id)
    for option in elem.find_elements_by_tag_name(options_tag_name):
        if option.text == payload.state:
            option.click()
    # Is Your Name on the Utility Bill?
    if payload.state == "Maryland":
        # Is Your Name on the Utility Bill?
        try:
            elem = driver.find_element_by_xpath(get_started_name_utility_yes_xpath).click()
        except:
            pass
    # What account are you calling about today? - gas or electric
    try:
        if payload.account_type_1 == 'Electric':
            try:
                elem = driver.find_element_by_class_name(
                    get_call_account_electric_class_name).click()
            except:
                pass
        if payload.account_type_1 == 'Gas':
            try:
                elem = driver.find_element_by_class_name(get_call_account_gas_class_name).click()
            except:
                pass
    except:
        pass
    # Who is the provider for your electric account?
    if payload.account_type_1 == 'Electric':
        elem = driver.find_element_by_name(get_started_EL_utility_1_class_name)
        for option in elem.find_elements_by_tag_name(options_tag_name):
            if option.text == payload.utility_1:
                option.click()
    if payload.account_type_1 == 'Gas':
        try:
            elem = driver.find_element_by_xpath(get_started_Gas_utility_1_xpath)
            for option in elem.find_elements_by_tag_name(options_tag_name):
                if option.text == payload.utility_1:
                    option.click()
        except:
            elem = driver.find_element_by_xpath(get_started_Gas_utility_NJ_xpath)
            for option in elem.find_elements_by_tag_name(options_tag_name):
                if option.text == payload.utility_1:
                    option.click()
    # Is this electric account a residential or business address?try:
    try:
        if payload.type == 'Residential':
            elem = driver.find_element_by_class_name(get_started_resident_class_name).click()
        elif payload.type == 'Business':
            elem = driver.find_element_by_class_name(get_started_business_class_name).click()
    except:
        pass

    ##2 accounts test:
    if payload.account_type_2 == "Electric" or payload.account_type_2 == "Gas":
        elem = driver.find_element_by_id(get_started_add_second_account_id).click()
        # time.sleep(1)
        # if payload.account_type_2 == "Gas":
        elem = driver.find_element_by_xpath(get_started_select_state_for_secondAC_xpath)  # second state
        for option in elem.find_elements_by_tag_name(options_tag_name):
            if option.text == payload.state:
                option.click()
        time.sleep(1)
        if payload.account_type_2 == "Gas":
            elem = driver.find_element_by_xpath(get_started_second_account_is_gas_xpath).click()  # choose second_gas
        elem = driver.find_element_by_xpath(get_started_secon_provider_xpath)  # choose second utility
        for option in elem.find_elements_by_tag_name(options_tag_name):
            if option.text == payload.utility_2:
                option.click()

    if payload.type == "Residential":
        Residentials_buttons = driver.find_elements_by_class_name('account-type-residential')
        for x in range(0, len(Residentials_buttons)):
            if Residentials_buttons[x].is_displayed():
                Residentials_buttons[x].click()

    if payload.type == "Business":
        Business_buttons = driver.find_elements_by_class_name('account-type-business')
        for x in range(0, len(Business_buttons)):
            if Business_buttons[x].is_displayed():
                Business_buttons[x].click()

    if payload.account_type_1 == "Gas" or payload.account_type_2 == "Gas":
        if payload.gas_option == 'Heating Only':
            heating_buttons = driver.find_elements_by_class_name(get_started_gas_HeatingOnly_class_name)
            for x in range(0, len(heating_buttons)):
                if heating_buttons[x].is_displayed():
                    heating_buttons[x].click()
        if payload.gas_option == 'Cooking Only':
            cooking_buttons = driver.find_elements_by_class_name(get_started_gas_CookingOnly_class_name)
            for x in range(0, len(cooking_buttons)):
                if cooking_buttons[x].is_displayed():
                    cooking_buttons[x].click()
        if payload.gas_option == 'Both Heating & Cooking':
            both_buttons = driver.find_elements_by_class_name(get_started_gas_Both_class_name)
            for x in range(0, len(both_buttons)):
                if both_buttons[x].is_displayed():
                    both_buttons[x].click()

    if payload.brand == Green_ME and payload.state == 'New York':
        try:
            elem = driver.find_element_by_name("zone")
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == ("Westchester"):
                    option.click()
        except:
            pass
    # Save and continue button
    elem = driver.find_element_by_id(get_started_save_and_con_but_id).click()

