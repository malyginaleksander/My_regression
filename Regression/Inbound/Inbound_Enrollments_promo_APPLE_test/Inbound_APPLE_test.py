import csv
import os
import random
import pytest
from webdriver_manager.chrome import ChromeDriverManager

from Regression.Inbound.Inbound_Enrollments_promo_APPLE_test.InboundPromo_tests_Settings import *
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_test.helpers.Inbound_BrandPage import BrandPage
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_test.helpers.Inbound_accountNO_generator import \
    servicereference_generator
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_test.helpers.Inbound_loginPage import LoginPage
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_test.helpers.Inbound_pages_methods import *
from Regression.Inbound.Inbound_Enrollments_promo_APPLE_test.helpers.Inbound_tags import *










def grab_code(given_ts , 	given_PremiseType , 	given_sku , 	given_BrandSlug ,
              given_ChannelSlug , 	given_ProductName , 	given_TermsOfServiceTyp ,
              given_city_check , 	given_account_no , 	given_first_name , 	given_last_name ,
              given_UtilitySlug , 	given_Commodity , 	given_ServiceAddress1 , 	given_ServiceAddress2 ,
              given_city , 	given_StateSlug , 	given_zip_code , 	given_email , 	given_emailmarketing ,
              servicereference ):
    global confcode
    wait_grab_code_page(driver)

    try:
        confcode = driver.find_element_by_id("confcode").text
    except:
        pass

    if given_emailmarketing =='emailmarketing':
        driver.find_element_by_id('toggle_xsell_consent_yes').click()
    else:
        pass

    from datetime import datetime
    now = datetime.now()
    date = now.strftime("_%m_%d_%Y_")
    csv_filename="./b_files_for_testing_02/" + test_name + "_"+ date + "_tests_results.csv"


    if os.path.isfile(csv_filename):
        f = open(csv_filename, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(
            [ given_ts , 	given_PremiseType , 	given_sku , 	given_BrandSlug , 	given_ChannelSlug ,
              given_ProductName , 	given_TermsOfServiceTyp , 	given_city_check , 	str("'" + given_account_no) ,
              given_first_name , 	given_last_name , 	given_UtilitySlug , 	given_Commodity ,
              given_ServiceAddress1 , 	given_ServiceAddress2 , 	given_city , 	given_StateSlug ,
              str("'" + given_zip_code) , 	given_email , 	given_emailmarketing , 	servicereference ,
             confcode, 'passed'])
    else:
        f = open(csv_filename, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(
            ['ts', 	'PremiseType', 	'sku', 	'BrandSlug', 	'ChannelSlug', 	'ProductName',
             'TermsOfServiceTyp', 	'city_check', 	'account_no', 	'first_name', 	'last_name',
             'UtilitySlug', 	'Commodity', 	'ServiceAddress1', 	'ServiceAddress2', 	'city',
             'StateSlug', 	'zip_code', 	'email', 	'emailmarketing', 'confcode', 'web_status'])
        csv_a.writerow(
            [ given_ts , 	given_PremiseType , 	given_sku , 	given_BrandSlug , 	given_ChannelSlug ,
              given_ProductName , 	given_TermsOfServiceTyp , 	given_city_check , 	str("'" + given_account_no) ,
              given_first_name , 	given_last_name , 	given_UtilitySlug , 	given_Commodity ,
              given_ServiceAddress1 , 	given_ServiceAddress2 , 	given_city , 	given_StateSlug ,
              str("'" + given_zip_code) , 	given_email , 	given_emailmarketing , 	servicereference ,
             confcode,'passed' ])



def test_state():
    global driver
    global servicereference


    if chosen_driver == "firefox":
        driver = webdriver.Firefox()
    elif chosen_driver == "chrome":
        driver = webdriver.Chrome(ChromeDriverManager("2.36").install())
    else:
        driver = webdriver.Chrome(ChromeDriverManager("2.36").install())
    from datetime import datetime
    now = datetime.now()
    # time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
    input_file_dict = csv.DictReader(open(workbook_name))

    for row in input_file_dict:
        dict_ = row
        given_ts = dict_.get('ts', '')
        given_PremiseType = dict_.get('PremiseType', '')
        given_sku = dict_.get('sku', '')
        given_BrandSlug = dict_.get('BrandSlug', '')
        given_ChannelSlug = dict_.get('ChannelSlug', '')
        given_ProductName = dict_.get('ProductName', '')
        given_TermsOfServiceTyp = dict_.get('TermsOfServiceTyp', '')
        given_city_check = dict_.get('city_check', '')
        given_account_no = dict_.get('account_no', '')
        given_first_name = dict_.get('first_name', '')
        given_last_name = dict_.get('last_name', '')
        given_UtilitySlug = dict_.get('UtilitySlug', '')
        given_Commodity = dict_.get('Commodity', '')
        given_ServiceAddress1 = dict_.get('ServiceAddress1', '')
        given_ServiceAddress2 = dict_.get('ServiceAddress2', '')
        given_city = dict_.get('city', '')
        given_StateSlug = dict_.get('StateSlug', '')
        given_zip_code = dict_.get('zip_code', '')
        given_email = dict_.get('email', '')
        given_emailmarketing = dict_.get('emailmarketing', '')
        servicereference = servicereference_generator(given_UtilitySlug)

        phone_area_code_generated = random.randint(100, 999)
        phone_prefix_generated = random.randint(100, 999)
        phone_last_generated = random.randint(1000, 9999)

        if driver.current_url == start_page:
            pass
        else:
            driver.get("http://pt.energypluscompany.com/myinbound/tab_brand.php")
            print(URL)


        #LOGIN page
        login = LoginPage(driver)
        login.fill_login()

        #brand page
        choose_brand = BrandPage(driver)
        if given_BrandSlug == 'nrg_residential':
            choose_brand.click_NRG_brand()
        choose_brand.click_save_and_continue_button()


        # Get Started page
        wait_get_started_page(driver)
        # May I please have your name?
        fill_get_started_page(given_first_name, given_last_name, given_StateSlug, given_UtilitySlug, given_PremiseType)


        # Offer page
        wait_offer_page(driver)
        import time
        time.sleep(2)
        #PROMO
        driver.find_element_by_xpath(offer_promo_partner_xpath).send_keys(partner)
        driver.find_element_by_xpath(offer_promo_Campaign_xpath).send_keys(campaign)
        driver.find_element_by_xpath(offer_promo_Promo_xpath).send_keys(promo)
        driver.find_element_by_xpath(offer_submit_promoCode_xpath).click()

        wait_PROMO_OfferPlans_page(driver)
        driver.find_element_by_name(continue_button_name).click()


        # Customer Info page

        wait_costumer_info_page(driver)

        elem = driver.find_element_by_name(customer_firs_name_name).send_keys(given_first_name)
        elem = driver.find_element_by_name(customer_last_name_name).send_keys(given_last_name)
        elem = driver.find_element_by_name(customer_service_address_1_name).send_keys(given_ServiceAddress1)
        elem = driver.find_element_by_name(customer_service_address_2_name).send_keys(given_ServiceAddress2)
        elem = driver.find_element_by_name(customer_city_name).send_keys(given_city)
        elem = driver.find_element_by_name(customer_zip_name).send_keys(str(given_zip_code))

        elem = driver.find_element_by_name(customer_phone_area_code_name).send_keys(phone_area_code_generated)
        elem = driver.find_element_by_name(customer_prefix_name).send_keys(phone_prefix_generated)
        elem = driver.find_element_by_name(customer_last_digit_name).send_keys(phone_last_generated)

        elem = driver.find_element_by_class_name(customer_uan_name).send_keys(given_account_no)

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

        time.sleep(2)
        try:
            elem = driver.find_element_by_id(continue_button_id).click()
        except:
            pass

        # Billing Info
        wait_billing_page(driver)
        fill_billing_info_page(given_ServiceAddress1, given_ServiceAddress2,
                               given_city,  phone_area_code_generated, phone_last_generated, phone_prefix_generated,
                               given_zip_code, given_email, given_emailmarketing)

        # Summary:
        summary(driver)


        # Disclosure:
        declouser_NRG(driver)

        # Grab Conformation Code
        grab_code(given_ts, given_PremiseType, given_sku, given_BrandSlug,
                  given_ChannelSlug, given_ProductName, given_TermsOfServiceTyp,
                  given_city_check, given_account_no, given_first_name, given_last_name,
                  given_UtilitySlug, given_Commodity, given_ServiceAddress1, given_ServiceAddress2,
                  given_city, given_StateSlug, given_zip_code, given_email, given_emailmarketing,
                  servicereference)

        #Submit
        try:
            elem = driver.find_element_by_id(submit_enroll_id).click()
        except:
            pass
    #
        wait_finish_page(driver)
        driver.find_element_by_id(start_new_call_id).click()


def  fill_billing_info_page(given_ServiceAddress1, given_ServiceAddress2,
                               given_city,  phone_area_code_generated, phone_last_generated, phone_prefix_generated,
                               given_zip_code, given_email, given_emailmarketing):

    elem = driver.find_element_by_name(billing_address_name).send_keys(given_ServiceAddress1)
    elem = driver.find_element_by_name(billing_address_name_2).send_keys(given_ServiceAddress2)
    elem = driver.find_element_by_name(billing_city_name).send_keys(given_city)
    elem = driver.find_element_by_class_name(billing_state_class_name)
    for option in elem.find_elements_by_tag_name(options_tag_name):
        if option.text == given_city:
            option.click()
    elem = driver.find_element_by_name(billing_zip_name).send_keys(str(given_zip_code))
    elem = driver.find_element_by_name(billing_phone_area_code_name).send_keys(phone_area_code_generated)
    elem = driver.find_element_by_name(billing_phone_prefix_area_name).send_keys(phone_prefix_generated)
    elem = driver.find_element_by_name(billing_phone_last_digits_name).send_keys(phone_last_generated)

    if given_emailmarketing == 'emailmarketing':
        email_no_buttons = driver.find_elements_by_class_name(billing_email_yes_class_name)
        for x in range(0, len(email_no_buttons)):
            if email_no_buttons[x].is_displayed():
                email_no_buttons[x].click()
        time.sleep(1)
        driver.find_element_by_name(billing_email_name).send_keys(given_email)

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


def fill_get_started_page(given_first_name, given_last_name, given_StateSlug, given_UtilitySlug, given_PremiseType):
    driver.find_element_by_id(get_started_First_name_id).send_keys(tester + "_" + given_first_name)
    driver.find_element_by_id(get_started_last_name_id).send_keys(given_last_name)
    wait_get_started_page_state_list(driver)
    # What state are you are calling from?
    elem = driver.find_element_by_name(get_started_state_list_id)
    for option in elem.find_elements_by_tag_name(options_tag_name):
        if option.text == given_StateSlug:
            option.click()
    # Is Your Name on the Utility Bill?
    if given_StateSlug == "Maryland":
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
        if option.text == given_UtilitySlug:
            option.click()

    # Is this electric account a residential or business address?try:
    try:
        if given_PremiseType.upper() == 'residential':
            elem = driver.find_element_by_class_name(get_started_resident_class_name).click()
        elif given_PremiseType.upper() == 'Business':
            elem = driver.find_element_by_class_name(get_started_business_class_name).click()
    except:
        pass


    if  given_PremiseType.upper() == "Residential":
        Residentials_buttons = driver.find_elements_by_class_name('account-type-residential')
        for x in range(0, len(Residentials_buttons)):
            if Residentials_buttons[x].is_displayed():
                Residentials_buttons[x].click()

    if  given_PremiseType.upper() == "Business":
        Business_buttons = driver.find_elements_by_class_name('account-type-business')
        for x in range(0, len(Business_buttons)):
            if Business_buttons[x].is_displayed():
                Business_buttons[x].click()


    # Save and continue button
    elem = driver.find_element_by_id(get_started_save_and_con_but_id).click()


    driver.close()
    driver.quit()
    return driver

