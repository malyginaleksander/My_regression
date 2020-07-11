import csv
from collections import namedtuple
from datetime import datetime
import pytest
import xlrd
from webdriver_manager.chrome import ChromeDriverManager


from Regression.Migration.GME_Migration.helpers.accountNO_generator import servicereference_generator, \
    account_generator_accountNo_1
from Regression.Migration.GME_Migration.helpers.generator import find_zip_city
from Regression.Migration.GME_Migration.helpers.generator_names_and_address import generator_names_and_address_work
from Regression.Inbound.States.Inbound_Enrollments_4brands_test.Inbound_BrandPage import BrandPage
from Regression.Migration.GME_Migration.Inbound_Enrollments_4brands_test.InboundEnrollments_tests_Settings import *
from Regression.Inbound.States.Inbound_Enrollments_4brands_test.Inbound_loginPage import *
from Regression.Inbound.States.Inbound_Enrollments_4brands_test.Inbound_pages_methods import *
from Regression.Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags import *

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


def grab_code(accountNo_1, payload):
    wait_grab_code_page(driver)
    elem = driver.find_element_by_id("confcode")
    confcode = elem.text
    # print(
    #     "Passed " + " " + payload.test_name + ", Conformation =  " + confcode + ' for ' + payload.state + ' - ' + payload.utility_1)
    # city, generated_zipCode = generator_zip_city(payload)
    f = open("./Inbound_Enrollments_tests_results.csv", 'a', newline='')
    now = datetime.now()
    time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
    csv_a = csv.writer(f)
    address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = names_and_address_generator()
    csv_a.writerow(
        ["Passed",  time, payload.test_name, payload.brand, payload.account_type_1, payload.account_type_2,
         payload.first_name,
         first_name_generated, last_name_generated, payload.state, payload.city, payload.utility_1, payload.partner_1,
         payload.campaign_1, payload.categorie_1,
         payload.promo_1, payload.zip, str("'" + str(accountNo_1)), confcode])


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
        # city, generated_zipCode = generator_zip_city(payload)
        f = open("./Inbound_Enrollments_tests_results.csv", 'a', newline='')
        now = datetime.now()
        time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
        csv_a = csv.writer(f)
        address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = names_and_address_generator()
        csv_a.writerow(
            ["FAILED",  time, payload.test_name, payload.brand, payload.account_type_1, payload.account_type_2,
             payload.first_name,
             first_name_generated, last_name_generated, payload.state, payload.city, payload.utility_1, payload.partner_1,
             payload.campaign_1, payload.categorie_1,
             payload.promo_1, payload.zip, " ", " "])
        raise ae


