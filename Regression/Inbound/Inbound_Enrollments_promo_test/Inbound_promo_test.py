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


Partner_base_list = []
Campaign_Code_base_list  = []
Promo_Code_base_list  = []
state_base_list  = []
account_type_1_base_list  = []



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
             payload.Utility, 	 payload.LP_Test_Confirmation_number, 	payload.SKU, promo_offer_portal_1,   "Passed",  ])


@pytest.mark.parametrize("payload", tests_values, ids=[p.ts for p in tests_values])
def test_state(test_setup, payload):
    now = datetime.now()
    time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")

    try:
        Inbound_start_test(driver, payload)
    except Exception as ae:
        filename = ("./failed/" + data_sheet_name + "_fail_{}_{}.png").format(payload.ts, time)
        driver.get_screenshot_as_file(filename)
        print("Saving screenshot of failed test -- ", payload.ts)
        print("filename:", filename)
        print(str(ae))
        city, generated_zipCode = generator_zip_city(payload)

        now = datetime.now()
        date = now.strftime("_%m_%d_%Y_")

        f = open("./outbox_files/" + test_name + date + "_tests_results.csv", 'a', newline='')
        now = datetime.now()
        time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
        csv_a = csv.writer(f)
        address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generaot_names_and_address_work()
        csv_a.writerow(
            [payload.ts, payload.state, 	payload.Partner, 	payload.Product, 	payload.account_type_1, 	payload.Bonus,
             payload.Ongoing_Earn, 	payload.Campaign_Code, 	payload.Promo_Code, 	payload.Slug, 	payload.URL,
             payload.utility_1, 	payload.LP_Test_Confirmation_number, 	payload.SKU," " , "failed",  ])
        raise ae


def Inbound_start_test(test_setup, payload):
    global promo2_account_type_1
    accountNo_1 = account_generator_accountNo_1(payload)
    address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generaot_names_and_address_work()
    first_name_generated_ = first_name_generated
    last_name_generated_ = last_name_generated
    servicereference = servicereference_generator(payload)
    # if payload.account_type_2 == 'Gas' or payload.account_type_2 == 'Electric':
    #     accountNo_2 = account_generator_accountNo_2(payload)
    # else:
    #     pass

    if driver.current_url == 'http://www.energypluscompany.com/myinbound/tab_offer_sku.php#/tab_offer_sku.php':
        driver.get('http://www.energypluscompany.com/myinbound/tab_brand.php')

    else:
        driver.get(URL)
        ###         Login page        #################################################################################
        login = LoginPage(driver)
        login.fill_login()
    ###         Brand page        #################################################################################
    choose_brand = BrandPage(driver)
    # if payload.brand == Energy_plus :
    #     choose_brand.click_EP_brand()
    # elif payload.brand == NRG_regression:
    choose_brand.click_NRG_brand()
    # elif payload.brand == Green_ME:
    #     choose_brand.click_GME_brand()
    # elif payload.brand == Cirro:
    #     choose_brand.click_Cirro_brand()
    choose_brand.click_save_and_continue_button()

    ### Get Started page       #################################################################################:
    wait_get_started_page(driver)
    # May I please have your name?
    fill_get_started_page(first_name_generated_, last_name_generated_, payload)

    ###     Offer page           #################################################################################:

    wait_offer_page(driver)
    # from datetime import datetime
    #
    # time.sleep(2)
