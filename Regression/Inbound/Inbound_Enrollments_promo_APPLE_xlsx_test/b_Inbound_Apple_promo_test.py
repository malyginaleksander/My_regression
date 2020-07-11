import csv
import os
import random
from collections import namedtuple
from datetime import datetime
import pytest
import xlrd
from webdriver_manager.chrome import ChromeDriverManager

from Regression.Inbound.Inbound_Enrollments_promo_APPLE_xlsx_test.InboundPromo_tests_Settings import *
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_xlsx_test._helpers.Inbound_BrandPage import BrandPage
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_xlsx_test._helpers.Inbound_accountNO_generator import account_generator_accountNo_1, \
    account_generator_accountNo_2, servicereference_generator
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_xlsx_test._helpers.Inbound_generator_names_and_address import generaot_names_and_address_work
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_xlsx_test._helpers.Inbound_generator_zip_city import generator_zip_city
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_xlsx_test._helpers.Inbound_loginPage import LoginPage
# from Regression.Inbound.Inbound_Enrollments_promo_test.InboundPromo_tests_Settings import tester, chosen_driver, workbook_name, \
#     start_string, \
#     data_sheet_name, start_page, test_name
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_xlsx_test._helpers.Inbound_pages_methods import *
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_xlsx_test._helpers.Inbound_tags import *

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