def Inbound_start_test(test_setup, payload):

    address_house_street_generated, first_name_generated, last_name_generated, \
    phone_area_code_generated, phone_last_generated, phone_prefix_generated= generator_names_and_address_work()
    generated_zipCode,generated_city = find_zip_city(payload.UtilitySlug, payload.StateSlug)
    accountNo_1 = account_generator_accountNo_1(payload.UtilitySlug)

    servicereference = servicereference_generator(payload)


    if driver.current_url == start_page:
        pass
    else:
        driver.get(URL)
        ###         Login page        #################################################################################
        login = LoginPage(driver)
        login.fill_login()
    ###         Brand page        #################################################################################
    choose_brand = BrandPage(driver)
    if payload.BrandSlug == Energy_plus :
        choose_brand.click_EP_brand()
    elif payload.BrandSlug == NRG:
        choose_brand.click_NRG_brand()
    elif payload.BrandSlug == Green_ME:
        choose_brand.click_GME_brand()
    elif payload.BrandSlug == Cirro:
        choose_brand.click_Cirro_brand()
    choose_brand.click_save_and_continue_button()

    ### Get Started page       #################################################################################:
    wait_get_started_page(driver)
    # May I please have your name?
    fill_get_started_page(payload)

    ###     Offer page           #################################################################################:

    wait_offer_page(driver)
    time.sleep(2)

    fill_offer_page(payload)

    ## Customer Info page        #################################################################################:

    global ServiceAddress1
    if len(payload.zip_code)>0:
        try:
            generated_zipCode_ = payload.zip_code.replace("'", '')
        except:
            generated_zipCode_=payload.zip
        b=generated_zipCode_
        if len (str(generated_zipCode))==4:
            zipCode = str("0")+str(generated_zipCode)
        else:
            zipCode = generated_zipCode_
    else:
        zipCode=generated_zipCode


    if len(payload.account_no) > 0:
        accountNo = payload.account_no
    else:
        given_utiity = payload.UtilitySlug
        accountNo = str(account_generator_accountNo_1(given_utiity))

    try:
        account_number = (accountNo.replace("'", ''))
    except:
        account_number = accountNo

    if len(payload.city)>0:
        city = payload.city
    else:
        city =   generated_city


    if len(payload.first_name) > 0:
        first_name = payload.first_name
    else:
        first_name = first_name_generated

    if len(payload.last_name) > 0:
        last_name = payload.UtilitySlug
    else:
        last_name = payload.UtilitySlug

    if len(payload.ServiceAddress1) > 0:
        ServiceAddress1 = payload.ServiceAddress1
    else:
        ServiceAddress1 = address_house_street_generated

    if len(payload.account_no) > 0:
        accountNo = payload.account_no
    else:
        given_utiity = payload.UtilitySlug
        accountNo = str(account_generator_accountNo_1(given_utiity))

    if len(payload.email) > 0:
        email_given = payload.email
    else:
        email_given = str(first_name) + str(last_name) + "@nrg.com"

    phone_number = (str(phone_area_code_generated) + str(phone_last_generated) + str(phone_prefix_generated))


    wait_costumer_info_page(driver)
    elem = driver.find_element_by_name(customer_firs_name_name).send_keys(first_name)
    elem = driver.find_element_by_name(customer_last_name_name).send_keys(last_name)
    elem = driver.find_element_by_name(customer_service_address_1_name).send_keys(ServiceAddress1)
    elem = driver.find_element_by_name(customer_city_name).send_keys(city)
    elem = driver.find_element_by_name(customer_zip_name).send_keys(zip)
    elem = driver.find_element_by_name(customer_phone_area_code_name).send_keys(phone_area_code_generated)
    elem = driver.find_element_by_name(customer_prefix_name).send_keys(phone_prefix_generated)
    elem = driver.find_element_by_name(customer_last_digit_name).send_keys(phone_last_generated)

    try:
        # if payload.brand == Energy_plus:
        #     if payload.account_type_2 == "Gas":
        #         elem = driver.find_element_by_xpath(costumer_ElectricPodId_input_xpath).send_keys(account_number)
        #         elem = driver.find_element_by_xpath(costumer_GasPodId_input_xpath).send_keys(str(zipCode))
        #         elem = driver.find_element_by_class_name(SameAsFirst_button_name).click()
        #         elem = driver.find_element_by_xpath(costumer_billing_the_samecervice_address_xpath).click()
        #         elem = driver.find_element_by_xpath(costumer_CheckElectricPoDID_buttn_xpath).click()
        #
        #
        #     elif payload.account_type_2 == "Electric":
        #         time.sleep(1)
        #         elem = driver.find_element_by_class_name(SameAsFirst_button_name).click()
        #
        #         try:
        #             driver.find_element_by_xpath(costumer_PECOAccountNumber_input_xpath).send_keys(accountNo_1)
        #
        #             driver.find_element_by_xpath(costumer_PECOAccountNumber_button_xpath).click()
        #         except:
        #             pass
        #         try:
        #             driver.find_element_by_xpath(costumer_PPL_EU_AcNum_input_xpath).send_keys(
        #                 int(accountNo_2))
        #             driver.find_element_by_xpath(costumer_PPL_EU_AcNum_checkButton_xpath).click()
        #         except:
        #             pass
        #
        #         elem = driver.find_element_by_class_name(costumer_UAN_class_name).send_keys(accountNo_1)
        #         elem = driver.find_element_by_class_name(customer_check_account_number_namber_name).click()
        #         elem = driver.find_element_by_xpath(costumer_PPL_EU_AcNum_input_xpath).send_keys(
        #             int(payload.accountNo_el_2))
        #         elem = driver.find_element_by_xpath(costumer_PPL_EU_AcNum_checkButton_xpath).click()

        if payload.BrandSlug == Green_ME:
            if payload.UtilitySlug == 'meted' or payload.utility_1 == 'peco':
                elem = driver.find_element_by_class_name(costumer_UAN_class_name).send_keys(accountNo)
            # elif payload.UtilitySlug == 'Philadelphia Gas Works':
            #     driver.find_element_by_xpath(costumer_ServicePointID_input_Xpath).send_keys(int(accountNo_1))
            #     driver.find_element_by_xpath(costumer_PGW_Account_input_xpath).send_keys(int(accountNo_1))
            #     driver.find_element_by_xpath(costumer_PGW_BillingAccount_input_xpath).send_keys(int(accountNo_1))

        # if payload.account_type_2 == "Gas" or payload.account_type_2 == "Electric":
        #     try:
        #         elem = driver.find_element_by_name(customer_customer_key_name).send_keys(costumer_key_TEXT)
        #         elem = driver.find_element_by_class_name(customer_check_extra_number_class_name).click()
        #         time.sleep(2)
        #     except:
        # #         pass
        #
        #     elem = driver.find_element_by_class_name(SameAsFirst_button_name).click()
        # #     driver.find_element_by_xpath(costumer_2nd_AcNo_inter_xpath).send_keys(accountNo_2)
        #
        # if payload.brand == NRG_regression:
        #     if payload.utility_1 == 'Philadelphia Gas Works':
        #         driver.find_element_by_xpath(costumer_ServicePointID_input_Xpath).send_keys(int(accountNo_1))
        #         driver.find_element_by_xpath(costumer_PGW_Account_input_xpath).send_keys(int(accountNo_1))
        #         driver.find_element_by_xpath(costumer_PGW_BillingAccount_NRG_input_xpath).send_keys(
        #             int(servicereference))
        #
        #     if payload.account_type_2 == "Gas":
        #         elem = driver.find_element_by_class_name(costumer_UAN_class_name).send_keys(accountNo_1)
        #         time.sleep(2)
        #         driver.find_element_by_class_name(SameAsFirst_button_name).click()
        #         driver.find_element_by_xpath(costumer_billing_the_samecervice_address_xpath).click()
        #         driver.find_element_by_xpath(costumer_AcNO_input_xpath).send_keys(int(accountNo_2))
        #     else:
        #         pass
        # elem = driver.find_element_by_class_name(customer_uan_name).send_keys(accountNo_1)


    except:
        elem = driver.find_element_by_class_name(customer_copy_to_billing_yes_name).click()
        elem = driver.find_element_by_class_name(customer_uan_name).send_keys(accountNo)

    if payload.StateSlug == 'Massachusetts':
        try:
            elem = driver.find_element_by_name(customer_customer_key_name).send_keys("test")
            driver.find_element_by_xpath(customer_servicereference_xpath).send_keys(int(servicereference))
            time.sleep(2)
        except:
            pass
    # if payload.type == 'Business':
    #     # Can you please tell me your average monthly usage in kWH
    #     try:
    #         elem = driver.find_element_by_xpath(costumer_AverageUsage_xpath)
    #         for option in elem.find_elements_by_tag_name(options_tag_name):
    #             if option.text == payload.monthly_usage:
    #                 option.click()
    #     except:
    #         pass
    time.sleep(1)
    try:
        Check_buttons = driver.find_elements_by_xpath(costumer_CheckButtons_xpath)
        for x in range(0, len(Check_buttons)):
            if Check_buttons[x].is_displayed():
                Check_buttons[x].click()
    except:
        pass
    # WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element_value(By.XPATH, "//span[@class='account-uan-span']/following-sibling::div/span"), "Valid!")

    time.sleep(6)
    try:
        elem = driver.find_element_by_id(continue_button_id).click()
    except:
        pass
    try:
        elem = driver.find_element_by_name(continue_button_id).click()
    except:
        pass
    ## Billing Info        #################################################################################:
    wait_billing_page(driver)
    fill_billing_info_page(address_house_street_generated, first_name_generated, last_name_generated, \
    phone_area_code_generated, phone_last_generated, phone_prefix_generated, generated_zipCode,generated_city,accountNo_1,
                          servicereference, zipCode,   payload )

    ## Summary:
    summary(driver)

    ## Disclosure:
    if start_page == start_page:
        declouser_GreenME_(driver)
    elif payload.brand == Green_ME:
            declouser_GreenME(driver)
    elif payload.brand == NRG:
        declouser_NRG(driver)
    else:
        declouser_EP(driver)

    ## Grab Conformation Code        #################################################################################:

    grab_code(accountNo_1, payload)

    ## Submit        #################################################################################:
    try:
        elem = driver.find_element_by_id(submit_enroll_id).click()
    except:
        pass

    wait_finish_page(driver)
    driver.find_element_by_id(start_new_call_id).click()