#PROMO ##################################################################################################################
    driver.find_element_by_xpath(offer_promo_partner_xpath).send_keys(payload.Partner)
    driver.find_element_by_xpath(offer_promo_Campaign_xpath).send_keys(int(payload.Campaign_Code))
    driver.find_element_by_xpath(offer_promo_Promo_xpath).send_keys(str(payload.Promo_Code))
    driver.find_element_by_xpath(offer_submit_promoCode_xpath).click()

    import pandas as pd

    # promo_file = './inbox_files/promo_list.xlsx'
    # read_file = pd.read_excel(promo_file)
    # read_file.to_csv(promo_file_csv, index=None, header=True)



    # try:
    wait_PROMO_OfferPlans_page(driver)
    driver.find_element_by_xpath(offer_Promo_OfferCodePlansHead_xpath)
    elem = driver.find_element_by_xpath(offer_Promo_OfferCodePlansHead_xpath).text
    promo_offer_portal_1 = driver.find_element_by_xpath('//*[@id="category-* OFFER CODE PLANS"]/../../div/div[2]/ul/li[1]').text
    # fact_code = driver.find_element_by_xpath('//*[@id="category-* OFFER CODE PLANS"]/../../../div[2]/div/div/div/p[1]/strong[3]').text
    code_2 = driver.find_element_by_xpath("//*[@ng-show='category.title == offercodeCategory'][1]/p/strong[3]").text
    code_2_ = code_2.replace(" ", "")
    partner_2 = driver.find_element_by_xpath("//*[@ng-show='category.title == offercodeCategory'][1]/p/strong[1]").text
    partner_2_ = partner_2.replace(" ", "")
    campaign_2 = driver.find_element_by_xpath("//*[@ng-show='category.title == offercodeCategory'][1]/p/strong[2]").text
    campaign_2_ = campaign_2.replace(" ", "")


    # if fact_clean_code2 == payload.check_code:
    #     check_offer_status = "passed"
    # else:
    #     check_offer_status = "failed"
    # print(check_offer_status)


    if int(code_2_) ==int(payload.Promo_Code):
        check_offer_status = "is equal"
    else:
        check_offer_status = "NOT equal"
    print(check_offer_status)



    # if elem == '* OFFER CODE PLANS':
    # if len(elem) > 0:
    #     check_offer = "PROMO offer exists"
    # else:
    #     check_offer = "PROMO offer DOESN't exists"
    # print(check_offer)

    promo_file_csv = './inbox_files/promo_list.csv'

    input_file_sap = csv.DictReader(open(promo_file_csv))
    for row in input_file_sap:
            dict = row
            Partner_base = dict.get('Partner', '')
            Campaign_Code_base = dict.get('Campaign_Code', '')
            Promo_Code_base = dict.get('Promo_Code', '')
            state_base = dict.get('state', '')
            account_type_1_base = dict.get('account_type_1', '')

            if payload.state ==state_base and (partner_2_)== (Partner_base) and int(code_2_) == int(Promo_Code_base) \
                    and  int(campaign_2_) == int(Campaign_Code_base):
                            if payload.account_type_1 == account_type_1_base:
                                promo2_account_type_1 = account_type_1_base


                            else:
                                promo2_account_type_1 = account_type_1_base





    now = datetime.now()
    date = now.strftime("_%m_%d_%Y_")

    f = open("./outbox_files/" + test_name + date + "_tests_results.csv", 'a', newline='')
    time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
    csv_a = csv.writer(f)
    f = open("./outbox_files/" + test_name + date + "_tests_results.csv", 'a', newline='')
    csv_a.writerow(
            [payload.ts, payload.state, 	payload.Partner, 	payload.Product, 	payload.account_type_1, 	payload.Bonus,
             payload.Ongoing_Earn, payload.Partner,	int(payload.Campaign_Code), 	str("'")+str(payload.Promo_Code), 	payload.Slug, 	payload.URL,
             payload.utility_1, 	payload.LP_Test_Confirmation_number, 	payload.SKU, promo_offer_portal_1,
               partner_2_, campaign_2_,str("'")+str((code_2_)), check_offer_status, promo2_account_type_1 ])



       # driver.find_element_by_name(continue_button_name).click()

        # fill_offer_page(payload)

        # ## Customer Info page        #################################################################################::
        # wait_costumer_info_page(driver)
        # elem = driver.find_element_by_name(customer_firs_name_name).send_keys(tester + "_" + first_name_generated_)
        # elem = driver.find_element_by_name(customer_last_name_name).send_keys(last_name_generated_)
        # elem = driver.find_element_by_name(customer_service_address_1_name).send_keys(address_house_street_generated)
        # elem = driver.find_element_by_name(customer_city_name).send_keys(city)
        # elem = driver.find_element_by_name(customer_zip_name).send_keys(random_zip)
        # elem = driver.find_element_by_name(customer_phone_area_code_name).send_keys(phone_area_code_generated)
        # elem = driver.find_element_by_name(customer_prefix_name).send_keys(phone_prefix_generated)
        # elem = driver.find_element_by_name(customer_last_digit_name).send_keys(phone_last_generated)

        # try:
        #     if payload.brand == Energy_plus:
        #         if payload.account_type_2 == "Gas":
        #             elem = driver.find_element_by_xpath(costumer_ElectricPodId_input_xpath).send_keys(accountNo_1)
        #             elem = driver.find_element_by_xpath(costumer_GasPodId_input_xpath).send_keys(str(accountNo_2))
        #             elem = driver.find_element_by_class_name(SameAsFirst_button_name).click()
        #             elem = driver.find_element_by_xpath(costumer_billing_the_samecervice_address_xpath).click()
        #             elem = driver.find_element_by_xpath(costumer_CheckElectricPoDID_buttn_xpath).click()
        #
        #
        #         elif payload.account_type_2 == "Electric":
        #             time.sleep(1)
        #             elem = driver.find_element_by_class_name(SameAsFirst_button_name).click()
        #
        #             try:
        #                 driver.find_element_by_xpath(costumer_PECOAccountNumber_input_xpath).send_keys(accountNo_1)
        #
        #                 driver.find_element_by_xpath(costumer_PECOAccountNumber_button_xpath).click()
        #             except:
        #                 pass
        #             try:
        #                 driver.find_element_by_xpath(costumer_PPL_EU_AcNum_input_xpath).send_keys(
        #                     int(accountNo_2))
        #                 driver.find_element_by_xpath(costumer_PPL_EU_AcNum_checkButton_xpath).click()
        #             except:
        #                 pass
        #
        #             elem = driver.find_element_by_class_name(costumer_UAN_class_name).send_keys(accountNo_1)
        #             elem = driver.find_element_by_class_name(customer_check_account_number_namber_name).click()
        #             elem = driver.find_element_by_xpath(costumer_PPL_EU_AcNum_input_xpath).send_keys(
        #                 int(payload.accountNo_el_2))
        #             elem = driver.find_element_by_xpath(costumer_PPL_EU_AcNum_checkButton_xpath).click()
        #
        #     elif payload.brand == Green_ME:
        #         if payload.utility_1 == 'Met-Ed' or payload.utility_1 == 'PECO':
        #             elem = driver.find_element_by_class_name(costumer_UAN_class_name).send_keys(accountNo_1)
        #         elif payload.utility_1 == 'Philadelphia Gas Works':
        #             driver.find_element_by_xpath(costumer_ServicePointID_input_Xpath).send_keys(int(accountNo_1))
        #             driver.find_element_by_xpath(costumer_PGW_Account_input_xpath).send_keys(int(accountNo_1))
        #             driver.find_element_by_xpath(costumer_PGW_BillingAccount_input_xpath).send_keys(int(accountNo_1))
        #
        #     if payload.account_type_2 == "Gas" or payload.account_type_2 == "Electric":
        #         try:
        #             elem = driver.find_element_by_name(customer_customer_key_name).send_keys(costumer_key_TEXT)
        #             elem = driver.find_element_by_class_name(customer_check_extra_number_class_name).click()
        #             time.sleep(2)
        #         except:
        #             pass
        #
        #         elem = driver.find_element_by_class_name(SameAsFirst_button_name).click()
        #         driver.find_element_by_xpath(costumer_2nd_AcNo_inter_xpath).send_keys(accountNo_2)
        #
        #     if payload.brand == NRG_regression:
        #         if payload.utility_1 == 'Philadelphia Gas Works':
        #             driver.find_element_by_xpath(costumer_ServicePointID_input_Xpath).send_keys(int(accountNo_1))
        #             driver.find_element_by_xpath(costumer_PGW_Account_input_xpath).send_keys(int(accountNo_1))
        #             driver.find_element_by_xpath(costumer_PGW_BillingAccount_NRG_input_xpath).send_keys(
        #                 int(servicereference))
        #
        #         if payload.account_type_2 == "Gas":
        #             elem = driver.find_element_by_class_name(costumer_UAN_class_name).send_keys(accountNo_1)
        #             time.sleep(2)
        #             driver.find_element_by_class_name(SameAsFirst_button_name).click()
        #             driver.find_element_by_xpath(costumer_billing_the_samecervice_address_xpath).click()
        #             driver.find_element_by_xpath(costumer_AcNO_input_xpath).send_keys(int(accountNo_2))
        #         else:
        #             pass
        #     elem = driver.find_element_by_class_name(customer_uan_name).send_keys(accountNo_1)
        #
        #
        # except:
        #     elem = driver.find_element_by_class_name(customer_copy_to_billing_yes_name).click()
        #     elem = driver.find_element_by_class_name(customer_uan_name).send_keys(accountNo_1)
        #
        # if payload.state == 'Massachusetts':
        #     try:
        #         elem = driver.find_element_by_name(customer_customer_key_name).send_keys("test")
        #         driver.find_element_by_xpath(customer_servicereference_xpath).send_keys(int(servicereference))
        #         time.sleep(2)
        #     except:
        #         pass
        # if payload.type == 'Business':
        #     # Can you please tell me your average monthly usage in kWH
        #     try:
        #         elem = driver.find_element_by_xpath(costumer_AverageUsage_xpath)
        #         for option in elem.find_elements_by_tag_name(options_tag_name):
        #             if option.text == payload.monthly_usage:
        #                 option.click()
        #     except:
        #         pass
        # time.sleep(1)
        # try:
        #     Check_buttons = driver.find_elements_by_xpath(costumer_CheckButtons_xpath)
        #     for x in range(0, len(Check_buttons)):
        #         if Check_buttons[x].is_displayed():
        #             Check_buttons[x].click()
        # except:
        #     pass
        # # WebDriverWait(driver, 30).until(EC.text_to_be_present_in_element_value(By.XPATH, "//span[@class='account-uan-span']/following-sibling::div/span"), "Valid!")
        #
        # time.sleep(6)
        # try:
        #     elem = driver.find_element_by_id(continue_button_id).click()
        # except:
        #     pass
        # try:
        #     elem = driver.find_element_by_name(continue_button_id).click()
        # except:
        #     pass
        ## Billing Info        #################################################################################:
        # wait_billing_page(driver)
        # fill_billing_info_page(address_house_street_generated, city, payload, phone_area_code_generated,
        #                        phone_last_generated, phone_prefix_generated, generated_zipCode)
        #
        # ## Summary:
        #
        #
        # summary(driver)
    # except:
    #     promo_offer_portal_1 = "N/a"
    #     promo_offer_portal_2 = "N/a"
    #     no_offer_message = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[2]').text

    # ## Disclosure:
    # if payload.brand == Green_ME:
    #     declouser_GreenME(driver)
    # elif payload.brand == NRG_regression:
    #     declouser_NRG(driver)
    # else:
    #     declouser_EP(driver)
    #
    # ## Grab Conformation Code        #################################################################################:
    #
    # grab_code(accountNo_1, payload, promo_offer_portal_1, promo_offer_portal_2, no_offer_message )
    #
    # ## Submit        #################################################################################:
    # try:
    #     elem = driver.find_element_by_id(submit_enroll_id).click()
    # except:
    #     pass
    #
    # wait_finish_page(driver)
    # driver.find_element_by_id(start_new_call_id).click()


