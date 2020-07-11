import csv
import os
from collections import namedtuple
from datetime import datetime
import pytest
import xlrd
from webdriver_manager.chrome import ChromeDriverManager

from Regression.Inbound.Inbound_Enrollments_promo_AMTRAK_test.InboundPromo_tests_Settings import *
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


now = datetime.now()
date_= now.strftime("%m.%d.%Y")

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


def grab_code(accountNo_1, payload):
    global confcode
    wait_grab_code_page(driver)

    try:
        confcode = driver.find_element_by_id("confcode").text
    except:
        pass

    if payload.email ==1:
        driver.find_element_by_id('toggle_xsell_consent_yes').click()
    else:
        pass


    now = datetime.now()
    date = now.strftime("_%m_%d_%Y_")
    csv_filename="./b_files_for_testing_02/" + test_name + date + "_tests_results.csv"


    if os.path.isfile(csv_filename):
        f = open(csv_filename, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(
            [ "Passed", payload.test_name, payload.brand, payload.account_type_1, payload.SKU, payload.TS, payload.state, payload.utility_, payload.utility_1, str("'" + str(payload.UAN)), payload.FirstName, payload.LastName	, payload.Service_Type, payload.UtilitySlug	, payload.ServiceAddress1	, payload.ServiceAddress2	, payload.ServiceCity	, payload.ServiceState	, payload.ServiceZip	, payload.zip_code	, payload.city	, "email", date_, confcode, ])
    else:
        f = open(csv_filename, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(
            ["status", "test_name", 'brand', 'account_type_1', 'SKU', 'TS', 'state',  'utility_', 'utility_1', 'UAN',	'FirstName',	'LastName',	'Service_Type',	'UtilitySlug',	'ServiceAddress1',	'ServiceAddress2',	'ServiceCity',	'ServiceState',	'ServiceZip',	'zip_code',	'city',	'with_email', 'date_', 'confcode' ])
        csv_a.writerow(
            [ "Passed", payload.test_name, payload.brand, payload.account_type_1, payload.SKU, payload.TS, payload.state, payload.utility_, payload.utility_1, str("'" + str(payload.UAN)), payload.FirstName, payload.LastName	, payload.Service_Type, payload.UtilitySlug	, payload.ServiceAddress1	, payload.ServiceAddress2	, payload.ServiceCity	, payload.ServiceState	, payload.ServiceZip	, payload.zip_code	, payload.city	, "email", date_, confcode, ])


@pytest.mark.parametrize("payload", tests_values, ids=[p.TS for p in tests_values])
def test_state(test_setup, payload):
    now = datetime.now()
    time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")

    try:
        Inbound_start_test(driver, payload)
    except Exception as ae:
        filename = ("./failed/" + sheet_name + "_fail_{}_{}.png").format(payload.TS, time)
        driver.get_screenshot_as_file(filename)
        print("Saving screenshot of failed test -- ", payload.TS)
        print("filename:", filename)
        print(str(ae))
        city, generated_zipCode = generator_zip_city(payload)

        now = datetime.now()
        date = now.strftime("_%m_%d_%Y_")

        f = open("./" + test_name + date + "_tests_results.csv", 'a', newline='')
        now = datetime.now()
        # time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
        csv_a = csv.writer(f)
        # address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generaot_names_and_address_work()
        csv_a.writerow(
            ["FAILED",  payload.test_name, payload.brand, payload.account_type_1, payload.SKU, payload.TS, payload.state, payload.utility_, payload.utility_1, date_, confcode])
        raise ae


def Inbound_start_test(test_setup, payload):
    accountNo_1 = account_generator_accountNo_1(payload)
    address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generaot_names_and_address_work()
    city, generated_zipCode = generator_zip_city(payload)
    random_zip = generated_zipCode
    first_name_generated_ = first_name_generated
    last_name_generated_ = last_name_generated
    servicereference = servicereference_generator(payload)


    if driver.current_url == start_page:
        pass
    else:
        driver.get("http://pt.energypluscompany.com/myinbound/tab_brand.php")
        print(URL)
###         Login page        #################################################################################
        login = LoginPage(driver)
        login.fill_login()
    ###         Brand page        #################################################################################
    choose_brand = BrandPage(driver)
    choose_brand.click_NRG_brand()
    choose_brand.click_save_and_continue_button()

    ### Get Started page       #################################################################################:
    wait_get_started_page(driver)
    # May I please have your name?
    fill_get_started_page(first_name_generated_, last_name_generated_, payload)

    ###     Offer page           #################################################################################:

    wait_offer_page(driver)
    time.sleep(2)
#PROMO ##################################################################################################################
    driver.find_element_by_xpath(offer_promo_partner_xpath).send_keys("ATK")
    driver.find_element_by_xpath(offer_promo_Campaign_xpath).send_keys("7923")
    driver.find_element_by_xpath(offer_promo_Promo_xpath).send_keys('249')
    driver.find_element_by_xpath(offer_submit_promoCode_xpath).click()

    wait_PROMO_OfferPlans_page(driver)
    driver.find_element_by_name(continue_button_name).click()




    ## Customer Info page        #################################################################################::

    wait_costumer_info_page(driver)

    if len(payload.FirstName)>0:
        FirstName = payload.FirstName
    else:
        FirstName = (tester + "_" + first_name_generated_)

    if len(payload.LastName)>0:
        LastName = payload.LastName
    else:
        LastName = (last_name_generated_)

    if len(payload.ServiceAddress1)>0:
        address_1 = payload.ServiceAddress1
        address_2 = payload.ServiceAddress2
    else:
        address_1 = (address_house_street_generated)
        address_2 = ""


    if len(payload.ServiceCity)>0:
        city_ = payload.ServiceCity
    else:
        city_ = city


    if len(str(payload.zip_code))>0:
        zip_code = payload.zip_code
    else:
        zip_code = random_zip


    if len(payload.UAN)>0:
        if payload.utility_1 =='Duke Energy Ohio':
            account_no = (str(payload.UAN)+"0")
        else:
            account_no = payload.UAN
    else:
        account_no = accountNo_1
    # z = payload.ServiceAddress2
    # if (payload.ServiceAddress2)>0:
    #     address_2=payload.ServiceAddress2
    #     print(payload.ServiceAddress2)
    # else:
        address2 = address_2
    elem = driver.find_element_by_name(customer_firs_name_name).send_keys(FirstName)
    elem = driver.find_element_by_name(customer_last_name_name).send_keys(LastName)
    elem = driver.find_element_by_name(customer_service_address_1_name).send_keys(address_1)
    elem = driver.find_element_by_name(customer_service_address_2_name).send_keys(address_2)
    elem = driver.find_element_by_name(customer_city_name).send_keys(city_)
    elem = driver.find_element_by_name(customer_zip_name).send_keys(str(zip_code))

    elem = driver.find_element_by_name(customer_phone_area_code_name).send_keys(phone_area_code_generated)
    elem = driver.find_element_by_name(customer_prefix_name).send_keys(phone_prefix_generated)
    elem = driver.find_element_by_name(customer_last_digit_name).send_keys(phone_last_generated)

    elem = driver.find_element_by_class_name(customer_uan_name).send_keys(account_no)

    if payload.state == 'Massachusetts':
        try:
            elem = driver.find_element_by_name(customer_customer_key_name).send_keys("test")
            driver.find_element_by_xpath(customer_servicereference_xpath).send_keys(int(servicereference))
            time.sleep(2)
        except:
            pass

    time.sleep(1)
    try:
        Check_buttons = driver.find_elements_by_xpath(costumer_CheckButtons_xpath)
        for x in range(0, len(Check_buttons)):
            if Check_buttons[x].is_displayed():
                Check_buttons[x].click()
    except:
        pass
    # WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element_value(By.XPATH, "//span[@class='account-uan-span']/following-sibling::div/span"), "Valid!")

    time.sleep(2)
    try:
        elem = driver.find_element_by_id(continue_button_id).click()
    except:
        pass
    # try:
    #     elem = driver.find_element_by_name(continue_button_id).click()
    # except:
    #     pass
        ## Billing Info        #################################################################################:
    wait_billing_page(driver)
    fill_billing_info_page(address_house_street_generated, city, payload, phone_area_code_generated,
                           phone_last_generated, phone_prefix_generated, generated_zipCode)

    # ## Summary:
    summary(driver)


    # ## Disclosure:
    declouser_NRG(driver)

    ### Grab Conformation Code #################################################################################:
    #
    grab_code(accountNo_1, payload)
    #
    ## Submit        #################################################################################:
    try:
        elem = driver.find_element_by_id(submit_enroll_id).click()
    except:
        pass
    #
    wait_finish_page(driver)
    driver.find_element_by_id(start_new_call_id).click()


def fill_billing_info_page(address_house_street_generated, city, payload, phone_area_code_generated,
                           phone_last_generated, phone_prefix_generated, generated_zipCode):


    if len(payload.ServiceAddress1)>0:
        address_1 = payload.ServiceAddress1
        address_2 = payload.ServiceAddress2
    else:
        address_1 = (address_house_street_generated)
        address_2 = ""


    if len(payload.ServiceCity)>0:
        city_ = payload.ServiceCity
    else:
        city_ = city


    if len(str(payload.zip_code))>0:
        zip_code = payload.zip_code
    else:
        zip_code = generated_zipCode


    elem = driver.find_element_by_name(billing_address_name).send_keys(address_1)
    elem = driver.find_element_by_name(billing_address_name_2).send_keys(address_2)
    elem = driver.find_element_by_name(billing_city_name).send_keys(city_)
    elem = driver.find_element_by_class_name(billing_state_class_name)
    for option in elem.find_elements_by_tag_name(options_tag_name):
        if option.text == payload.state:
            option.click()
    elem = driver.find_element_by_name(billing_zip_name).send_keys(str(zip_code))
    elem = driver.find_element_by_name(billing_phone_area_code_name).send_keys(phone_area_code_generated)
    elem = driver.find_element_by_name(billing_phone_prefix_area_name).send_keys(phone_prefix_generated)
    elem = driver.find_element_by_name(billing_phone_last_digits_name).send_keys(phone_last_generated)

    if payload.email == 1:
        email_no_buttons = driver.find_elements_by_class_name(billing_email_yes_class_name)
        for x in range(0, len(email_no_buttons)):
            if email_no_buttons[x].is_displayed():
                email_no_buttons[x].click()
        time.sleep(1)
        driver.find_element_by_name(billing_email_name).send_keys(str(payload.TS + "@gmail.com"))

    else:
        email_no_buttons = driver.find_elements_by_class_name(billing_phone_email_no_class_name)
        for x in range(0, len(email_no_buttons)):
            if email_no_buttons[x].is_displayed():
                email_no_buttons[x].click()

        email_no_buttons = driver.find_elements_by_class_name(billing_phone_email_no_no_class_name)
        for x in range(0, len(email_no_buttons)):
            if email_no_buttons[x].is_displayed():
                email_no_buttons[x].click()





    elem = driver.find_element_by_id(continue_button_id).click()
    time.sleep(2)


def fill_offer_page(payload):

    if payload.brand == NRG:
        wait_offer_page(driver)

        try:
            driver.find_element_by_xpath(offer_search_xpath).send_keys(payload.categorie_1)
            driver.find_element_by_id(payload.categorie_1).click()
        except:
            try:
                elem = driver.find_element_by_id(payload.categorie_1).click()
            except:
                pass


    if payload.utility_type == 'Variable':
        try:
            Variable_buttons = driver.find_elements_by_xpath(offer_Varriable_choise_xpath)
            for x in range(0, len(Variable_buttons)):
                if Variable_buttons[x].is_displayed():
                    Variable_buttons[x].click()
        except:
            pass
    elif payload.utility_type == 'Fixed':
        try:
            Fixed_buttons = driver.find_elements_by_xpath(offer_Fixed_choise_xpath)
            for x in range(0, len(Fixed_buttons)):
                if Fixed_buttons[x].is_displayed():
                    Fixed_buttons[x].click()
        except:
            pass

    time.sleep(2)
    # Green option

    try:
        Check_buttons = driver.find_elements_by_xpath(costumer_CheckButtons_xpath)
        for x in range(0, len(Check_buttons)):
            if Check_buttons[x].is_displayed():
                Check_buttons[x].click()
    except:
        pass
    # Todo - finish wait
    time.sleep(1)
    try:
        elem = driver.find_element_by_id(continue_button_id).click()
    except:
        pass
    if payload.brand == Green_ME or payload.brand == NRG or payload.brand == Cirro:
        try:
            driver.find_element_by_name(continue_button_name).click()
        except:
            pass


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
        elem = driver.find_element_by_class_name(get_call_account_electric_class_name).click()
    except:
        pass
    # Who is the provider for your electric account?

    elem = driver.find_element_by_name(get_started_EL_utility_1_class_name)
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


    # Save and continue button
    elem = driver.find_element_by_id(get_started_save_and_con_but_id).click()