def fill_billing_info_page(address_house_street_generated, first_name_generated, last_name_generated, \
    phone_area_code_generated, phone_last_generated, phone_prefix_generated, generated_zipCode,generated_city,accountNo_1,
                          servicereference, zipCode,   payload):
    # if payload.type == 'Business':
    #     try:
    #         driver.find_element_by_xpath(billing_businessName_radio_yes_xpath).click()
    #         driver.find_element_by_xpath(billing_businessName_xpath).send_keys(
    #             "Tester_busines_account")
    #     except:
    #         pass
    elem = driver.find_element_by_name(billing_address_name).send_keys(ServiceAddress1)
    elem = driver.find_element_by_name(billing_city_name).send_keys(payload.city)
    elem = driver.find_element_by_class_name(billing_state_class_name)
    for option in elem.find_elements_by_tag_name(options_tag_name):
        if option.text == payload.StateSlug:
            option.click()
    elem = driver.find_element_by_name(billing_zip_name).send_keys(str(zipCode))
    elem = driver.find_element_by_name(billing_phone_area_code_name).send_keys(
        phone_area_code_generated)
    elem = driver.find_element_by_name(billing_phone_prefix_area_name).send_keys(
        phone_prefix_generated)
    elem = driver.find_element_by_name(billing_phone_last_digits_name).send_keys(
        phone_last_generated)

    if payload.email == "emailmarketing" or payload.email == "bouncedmail":
        driver.find_elements_by_class_name(billing_phone_email_yes_class_name).click()
        driver.find_element_by_xpath('//*[@class="billing-email required"]').send_keys(payload.email)


    # for x in range(0, len(email_no_buttons)):
    #     if email_no_buttons[x].is_displayed():
    #         email_no_buttons[x].click()

    # email_no_buttons = driver.find_elements_by_class_name(billing_phone_email_no_no_class_name)
    # for x in range(0, len(email_no_buttons)):
    #     if email_no_buttons[x].is_displayed():
    #         email_no_buttons[x].click()

    # if payload.account_type_2 == "Electric" or payload.account_type_2 == "Gas":
    #     driver.find_element_by_class_name(SameAsFirst_button_name).click()

    elem = driver.find_element_by_id(continue_button_id).click()
    time.sleep(2)