def fill_billing_info_page(address_house_street_generated, city, payload, phone_area_code_generated,
                           phone_last_generated, phone_prefix_generated, generated_zipCode):
    if payload.type == 'Business':
        try:
            driver.find_element_by_xpath(billing_businessName_radio_yes_xpath).click()
            driver.find_element_by_xpath(billing_businessName_xpath).send_keys(
                "Tester_busines_account")
        except:
            pass
    elem = driver.find_element_by_name(billing_address_name).send_keys(
        address_house_street_generated)
    elem = driver.find_element_by_name(billing_city_name).send_keys(city)
    elem = driver.find_element_by_class_name(billing_state_class_name)
    for option in elem.find_elements_by_tag_name(options_tag_name):
        if option.text == payload.state:
            option.click()
    elem = driver.find_element_by_name(billing_zip_name).send_keys(generated_zipCode)
    elem = driver.find_element_by_name(billing_phone_area_code_name).send_keys(
        phone_area_code_generated)
    elem = driver.find_element_by_name(billing_phone_prefix_area_name).send_keys(
        phone_prefix_generated)
    elem = driver.find_element_by_name(billing_phone_last_digits_name).send_keys(
        phone_last_generated)

    email_no_buttons = driver.find_elements_by_class_name(billing_phone_email_no_class_name)
    for x in range(0, len(email_no_buttons)):
        if email_no_buttons[x].is_displayed():
            email_no_buttons[x].click()

    email_no_buttons = driver.find_elements_by_class_name(billing_phone_email_no_no_class_name)
    for x in range(0, len(email_no_buttons)):
        if email_no_buttons[x].is_displayed():
            email_no_buttons[x].click()

    if payload.account_type_2 == "Electric" or payload.account_type_2 == "Gas":
        driver.find_element_by_class_name(SameAsFirst_button_name).click()

    elem = driver.find_element_by_id(continue_button_id).click()
    time.sleep(2)