def grab_code(payload):
    global confcode
    wait_grab_code_page(driver)

    try:
        confcode = driver.find_element_by_id("confcode").text
    except:
        pass

    if payload.emailmarketing =='emailmarketing':
        driver.find_element_by_id('toggle_xsell_consent_yes').click()
    else:
        pass


    now = datetime.now()
    date = now.strftime("_%m_%d_%Y_")
    csv_filename="./c_web_test_result/_Inbound" + test_name + date + "_passed_tests_results.csv"


    if os.path.isfile(csv_filename):
        f = open(csv_filename, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(
            [payload.ts, 	payload.PremiseType, 	payload.sku, 	payload.BrandSlug, 	payload.ChannelSlug,
             payload.ProductName, 	payload.TermsOfServiceTyp, 	payload.city_check, 	str("'" + str(payload.account_no)),
             payload.first_name, 	payload.last_name, 	payload.UtilitySlug, 	payload.Commodity,
             payload.ServiceAddress1, 	payload.ServiceAddress2, 	payload.city, 	payload.StateSlug, 	str("'" + str(payload.zip_code)),
             payload.email, 	payload.emailmarketing, date_, confcode, "Passed"])

    else:
        f = open(csv_filename, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(
            ['ts', 	'PremiseType', 	'sku', 	'BrandSlug', 	'ChannelSlug',
             'ProductName', 	'TermsOfServiceTyp', 	'city_check', 	'account_no',
             'first_name', 	'last_name', 	'UtilitySlug', 	'Commodity',
             'ServiceAddress1', 	'ServiceAddress2', 	'city', 	'StateSlug', 	'zip_code',
             'email', 	'emailmarketing', "test_date", "conf_code", "web_status"])
        csv_a.writerow(
            [payload.ts, 	payload.PremiseType, 	payload.sku, 	payload.BrandSlug, 	payload.ChannelSlug,
             payload.ProductName, 	payload.TermsOfServiceTyp, 	payload.city_check, 	 str(payload.account_no),
             payload.first_name, 	payload.last_name, 	payload.UtilitySlug, 	payload.Commodity,
             payload.ServiceAddress1, 	payload.ServiceAddress2, 	payload.city, 	payload.StateSlug, 	str("'" + str(int(payload.zip_code))),
             payload.email, 	payload.emailmarketing, date_, confcode, "Passed"])

@pytest.mark.parametrize("payload", tests_values, ids=[p.ts for p in tests_values])
def test_state(test_setup, payload):
    now = datetime.now()
    time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")

    try:
        Inbound_start_test(driver, payload)
    except Exception as ae:
        filename = ("./failed/" + sheet_name + "_fail_{}_{}.png").format(payload.ts, time)
        driver.get_screenshot_as_file(filename)
        print("Saving screenshot of failed test -- ", payload.ts)
        print("filename:", filename)
        print(str(ae))

        now = datetime.now()
        date = now.strftime("_%m_%d_%Y_")

        f = open("./b_files_for_testing_02/_" + test_name + date + "_FAILED_tests_results.csv", 'a', newline='')
        now = datetime.now()
        # time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
        csv_a = csv.writer(f)
        # address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generaot_names_and_address_work()
        csv_a.writerow(
            [payload.ts, 	payload.PremiseType, 	payload.sku, 	payload.BrandSlug, 	payload.ChannelSlug,
             payload.ProductName, 	payload.TermsOfServiceTyp, 	payload.city_check, 	str(payload.account_no),
             payload.first_name, 	payload.last_name, 	payload.UtilitySlug, 	payload.Commodity,
             payload.ServiceAddress1, 	payload.ServiceAddress2, 	payload.city, 	payload.StateSlug, 	str("'" + str(int(payload.zip_code))),
             payload.email, 	payload.emailmarketing, date_,  "Failed"])
        raise ae


def Inbound_start_test(test_setup, payload):

    global promo_code, campaign_code
    servicereference = random.randint(80000,89999)


    if driver.current_url == start_page:
        pass
    else:
        driver.get("http://www.pt.energypluscompany.com/myinbound/tab_brand.php")
        print(URL)
        # Login page
        login = LoginPage(driver)
        login.fill_login()

    # Brand page
    choose_brand = BrandPage(driver)
    choose_brand.click_NRG_brand()
    choose_brand.click_save_and_continue_button()

    # Get Started page  :
    wait_get_started_page(driver)
    # May I please have your name?
    fill_get_started_page(payload)

    #Offer page:

    wait_offer_page(driver)
    time.sleep(2)
    #PROMO

    if payload.ProductName == 'Electric Choice Ohio Plan 3M':
        campaign_code ='7939'
    elif payload.ProductName == 'Electric Choice Ohio Plan 6M':
        campaign_code ='7946'
    elif payload.ProductName == 'Electric Choice Ohio Plan 12M':
        campaign_code = '7947'


    driver.find_element_by_xpath(offer_promo_partner_xpath).send_keys(partner)
    driver.find_element_by_xpath(offer_promo_Campaign_xpath).send_keys(campaign_code)
    driver.find_element_by_xpath(offer_promo_Promo_xpath).send_keys(promo)
    driver.find_element_by_xpath(offer_submit_promoCode_xpath).click()

    wait_PROMO_OfferPlans_page(driver)
    driver.find_element_by_name(continue_button_name).click()


    #Costomer Info page:

    wait_costumer_info_page(driver)

    elem = driver.find_element_by_name(customer_firs_name_name).send_keys(payload.first_name)
    elem = driver.find_element_by_name(customer_last_name_name).send_keys(payload.last_name)
    elem = driver.find_element_by_name(customer_service_address_1_name).send_keys(payload.ServiceAddress1)
    elem = driver.find_element_by_name(customer_service_address_2_name).send_keys(payload.ServiceAddress2)
    elem = driver.find_element_by_name(customer_city_name).send_keys(payload.city)
    elem = driver.find_element_by_name(customer_zip_name).send_keys(str(payload.zip_code))

    elem = driver.find_element_by_name(customer_phone_area_code_name).send_keys(phone_area_code_generated)
    elem = driver.find_element_by_name(customer_prefix_name).send_keys(phone_prefix_generated)
    elem = driver.find_element_by_name(customer_last_digit_name).send_keys(phone_last_generated)

    account_number = (payload.account_no.replace("'", ''))
    elem = driver.find_element_by_class_name(customer_uan_name).send_keys(account_number)

    if payload.StateSlug == 'Massachusetts':
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

    time.sleep(2)
    try:
        elem = driver.find_element_by_id(continue_button_id).click()
    except:
        pass

    # Billing Info:
    wait_billing_page(driver)
    fill_billing_info_page(payload)

    # ## Summary:
    summary(driver)


    # ## Disclosure:
    declouser_NRG(driver, payload)

    #Grab Conformation Code
    grab_code(payload)

    ## Submit        #################################################################################:
    try:
        elem = driver.find_element_by_id(submit_enroll_id).click()
    except:
        pass
    #
    wait_finish_page(driver)
    driver.find_element_by_id(start_new_call_id).click()

def fill_billing_info_page(payload):

    elem = driver.find_element_by_name(billing_address_name).send_keys(payload.ServiceAddress1)
    elem = driver.find_element_by_name(billing_address_name_2).send_keys(payload.ServiceAddress2)
    elem = driver.find_element_by_name(billing_city_name).send_keys(payload.city)
    elem = driver.find_element_by_class_name(billing_state_class_name)

    for option in elem.find_elements_by_tag_name(options_tag_name):
        if option.text == payload.StateSlug:
            option.click()
    elem = driver.find_element_by_name(billing_zip_name).send_keys(str(payload.zip_code))
    elem = driver.find_element_by_name(billing_phone_area_code_name).send_keys(phone_area_code_generated)
    elem = driver.find_element_by_name(billing_phone_prefix_area_name).send_keys(phone_prefix_generated)
    elem = driver.find_element_by_name(billing_phone_last_digits_name).send_keys(phone_last_generated)

    if payload.emailmarketing == 'emailmarketing':
        email_no_buttons = driver.find_elements_by_class_name(billing_email_yes_class_name)
        for x in range(0, len(email_no_buttons)):
            if email_no_buttons[x].is_displayed():
                email_no_buttons[x].click()
        time.sleep(1)
        driver.find_element_by_name(billing_email_name).send_keys(payload.email)

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


def fill_get_started_page(payload):
    driver.find_element_by_id(get_started_First_name_id).send_keys(payload.first_name)
    driver.find_element_by_id(get_started_last_name_id).send_keys(payload.last_name)
    print(payload.UtilitySlug)
    z=payload.UtilitySlug
    wait_get_started_page_state_list(driver)
    # What state are you are calling from?
    elem = driver.find_element_by_name(get_started_state_list_id)
    for option in elem.find_elements_by_tag_name(options_tag_name):
        if option.text == payload.StateSlug:
            option.click()
    # Is Your Name on the Utility Bill?
    if payload.StateSlug == "Maryland":
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

    if payload.UtilitySlug == 'ace':
        utility = 'Atlantic City Electric'
    if payload.UtilitySlug == 'aepn':
        utility = 'AEP Ohio'
    if payload.UtilitySlug == 'aeps':
        utility = 'AEP Ohio'
    if payload.UtilitySlug == 'Ameren':
        utility = 'Ameren'
    if payload.UtilitySlug == 'apmd':
        utility = 'Potomac Edison'
    if payload.UtilitySlug == 'beco':
        utility = 'Eversource (Eastern Massachusetts)'
    if payload.UtilitySlug == 'bge':
        utility = 'BGE'
    if payload.UtilitySlug == 'camb':
        utility = 'camb'
    if payload.UtilitySlug == 'CEI':
        utility = 'The Illuminating Company'
    if payload.UtilitySlug == 'come':
        utility = 'come'
    if payload.UtilitySlug == 'Comed':
        utility = 'ComEd'
    if payload.UtilitySlug == 'delmarva':
        utility = 'Delmarva Power'
    if payload.UtilitySlug == 'dpl':
        utility = 'Dayton Power & Light'
    if payload.UtilitySlug == 'dukeoh':
        utility = 'Duke Energy Ohio'
    if payload.UtilitySlug == 'duq':
        utility = 'Duquesne Light Company'
    if payload.UtilitySlug == 'jcpl':
        utility = 'Jersey Central Power & Light (JCP&L)'
    if payload.UtilitySlug == 'meco':
        utility = 'National Grid'
    if payload.UtilitySlug == 'meted':
        utility = 'Met-Ed'
    if payload.UtilitySlug == 'ngntkt':
        utility = 'ngntkt'
    if payload.UtilitySlug == 'OE':
        utility = 'Ohio Edison'
    if payload.UtilitySlug == 'peco':
        utility = 'PECO'
    if payload.UtilitySlug == 'penelec':
        utility = 'Penelec'
    if payload.UtilitySlug == 'penn':
        utility = 'Penn Power'
    if payload.UtilitySlug == 'pepco':
        utility = 'Pepco'
    if payload.UtilitySlug == 'ppl':
        utility = 'PPL Electric Utilities'
    if payload.UtilitySlug == 'pseg':
        utility = 'PSE&G'
    if payload.UtilitySlug == 'RECO':
        utility = 'Rockland Electric Company (O&R)'
    if payload.UtilitySlug == 'te':
        utility = 'Toledo Edison'
    if payload.UtilitySlug == 'wmeco':
        utility = 'Eversource (Western Massachusetts)'
    if payload.UtilitySlug == 'wpp':
        utility = 'West Penn Power'

    if payload.UtilitySlug == 'aeps':
        for option in elem.find_elements_by_tag_name(options_tag_name):
            c=option.text
            if option.text == 'AEP Ohio':
                option.click()
    else:
        for option in elem.find_elements_by_tag_name(options_tag_name):
                if option.text == utility:
                    option.click()

    # Is this electric account a residential or business address?try:
    try:
        if payload.PremiseType.lower() == 'residential':
            elem = driver.find_element_by_class_name(get_started_resident_class_name).click()
        elif payload.PremiseType.lower() == 'business':
            elem = driver.find_element_by_class_name(get_started_business_class_name).click()
    except:
        pass


    if payload.PremiseType.lower() == "residential":
        Residentials_buttons = driver.find_elements_by_class_name('account-type-residential')
        for x in range(0, len(Residentials_buttons)):
            if Residentials_buttons[x].is_displayed():
                Residentials_buttons[x].click()
    elif payload.PremiseType.lower() == "business":
        Business_buttons = driver.find_elements_by_class_name('account-type-business')
        for x in range(0, len(Business_buttons)):
            if Business_buttons[x].is_displayed():
                Business_buttons[x].click()


    # Save and continue button
    elem = driver.find_element_by_id(get_started_save_and_con_but_id).click()