def fill_offer_page(payload):
    if payload.BrandSlug == Green_ME:
        try:
            fill_greenME_offer(payload)
        except:
            pass
    #     try:
    #         driver.find_element_by_xpath(offer_greenME_first_search_xpath).send_keys(payload.categorie_1)
    #         driver.find_element_by_id(payload.categorie_1).click()
    #     except:
    #         pass
    # if payload.brand == NRG_regression:
    #     wait_offer_page(driver)
    #
    #     try:
    #         driver.find_element_by_xpath(offer_search_xpath).send_keys(payload.categorie_1)
    #         driver.find_element_by_id(payload.categorie_1).click()
    #     except:
    #         try:
    #             elem = driver.find_element_by_id(payload.categorie_1).click()
    #         except:
    #             pass
    #
    #     if payload.account_type_2 == "Gas":
    #         driver.find_element_by_xpath(offer_second_).send_keys(payload.categorie_2)
    #         driver.find_element_by_id(payload.categorie_2).click()
    if payload.TermsOfServiceType.upper() == 'Variable'.upper():
        try:
            Variable_buttons = driver.find_elements_by_xpath(offer_Varriable_choise_xpath)
            for x in range(0, len(Variable_buttons)):
                if Variable_buttons[x].is_displayed():
                    Variable_buttons[x].click()
        except:
            pass
    elif payload.TermsOfServiceType.upper()  == 'Fixed'.upper():
        try:
            Fixed_buttons = driver.find_elements_by_xpath(offer_Fixed_choise_xpath)
            for x in range(0, len(Fixed_buttons)):
                if Fixed_buttons[x].is_displayed():
                    Fixed_buttons[x].click()
        except:
            pass

    # else:
    #     try:
    #         elem = driver.find_element_by_xpath(offer_select_category_1_xpath)
    #         for option in elem.find_elements_by_tag_name(options_tag_name):
    #             if option.text == payload.categorie_1:
    #                 option.click()
    #             elem = driver.find_element_by_class_name(offer_partner_class_name)
    #         for option in elem.find_elements_by_tag_name(options_tag_name):
    #             if option.text == payload.partner_1:
    #                 option.click()
    #         elem = driver.find_element_by_class_name(offer_campaigns_class_name)
    #         for option in elem.find_elements_by_tag_name(options_tag_name):
    #             if option.text == payload.campaign_1:
    #                 option.click()
    #         elem = driver.find_element_by_class_name(offer_campaigns_promos_name)
    #         for option in elem.find_elements_by_tag_name(options_tag_name):
    #             if option.text == payload.promo_1:
    #                 option.click()
    #     except:
    #         pass
    # todo do we need sleep?
    time.sleep(2)
    # Green option
    # if payload.brand == Energy_plus :
    #     if payload.account_type_1 == 'Electric' or payload.account_type_2 == 'Electric':
    #         if payload.green_opt == "yes":
    #             elem = driver.find_element_by_id(offer_green_opt_yes).click()
    #         elif payload.green_opt == "no":
    #             elem = driver.find_element_by_id(offer_green_opt_no).click()
    # try:
    #     Check_buttons = driver.find_elements_by_xpath(costumer_CheckButtons_xpath)
    #     for x in range(0, len(Check_buttons)):
    #         if Check_buttons[x].is_displayed():
    #             Check_buttons[x].click()
    # except:
    #     pass
    # # Todo - finish wait
    # time.sleep(1)
    try:
        elem = driver.find_element_by_id(continue_button_id).click()
    except:
        pass
    if payload.BrandSlug == Green_ME or payload.BrandSlug == NRG or payload.BrandSlug == Cirro:
        try:
            driver.find_element_by_name(continue_button_name).click()
        except:
            pass