def fill_offer_page(payload):
    if payload.brand == Green_ME:
        try:
            fill_greenME_offer(payload)
        except:
            pass
        try:
            driver.find_element_by_xpath(offer_greenME_first_search_xpath).send_keys(payload.categorie_1)
            driver.find_element_by_id(payload.categorie_1).click()
        except:
            pass
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

        if payload.account_type_2 == "Gas":
            driver.find_element_by_xpath(offer_second_).send_keys(payload.categorie_2)
            driver.find_element_by_id(payload.categorie_2).click()
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
    # if multichoise:
    if payload.account_type_2 == "Gas" or payload.account_type_2 == "Electric":

        if payload.brand == Energy_plus :
            # fill first offer
            try:
                elem = driver.find_element_by_xpath(offer_first_search_xpath)
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.categorie_1:
                        option.click()
                    # new
                    elif option.text == payload.categorie_2:
                        option.click()
                elem = driver.find_element_by_xpath(offer_first_partner_choise_xpath)
                for option in elem.find_elements_by_tag_name(options_tag_name):
                    if option.text == payload.partner_1:
                        option.click()
                        # new
                    elif option.text == payload.partner_2:
                        option.click()
                elem = driver.find_element_by_class_name(offer_compaign_class_name)
                for option in elem.find_elements_by_tag_name(options_tag_name):
                    if option.text == payload.campaign_1:
                        option.click()
                    if option.text == payload.campaign_2:
                        option.click()
                elem = driver.find_element_by_class_name(offer_promo_class_name)
                for option in elem.find_elements_by_tag_name(options_tag_name):
                    if option.text == payload.promo_1:
                        option.click()
                    elif option.text == payload.promo_2:
                        option.click()
            except:
                pass

            try:
                elem = driver.find_element_by_xpath(offer_second_category_search_xpath)
                for option in elem.find_elements_by_tag_name(options_tag_name):
                    if option.text == payload.categorie_2:
                        option.click()
                    # new
                    elif option.text == payload.categorie_1:
                        option.click()
                elem = driver.find_element_by_xpath(offer_second_partner_choise_xpath)
                for option in elem.find_elements_by_tag_name(options_tag_name):
                    if option.text == payload.partner_2:
                        option.click()
                        # new
                    elif option.text == payload.partner_1:
                        option.click()
                elem = driver.find_element_by_xpath(offer_compaign_second_xpath)
                for option in elem.find_elements_by_tag_name(options_tag_name):
                    if option.text == payload.campaign_2:
                        option.click()
                    if option.text == payload.campaign_1:
                        option.click()
                elem = driver.find_element_by_xpath(offer_promo_second_xpath)
                for option in elem.find_elements_by_tag_name(options_tag_name):
                    if option.text == payload.promo_2:
                        option.click()
                    elif option.text == payload.promo_1:
                        option.click()

            except:
                pass
        if payload.brand == Green_ME:
            driver.find_element_by_xpath(offer_greenME_second_search_xpath).send_keys(payload.categorie_2)
            driver.find_element_by_id(payload.categorie_2).click()
    if payload.brand == Cirro:
        try:
            driver.find_element_by_id(payload.categorie_1).click()
        except:
            driver.find_element_by_xpath(offer_search_xpath).send_keys(payload.categorie_1)
            driver.find_element_by_id(payload.categorie_1).click()

    else:
        try:
            elem = driver.find_element_by_xpath(offer_select_category_1_xpath)
            for option in elem.find_elements_by_tag_name(options_tag_name):
                if option.text == payload.categorie_1:
                    option.click()
                elem = driver.find_element_by_class_name(offer_partner_class_name)
            for option in elem.find_elements_by_tag_name(options_tag_name):
                if option.text == payload.partner_1:
                    option.click()
            elem = driver.find_element_by_class_name(offer_campaigns_class_name)
            for option in elem.find_elements_by_tag_name(options_tag_name):
                if option.text == payload.campaign_1:
                    option.click()
            elem = driver.find_element_by_class_name(offer_campaigns_promos_name)
            for option in elem.find_elements_by_tag_name(options_tag_name):
                if option.text == payload.promo_1:
                    option.click()
        except:
            pass
    # todo do we need sleep?
    time.sleep(2)
    # Green option
    if payload.brand == Energy_plus :
        if payload.account_type_1 == 'Electric' or payload.account_type_2 == 'Electric':
            if payload.green_opt == "yes":
                elem = driver.find_element_by_id(offer_green_opt_yes).click()
            elif payload.green_opt == "no":
                elem = driver.find_element_by_id(offer_green_opt_no).click()
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
        if payload.account_type_1.lower() == 'electric':
            try:
                elem = driver.find_element_by_class_name(
                    get_call_account_electric_class_name).click()
            except:
                pass
        if payload.account_type_1.lower() == 'gas':
            try:
                elem = driver.find_element_by_class_name(get_call_account_gas_class_name).click()
            except:
                pass
    except:
        pass
    # Who is the provider for your electric account?
    if payload.account_type_1.lower() == 'electric':
        elem = driver.find_element_by_name(get_started_EL_utility_1_class_name)
        for option in elem.find_elements_by_tag_name(options_tag_name):
            if option.text == payload.utility_1:
                option.click()
    if payload.account_type_1.lower() == 'gas':
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
        # if payload.type == 'Residential':
        elem = driver.find_element_by_class_name(get_started_resident_class_name).click()
        # elif payload.type == 'Business':
    #         elem = driver.find_element_by_class_name(get_started_business_class_name).click()
    except:
        pass

    ##2 accounts test:
    # if payload.account_type_2 == "Electric" or payload.account_type_2 == "Gas":
    #     elem = driver.find_element_by_id(get_started_add_second_account_id).click()
    #     time.sleep(1)
    #     # if payload.account_type_2 == "Gas":
    #     elem = driver.find_element_by_xpath(get_started_select_state_for_secondAC_xpath)  # second state
    #     for option in elem.find_elements_by_tag_name(options_tag_name):
    #         if option.text == payload.state:
    #             option.click()
    #     time.sleep(1)
    #     if payload.state == "Maryland":
    #         # Is Your Name on the Utility Bill?
    #         try:
    #             elem = driver.find_element_by_xpath(get_started_name_utility_yes_xpath_second_offer).click()
    #         except:
    #             pass
    #         try:
    #             if payload.account_type_2 == "Gas":
    #                 elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[7]/div[3]/div[2]/label/input').click()  # choose second_gas
    #             if payload.account_type_2 == 'Electric':
    #                 driver.find_element_by_xpath(
    #                     '/html/body/div[2]/div/div[1]/div[7]/div[3]/div[1]/label/input').click()
    #         except:
    #             pass
    #         # Who is the  provider for your gas account?
    #         elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[7]/div[4]/select')  # choose second utility
    #         for option in elem.find_elements_by_tag_name(options_tag_name):
    #             if option.text == payload.utility_2:
    #                 option.click()
    #
    #     if payload.state != "Maryland":
    #         try:
    #             if payload.account_type_2 == "Gas":
    #                 elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[7]/div[2]/div[2]/label/input').click()  # choose second_gas
    #             if payload.account_type_2 == 'Electric':
    #                 driver.find_element_by_xpath(
    #                     '/html/body/div[2]/div/div[1]/div[7]/div[2]/div[1]/label/input').click()
    #         except:
    #             pass
    #         elem = driver.find_element_by_xpath(get_started_second_provider_xpath)  # choose second utility
    #         for option in elem.find_elements_by_tag_name(options_tag_name):
    #             if option.text == payload.utility_2:
    #                 option.click()
    #
    #
    # if payload.type == "Residential":
    Residentials_buttons = driver.find_elements_by_class_name('account-type-residential')
    for x in range(0, len(Residentials_buttons)):
        if Residentials_buttons[x].is_displayed():
            Residentials_buttons[x].click()

    # if payload.type == "Business":
    #     Business_buttons = driver.find_elements_by_class_name('account-type-business')
    #     for x in range(0, len(Business_buttons)):
    #         if Business_buttons[x].is_displayed():
    #             Business_buttons[x].click()

    if payload.account_type_1.lower()== "gas" :
    # if payload.account_type_1 == "Gas" or payload.account_type_2 == "Gas":
    #     if payload.gas_option == 'Heating Only':
    #         heating_buttons = driver.find_elements_by_class_name(get_started_gas_HeatingOnly_class_name)
    #         for x in range(0, len(heating_buttons)):
    #             if heating_buttons[x].is_displayed():
    #                 heating_buttons[x].click()
        # if payload.gas_option == 'Cooking Only':
        #     cooking_buttons = driver.find_elements_by_class_name(get_started_gas_CookingOnly_class_name)
        #     for x in range(0, len(cooking_buttons)):
        #         if cooking_buttons[x].is_displayed():
        #             cooking_buttons[x].click()
        # if payload.gas_option == 'Both Heating & Cooking':
            both_buttons = driver.find_elements_by_class_name(get_started_gas_Both_class_name)
            for x in range(0, len(both_buttons)):
                if both_buttons[x].is_displayed():
                    both_buttons[x].click()

    #
    # Save and continue button
    elem = driver.find_element_by_id(get_started_save_and_con_but_id).click()


def fill_greenME_offer(payload):
    if payload.categorie_1 == 'Pollution Free Smart 6':
        driver.find_element_by_id(payload.categorie_1).click()
    if payload.categorie_1 == "Pollution Free Reliable Rate" and payload.utility_1 == "ComEd":
        driver.find_element_by_id(payload.categorie_1).click()
    if payload.categorie_1 == 'SolarSPARC 10%12':
        driver.find_element_by_xpath('//span[contains(text(), "SolarSPARC")]').click()
        driver.find_element_by_id(payload.categorie_1).click()
    if payload.categorie_1 == 'SolarSPARC 10% 12':
        driver.find_element_by_xpath('//span[contains(text(), "SolarSPARC")]').click()
        driver.find_element_by_id(payload.categorie_1).click()
    if payload.categorie_1 == 'Pollution Free Reliable Rate':
        driver.find_element_by_xpath('//span[contains(text(), "Pollution Free Reliable Rate")]').click()
        driver.find_element_by_id(payload.categorie_1).click()

    if payload.categorie_1 == 'Pollution Free Farm to Market Reliable Rate' or payload.categorie_1 == 'Pollution Free TimeWise 12':  # 'Pollution Free Reliable Rate' or 'Pollution Free TimeWise 12'
        if payload.categorie_1 == 'Pollution Free Farm to Market Reliable Rate':  # Pollution Free Farm to Market Reliable Rate
            try:
                driver.find_element_by_xpath(
                    '//span[contains(text(), "Pollution Free Farm to Market Reliable Rate")]').click()
                driver.find_element_by_id(payload.categorie_1).click()
            except:
                driver.find_element_by_xpath('//span[contains(text(), "Pollution Free Farm to Market")]').click()
                driver.find_element_by_id(payload.categorie_1).click()
        else:
            try:
                driver.find_element_by_id(payload.categorie_1).click()
            except:
                driver.find_element_by_xpath('//span[contains(text(), "Pollution Free Reliable Rate")]').click()
                driver.find_element_by_id(payload.categorie_1).click()

    if payload.categorie_1 == 'Pollution Free with Goal Zero 6' or payload.categorie_1 == 'Pollution Free with Goal Zero 24' \
            or payload.categorie_1 == 'Pollution Free with Goal Zero 12':
        driver.find_element_by_xpath('//span[contains(text(), "Goal Zero")]').click()
        driver.find_element_by_id(payload.categorie_1).click()

    else:
        pass