def fill_get_started_page(payload):
    driver.find_element_by_id(get_started_First_name_id).send_keys("Tester_Alex")
    driver.find_element_by_id(get_started_last_name_id).send_keys("Tester_Malygin")
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
        if payload.Commodity.upper() == 'Electric'.upper():
            try:
                elem = driver.find_element_by_class_name(
                    get_call_account_electric_class_name).click()
            except:
                pass
        if payload.Commodity.upper() == 'Gas'.upper():
            try:
                elem = driver.find_element_by_class_name(get_call_account_gas_class_name).click()
            except:
                pass
    except:
        pass
    # Who is the provider for your electric account?
    if payload.Commodity.upper() == 'Electric'.upper():
        elem = driver.find_element_by_name(get_started_EL_utility_1_class_name)
        for option in elem.find_elements_by_tag_name(options_tag_name):
            if option.text.upper() == payload.UtilitySlug.upper():
                option.click()
    # if payload.Commodity.upper() == 'Gas'.upper():
    #     # try:
    #     #     elem= driver.find_element_by_xpath('//*[@id="get-started-account-section"]/div[3]/select')
    #     #     for option in elem.find_elements_by_tag_name(options_tag_name):
    #     #         print(option.text)
    #     #         print(option.text + " " + payload.utility_1)
    #     #         if option.text == payload.utility_1:
    #     #             option.click()
    #     # except:
    #     #     pass
    #     try:
    #         elem = driver.find_element_by_xpath(get_started_Gas_utility_1_xpath)
    #         for option in elem.find_elements_by_tag_name(options_tag_name):
    #             if option.text == payload.utility_1:
    #                 option.click()
    #     except:
    #         elem = driver.find_element_by_xpath(get_started_Gas_utility_NJ_xpath)
    #         for option in elem.find_elements_by_tag_name(options_tag_name):
    #             if option.text == payload.utility_1:
    #                 option.click()
    # Is this electric account a residential or business address?try:
    try:
        if payload.PremiseType.upper() == 'Residential'.upper():
            elem = driver.find_element_by_class_name(get_started_resident_class_name).click()
        elif payload.PremiseType.upper() == 'Business'.upper():
            elem = driver.find_element_by_class_name(get_started_business_class_name).click()
    except:
        pass


    if payload.PremiseType.upper() == 'Residential'.upper():
        Residentials_buttons = driver.find_elements_by_class_name('account-type-residential')
        for x in range(0, len(Residentials_buttons)):
            if Residentials_buttons[x].is_displayed():
                Residentials_buttons[x].click()

    if payload.PremiseType.upper() == "Business":
        Business_buttons = driver.find_elements_by_class_name('account-type-business')
        for x in range(0, len(Business_buttons)):
            if Business_buttons[x].is_displayed():
                Business_buttons[x].click()

    # if payload.account_type_1 == "Gas" or payload.account_type_2 == "Gas":
    #     if payload.gas_option == 'Heating Only':
    #         heating_buttons = driver.find_elements_by_class_name(get_started_gas_HeatingOnly_class_name)
    #         for x in range(0, len(heating_buttons)):
    #             if heating_buttons[x].is_displayed():
    #                 heating_buttons[x].click()
    #     if payload.gas_option == 'Cooking Only':
    #         cooking_buttons = driver.find_elements_by_class_name(get_started_gas_CookingOnly_class_name)
    #         for x in range(0, len(cooking_buttons)):
    #             if cooking_buttons[x].is_displayed():
    #                 cooking_buttons[x].click()
    #     if payload.gas_option == 'Both Heating & Cooking':
    #         both_buttons = driver.find_elements_by_class_name(get_started_gas_Both_class_name)
    #         for x in range(0, len(both_buttons)):
    #             if both_buttons[x].is_displayed():
    #                 both_buttons[x].click()

    if payload.BrandSlug == Green_ME and payload.StateSlug == 'New York':
        try:
            elem = driver.find_element_by_name("zone")
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == ("Westchester"):
                    option.click()
        except:
            pass
    # Save and continue button
    elem = driver.find_element_by_id(get_started_save_and_con_but_id).click()


def fill_greenME_offer(payload):

    driver.find_element_by_xpath("//input[@class='col-md-2 form-control ng-pristine ng-valid']").send_keys(payload.ProductName)
    driver.find_element_by_xpath('//*[@id="The Cash Back Plan"]/ul/li[2][1]').click()

