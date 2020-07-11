import csv
from collections import namedtuple
from datetime import datetime

import pytest
import xlrd
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_BrandPage import BrandPage
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_accountNO_generator import account_generator_accountNo_1, account_generator_accountNo_2, servicereference_generator
from Inbound.States.Inbound_Enrollments_4brands_test.address_generator import generated_zipCode
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_generator_names_and_address import names_and_address_generator
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_generator_zip_city import generator_zip_city
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_loginPage import LoginPage
from Inbound.States.Inbound_Enrollments_4brands_test.InboundEnrollments_tests_Settings import URL, tester, chosen_driver, workbook_name, start_string, data_sheet_name, start_page
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_pages_methods import summary, wait_offer_page, \
    wait_get_started_page, wait_get_started_page_state_list, wait_costumer_info_page, wait_billing_page, \
    wait_grab_code_page, wait_finish_page, declouser_EP, declouser_GreenME, declouser_NRG
import Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags
import Inbound.States.Inbound_Enrollments_4brands_test.Inbound_pages_methods
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
def driver(request):
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

def grab_code( accountNo_1, payload):
    wait_grab_code_page(driver)
    elem = driver.find_element_by_id("confcode")
    confcode = elem.text
    # print(
    #     "Passed " + " " + payload.test_name + ", Conformation =  " + confcode + ' for ' + payload.state + ' - ' + payload.utility_1)
    city, generated_zipCode = generator_zip_city(payload)
    # zip = generated_zipCode
    f = open("./Inbound_Enrollments_tests_results.csv", 'a', newline='')
    now = datetime.now()
    time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
    csv_a = csv.writer(f)
    address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = names_and_address_generator()
    csv_a.writerow(["Passed", tester, time, payload.test_name, payload.brand, payload.account_type_1, payload.account_type_2, payload.first_name,
                    first_name_generated, last_name_generated, payload.state, city, payload.utility_1, payload.partner_1, payload.campaign_1, payload.categorie_1,
                    payload.promo_1, generated_zipCode,  str("'"+str(accountNo_1)), confcode])



@pytest.mark.parametrize("payload", tests_values, ids=[p.first_name for p in tests_values])
def test_state(driver, payload):
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
        account = str(payload.accountNo_1)
        zip = str(generated_zipCode)
        f = open("./results.txt", 'a')
        raise ae


def Inbound_start_test(test_setup, payload):
    accountNo_1 = account_generator_accountNo_1(payload)
    address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = names_and_address_generator()
    city, generated_zipCode = generator_zip_city(payload)
    random_zip =  generated_zipCode
    first_name_generated_ = first_name_generated
    last_name_generated_ = last_name_generated
    servicereference = servicereference_generator(payload)
    if payload.account_type_2 =='Gas' or payload.account_type_2 == 'Electric':
        accountNo_2 = account_generator_accountNo_2(payload)
    else:
        pass

    if  driver.current_url == start_page :
        pass
    else:
        driver.get(URL)
        login = LoginPage(driver)
        login.fill_login()
    ###         Login page        #################################################################################
    # login = LoginPage(driver)
    # login.fill_login()

    ###Brand page
    choose_brand = BrandPage(driver)
    if payload.brand == Energy_plus:
        choose_brand.click_EP_brand()
    elif payload.brand == 'NRG_regression':
        choose_brand.click_NRG_brand()
    elif payload.brand == 'GreenMT':
        choose_brand.click_GME_brand()
    elif payload.brand == 'Cirro':
        choose_brand.click_Cirro_brand()
    choose_brand.click_save_and_continue_button()

    ### Get Started page       #################################################################################:
    wait_get_started_page(driver)
    # May I please have your name?
    fill_get_started_page(first_name_generated_, last_name_generated_, payload)

    ###     Offer page           #################################################################################:

    wait_offer_page(driver)
    # time.sleep(2)
    time.sleep(1)

    fill_offer_page(payload)

## Customer Info page        #################################################################################::
    wait_costumer_info_page(driver)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_firs_name_name).send_keys(tester + "_" + first_name_generated_)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_last_name_name).send_keys(last_name_generated_)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_service_address_1_name).send_keys(address_house_street_generated)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_city_name).send_keys(city)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_zip_name).send_keys(random_zip)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_phone_area_code_name).send_keys(phone_area_code_generated)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_prefix_name).send_keys(phone_prefix_generated)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_last_digit_name).send_keys(phone_last_generated)

    try:
        if payload.brand ==Energy_plus:
#Todo - do we need double twice choose
            if payload.account_type_2 =="Gas":
                elem = driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_ElectricPodId_input_xpath).send_keys(accountNo_1)
                elem = driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_GasPodId_input_xpath).send_keys(str(payload.accountNo_gas_1))
                #Is your billing information the same as your service information for this account?
                elem = driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.SameAsFirst_button_name).click()
                elem = driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_billing_the_samecervice_address_xpath).click()
                elem = driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_CheckElectricPoDID_buttn_xpath).click()
                # elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/button").click()
                # driver.find_element_by_xpath('//button[contains(text(), "Check Electric PoD ID")]').click()
                # driver.find_element_by_xpath('//span[contains(text(), "New Jersey Natural Gas Account Number")]/parent::div/button').click()

            elif payload.account_type_2 == "Electric":

                time.sleep(1)
                elem = driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.SameAsFirst_button_name).click()

                try:
                    driver.find_element_by_xpath(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_PECOAccountNumber_input_xpath).send_keys(accountNo_1)
                # except:
                #     pass
                # try:
                    driver.find_element_by_xpath(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_PECOAccountNumber_button_xpath).click()
                except:
                    pass
                try:
                    driver.find_element_by_xpath(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_PPL_EU_AcNum_input_xpath).send_keys(int(payload.accountNo_el_2))
                # except:
                #     pass
                # try:
                    driver.find_element_by_xpath(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_PPL_EU_AcNum_checkButton_xpath).click()
                except:
                    pass

                elem = driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_UAN_class_name).send_keys(accountNo_1)
                elem = driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_check_account_number_namber_name).click()
                elem = driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_PPL_EU_AcNum_input_xpath).send_keys(
                    int(payload.accountNo_el_2))
                elem = driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_PPL_EU_AcNum_checkButton_xpath).click()

        elif payload.brand =='GreenMT':
            if payload.utility_1 == 'Met-Ed' or  payload.utility_1 =='PECO':
                elem = driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_UAN_class_name).send_keys(accountNo_1)
            elif payload.utility_1 == 'Philadelphia Gas Works':
                driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_ServicePointID_input_Xpath).send_keys(int(accountNo_1))
                driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_PGW_Account_input_xpath).send_keys(int(accountNo_1))
                driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_PGW_BillingAccount_input_xpath).send_keys(int(accountNo_1))



        if payload.account_type_2 =="Gas" or payload.account_type_2 =="Electric":
                try:
                    elem = driver.find_element_by_name(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_customer_key_name).send_keys(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_key_TEXT)
                    elem = driver.find_element_by_class_name(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_check_extra_number_class_name).click()
                    time.sleep(2)
                except:
                    pass

                elem = driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.SameAsFirst_button_name).click()
                driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_2nd_AcNo_inter_xpath).send_keys(accountNo_2)


        if payload.brand == 'NRG_regression':
            if payload.utility_1 == 'Philadelphia Gas Works':
                driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_ServicePointID_input_Xpath).send_keys(int(accountNo_1))
                driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_PGW_Account_input_xpath).send_keys(int(accountNo_1))
                driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_PGW_BillingAccount_NRG_input_xpath).send_keys(int(servicereference))


            if payload.account_type_2 == "Gas":
                elem=driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_UAN_class_name).send_keys(accountNo_1)
                # elem = driver.find_element_by_class_name(Inbound.States.tags.customer_check_account_number_namber_name).click()
                time.sleep(2)

                driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.SameAsFirst_button_name).click()
                driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_billing_the_samecervice_address_xpath).click()
                driver.find_element_by_xpath(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_AcNO_input_xpath).send_keys(int(payload.accountNo_gas_1))
                # driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/button").click()
            else:
                pass
        elem = driver.find_element_by_class_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_uan_name).send_keys(accountNo_1)


    except:
        elem = driver.find_element_by_class_name(
            Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_copy_to_billing_yes_name).click()
        elem = driver.find_element_by_class_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_uan_name).send_keys(accountNo_1)


    if  payload.state == 'Massachusetts':
        try:
            elem = driver.find_element_by_name(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_customer_key_name).send_keys("test")
            driver.find_element_by_xpath(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_servicereference_xpath).send_keys(int(servicereference))
            # elem = driver.find_element_by_class_name(Inbound.States.tags.customer_check_extra_number_class_name).click()

            time.sleep(2)
        except:
            pass
    if payload.type == 'Business':
        #Can you please tell me your average monthly usage in kWH
        try:
            elem = driver.find_element_by_xpath(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_AverageUsage_xpath)
            for option in elem.find_elements_by_tag_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                if option.text == payload.monthly_usage:
                    option.click()
        except:
            pass
    try:
        Check_buttons = driver.find_elements_by_xpath(
            Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_CheckButtons_xpath)
        for x in range(0, len(Check_buttons)):
            if Check_buttons[x].is_displayed():
                Check_buttons[x].click()
    except:
        pass

    # Todo - finish wait
    time.sleep(3)
    elem = driver.find_element_by_id(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.continue_button_id).click()

    ## Billing Info        #################################################################################:
    wait_billing_page(driver)
    fill_billing_info_page(address_house_street_generated, city, payload, phone_area_code_generated,
                           phone_last_generated, phone_prefix_generated, generated_zipCode)

    ## Summary:
    summary(driver)

    ## Disclosure:
    if payload.brand == 'GreenMT':
        declouser_GreenME(driver)
    elif payload.brand == 'NRG_regression':
        declouser_NRG(driver)
    else:
        declouser_EP(driver)

    ## Grab Conformation Code        #################################################################################:

    grab_code(accountNo_1, payload)

    ## Submit        #################################################################################:
    try:
        elem = driver.find_element_by_id(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.submit_enroll_id).click()
    except:
        pass

    wait_finish_page(driver)
    driver.find_element_by_id(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.start_new_call_id).click()


def fill_billing_info_page(address_house_street_generated, city, payload, phone_area_code_generated,
                           phone_last_generated, phone_prefix_generated, generated_zipCode):
    if payload.type == 'Business':
        try:
            driver.find_element_by_xpath(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_businessName_radio_yes_xpath).click()
            driver.find_element_by_xpath(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_businessName_xpath).send_keys(
                "Tester_busines_account")
        except:
            pass
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_address_name).send_keys(
        address_house_street_generated)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_city_name).send_keys(city)
    elem = driver.find_element_by_class_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_state_class_name)
    for option in elem.find_elements_by_tag_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
        if option.text == payload.state:
            option.click()
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_zip_name).send_keys(generated_zipCode)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_phone_area_code_name).send_keys(
        phone_area_code_generated)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_phone_prefix_area_name).send_keys(
        phone_prefix_generated)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_phone_last_digits_name).send_keys(
        phone_last_generated)
    # elem = driver.find_element_by_class_name(Inbound.States.tags.billing_phone_email_no_class_name).click()
    # elem = driver.find_element_by_class_name(Inbound.States.tags.billing_phone_email_no_no_class_name).click()

    email_no_buttons = driver.find_elements_by_class_name(
        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_phone_email_no_class_name)
    for x in range(0, len(email_no_buttons)):
        if email_no_buttons[x].is_displayed():
            email_no_buttons[x].click()

    email_no_buttons = driver.find_elements_by_class_name(
        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_phone_email_no_no_class_name)
    for x in range(0, len(email_no_buttons)):
        if email_no_buttons[x].is_displayed():
            email_no_buttons[x].click()

    # if payload.brand == Energy_plus and payload.account_type_2 == "Electric" or payload.account_type_2 == "Gas":
    if payload.account_type_2 == "Electric" or payload.account_type_2 == "Gas":
    #     driver.find_element_by_xpath(Inbound.States.tags.billing_phone_email_no_2ndAccount_class_xpath).click()  # no email
    #     driver.find_element_by_xpath(
    #         '/html/body/div[2]/div/div[1]/div[1]/div[2]/div[4]/div/div/div[1]/p[2]/input[2]').click()  # no email
    #     try:
            driver.find_element_by_class_name(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.SameAsFirst_button_name).click()
    #     except:
    #         pass
    # if payload.brand == 'GreenMT' and payload.account_type_2 == "Gas":
        # elem = driver.find_element_by_class_name("same-as-first").click()
        # elem = driver.find_element_by_class_name("same-emailchoice-as-first").click()
    elem = driver.find_element_by_id(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.continue_button_id).click()
    time.sleep(2)


def fill_offer_page(payload):

    if payload.brand == 'GreenMT':
        driver.find_element_by_xpath(offer_greenME_first_search_xpath).send_keys(payload.categorie_1)
        driver.find_element_by_id(payload.categorie_1).click()
    # if payload.brand == "GreenMT":
    #     # todo
    #     # try:
    #     #     from selenium.webdriver.support.wait import WebDriverWait
    #     #     WebDriverWait(driver, 1).until(expected_conditions.visibility_of_element_located(
    #     #             (By.XPATH, "//span[contains(text(),'1') and @class= 'badge default-gray ng-binding']")))
    #     # except:
    #     #     try:
    #     #         from selenium.webdriver.support.wait import WebDriverWait
    #     #         WebDriverWait(driver, 1).until(expected_conditions.visibility_of_element_located((By.ID, "category-*Pollution Free")))
    #     #     except:
    #     #         WebDriverWait(drive   r, 1).until(expected_conditions.visibility_of_element_located((By.ID, "category-Google Products")))
    #     wait_offer_page(driver)
    #
    #     try:
    #         driver.find_element_by_id(payload.categorie_1).click()
    #     except:
    #         pass
    #     try:
    #         fill_greenMT_offer(payload)
    #     except:
    #         pass
        # try:
        #     driver.find_element_by_xpath("//input[@class='col-md-2 form-control ng-pristine ng-valid']").send_keys(
        #         payload.categorie_1)
        #     driver.find_element_by_id(payload.categorie_1).click()
        # except:
        #     pass
    if payload.brand == 'NRG_regression':
        wait_offer_page(driver)
        #
        # try:
        #     from selenium.webdriver.support.wait import WebDriverWait
        #     WebDriverWait(driver, 1).until(
        #         expected_conditions.visibility_of_element_located(
        #             (By.XPATH, "//span[contains(text(),'1') and @class= 'badge default-gray ng-binding']")))
        # except:
        #     pass
        try:
            # fill_greenMT_offer(payload)
            driver.find_element_by_xpath(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_search_xpath).send_keys(payload.categorie_1)
            driver.find_element_by_id(payload.categorie_1).click()
        except:
            try:
                elem = driver.find_element_by_id(payload.categorie_1).click()
            except:
                pass

        if payload.account_type_2 == "Gas":
            # driver.find_element_by_xpath('//span[contains(text(),"1") and @class ="badge default-gray ng-binding"]').send_keys(payload.categorie_1)
            # time.sleep(1)
            # driver.find_element_by_id(payload.categorie_1).click()
            driver.find_element_by_xpath(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_second_).send_keys(payload.categorie_2)
            driver.find_element_by_id(payload.categorie_2).click()
    # Offer - PSE_Electric "Fixed" choise
    if payload.utility_type == 'Variable':
        try:
            Variable_buttons = driver.find_elements_by_xpath(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_Varriable_choise_xpath)
            for x in range(0, len(Variable_buttons)):
                if Variable_buttons[x].is_displayed():
                    Variable_buttons[x].click()
        except:
            pass
    elif payload.utility_type == 'Fixed':
        try:
            Fixed_buttons = driver.find_elements_by_xpath(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_Fixed_choise_xpath)
            for x in range(0, len(Fixed_buttons)):
                if Fixed_buttons[x].is_displayed():
                    Fixed_buttons[x].click()
        except:
            pass
    # if multichoise:
    # time.sleep(2)
    if payload.account_type_2 == "Gas" or payload.account_type_2 == "Electric":

        if payload.brand == Energy_plus:
            # IF Electric choise on the TOP:
            #fill first offer
            try:
                # elem = driver.find_element_by_xpath(Inbound.States.tags.offer_first_search_xpath).click()
                elem = driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_first_search_xpath)
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.categorie_1:
                        option.click()
                    # new
                    elif option.text == payload.categorie_2:
                        option.click()
                elem = driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_first_partner_choise_xpath)
                for option in elem.find_elements_by_tag_name(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                    if option.text == payload.partner_1:
                        option.click()
                        # new
                    elif option.text == payload.partner_2:
                        option.click()
                elem = driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_compaign_class_name)
                for option in elem.find_elements_by_tag_name(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                    if option.text == payload.campaign_1:
                        option.click()
                    if option.text == payload.campaign_2:
                        option.click()
                elem = driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_promo_class_name)
                for option in elem.find_elements_by_tag_name(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                    if option.text == payload.promo_1:
                        option.click()
                    elif option.text == payload.promo_2:
                        option.click()
            except:
                pass


            try:
                elem = driver.find_element_by_xpath(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_second_category_search_xpath)
                for option in elem.find_elements_by_tag_name(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                    if option.text == payload.categorie_2:
                        option.click()
                    # new
                    elif option.text == payload.categorie_1:
                        option.click()
                elem = driver.find_element_by_xpath(offer_second_partner_choise_xpath)
                for option in elem.find_elements_by_tag_name(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                    if option.text == payload.partner_2:
                        option.click()
                        # new
                    elif option.text == payload.partner_1:
                        option.click()
                elem = driver.find_element_by_xpath(offer_compaign_second_xpath)
                for option in elem.find_elements_by_tag_name(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                    if option.text == payload.campaign_2:
                        option.click()
                    if option.text == payload.campaign_1:
                        option.click()
                elem = driver.find_element_by_xpath(offer_promo_second_xpath)
                for option in elem.find_elements_by_tag_name(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                    if option.text == payload.promo_2:
                        option.click()
                    elif option.text == payload.promo_1:
                        option.click()

            except:
                pass
            # time.sleep(2)
            #
            # # IF GAS choise on the TOP:
            # # for gas choise
            # try:
            #     elem = driver.find_element_by_xpath(Inbound.States.tags.offer_first_search_xpath)
            #     for option in elem.find_elements_by_tag_name(options_tag_name):
            #         if option.text == payload.categorie_2:
            #             option.click()
            #     elem = driver.find_element_by_class_name(offer_first_partner_choise_xpath)
            #     for option in elem.find_elements_by_tag_name(options_tag_name):
            #         if option.text == payload.partner_2:
            #             option.click()
            #     driver.find_element_by_class_name(offer_compaign_class_name)
            #     for option in elem.find_elements_by_tag_name(options_tag_name):
            #         if option.text == payload.campaign_2:
            #             option.click()
            #         if option.text == payload.campaign_1:
            #             option.click()
            #     elem = driver.find_element_by_xpath(offer_promo_class_name)
            #     for option in elem.find_elements_by_tag_name(options_tag_name):
            #         if option.text == payload.promo_2:
            #             option.click()
            #         if option.text == payload.promo_1:
            #             option.click()
            #
            #     # for electric choise
            #     elem = driver.find_element_by_xpath(
            #         "//h4[@class='account-header']/span[contains(text(),'2')]/parent::h4/following-sibling::div[2]/div/p/select[@class='categories categories-dropdown form-control']")
            #     for option in elem.find_elements_by_tag_name('option'):
            #         if option.text == payload.categorie_1:
            #             option.click()
            #     elem = driver.find_element_by_xpath(
            #         "//h4[@class='account-header']/span[contains(text(),'2')]/parent::h4/following-sibling::div[2]/div/p[2]/select[@class='partners partners-dropdown form-control']")
            #     for option in elem.find_elements_by_tag_name('option'):
            #         if option.text == payload.partner_1:
            #             option.click()
            #     elem = driver.find_element_by_xpath(
            #         "//h4[@class='account-header']/span[contains(text(),'2')]/parent::h4/following-sibling::div[2]/div[2]/p/select[@class='campaigns campaigns-dropdown form-control']").click()
            #     elem = driver.find_element_by_xpath(
            #         "//h4[@class='account-header']/span[contains(text(),'2')]/parent::h4/following-sibling::div[2]/div[2]/p/select[@class='campaigns campaigns-dropdown form-control']")
            #     for option in elem.find_elements_by_tag_name('option'):
            #         if option.text == payload.campaign_2:
            #             option.click()
            #         if option.text == payload.campaign_1:
            #             option.click()
            #     elem = driver.find_element_by_xpath(
            #         "//h4[@class='account-header']/span[contains(text(),'2')]/parent::h4/following-sibling::div[2]/div[2]/p[2]/select[@class='promos promos-dropdown form-control']")
            #     for option in elem.find_elements_by_tag_name('option'):
            #         if option.text == payload.promo_1:
            #             option.click()
            #         if option.text == payload.promo_2:
            #             option.click()
            # except:
            #     pass
            #
            # try:
            #     elem = driver.find_element_by_xpath(
            #         "/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[1]/p[1]/select")
            #     # for El choise:
            #     for option in elem.find_elements_by_tag_name('option'):
            #         if option.text == ("Cash Back"):
            #             option.click()
            #     elem = driver.find_element_by_xpath(
            #         "/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[1]/p[2]/select")
            #     for option in elem.find_elements_by_tag_name('option'):
            #         if option.text == payload.partner_1:
            #             option.click()
            #     elem = driver.find_element_by_xpath(
            #         "/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[2]/p[1]/select")
            #     for option in elem.find_elements_by_tag_name('option'):
            #         if option.text == payload.campaign_1:
            #             option.click()
            #     elem = driver.find_element_by_xpath(
            #         "/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[2]/p[2]/select")
            #     for option in elem.find_elements_by_tag_name('option'):
            #         if option.text == payload.promo_1:
            #             option.click()
            # except:

                # try:
                #     driver.find_element_by_xpath(Inbound.States.tags.offer_fixed_button_xpath).click()
                # except
                #     pass

        if payload.brand == 'GreenMT':
            # driver.find_element_by_xpath(offer_greenMT_first_search_xpath).send_keys(payload.categorie_1)
            # driver.find_element_by_id(payload.categorie_1).click()
            driver.find_element_by_xpath(offer_greenME_second_search_xpath).send_keys(payload.categorie_2)
            driver.find_element_by_id(payload.categorie_2).click()

            # driver.find_element_by_xpath(offer_greenMT_first_search_xpath).send_keys(payload.categorie_1)
            # driver.find_element_by_xpath('//*[@id="Pollution Free Reliable Rate"]').click()
            # driver.find_element_by_xpath(
            #     '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[2]/div/div[4]/p[2]/span/input').send_keys(
            #     'Carbon Conscious plan')
            # driver.find_element_by_xpath('//*[@id="Carbon Conscious plan"]').click()
            # # time.sleep(3)3


    # elif payload.account_type_2 == "Electric":
    #     try:
    #         elem = driver.find_element_by_xpath(
    #             '/html/body/div[2]/div/div[1]/div[3]/div[1]/div/p/button[1]').click()  # fixed button
    #     except:
    #         pass
    #     try:
    #         elem = driver.find_element_by_xpath(
    #             '/html/body/div[2]/div/div[1]/div[3]/div[2]/div/p/button[1]').click()  # fixed button
    #     except:
    #         pass
    #
    #     elem = driver.find_element_by_xpath("//select[contains(@class, 'categories categories-dropdown form-control')]")
    #     for option in elem.find_elements_by_tag_name('option'):
    #         if option.text == ("Cash Back"):
    #             option.click()
    #
    #     elem = driver.find_element_by_class_name("partners")
    #     for option in elem.find_elements_by_tag_name('option'):
    #         if option.text == ("Brand Residential - PA - BRC"):
    #             option.click()
    #     elem = driver.find_element_by_class_name("campaigns")
    #     for option in elem.find_elements_by_tag_name('option'):
    #         if option.text == ("6742 - Fixed Downsell"):
    #             option.click()
    #     elem = driver.find_element_by_class_name("promos")
    #     for option in elem.find_elements_by_tag_name('option'):
    #         if option.text == ("015 - Residential (3%/$25)"):
    #             option.click()
    #     time.sleep(2)
    #
    #     # Offer: 2nd Electric account
    #
    #     elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/p[1]/select")
    #     for option in elem.find_elements_by_tag_name('option'):
    #         if option.text == ("Cash Back"):
    #             option.click()
    #     elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/p[2]/select")
    #     for option in elem.find_elements_by_tag_name('option'):
    #         if option.text == ("Brand Residential - PA - BRC"):
    #             option.click()
    #     elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/p[1]/select")
    #     for option in elem.find_elements_by_tag_name('option'):
    #         if option.text == ("6742 - Fixed Downsell"):
    #             option.click()
    #     elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/p[2]/select")
    #     for option in elem.find_elements_by_tag_name('option'):
    #         if option.text == ("015 - Residential (3%/$25)"):
    #             option.click()
    #     elem = driver.find_element_by_id("green_option_no").click()
    #     time.sleep(2)

    if payload.brand == "Cirro":
        try:
            driver.find_element_by_id(payload.categorie_1).click()
        except:
            driver.find_element_by_xpath(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_search_xpath).send_keys(payload.categorie_1)
            driver.find_element_by_id(payload.categorie_1).click()

    else:
        try:
            elem = driver.find_element_by_xpath(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_select_category_1_xpath)
            for option in elem.find_elements_by_tag_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                if option.text == payload.categorie_1:
                    option.click()
                elem = driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_partner_class_name)
            for option in elem.find_elements_by_tag_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                if option.text == payload.partner_1:
                    option.click()
            elem = driver.find_element_by_class_name(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_campaigns_class_name)
            for option in elem.find_elements_by_tag_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                if option.text == payload.campaign_1:
                    option.click()
            elem = driver.find_element_by_class_name(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_campaigns_promos_name)
            for option in elem.find_elements_by_tag_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                if option.text == payload.promo_1:
                    option.click()
        except:
            pass
    # todo do we need sleep?
    time.sleep(2)
    # Green option
    if payload.brand == Energy_plus:
        if payload.account_type_1 == 'Electric' or payload.account_type_2 == 'Electric':
            if payload.green_opt == "yes":
                elem = driver.find_element_by_id(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_green_opt_yes).click()
            elif payload.green_opt == "no":
                elem = driver.find_element_by_id(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_green_opt_no).click()
    try:
        Check_buttons = driver.find_elements_by_xpath(
            Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.costumer_CheckButtons_xpath)
        for x in range(0, len(Check_buttons)):
            if Check_buttons[x].is_displayed():
                Check_buttons[x].click()
    except:
        pass
    # Todo - finish wait
    time.sleep(1)
    try:
        elem = driver.find_element_by_id(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.continue_button_id).click()
    except:
        pass
    if payload.brand == 'GreenMT' or payload.brand == 'NRG_regression' or payload.brand == "Cirro":
        try:
            driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.continue_button_name).click()
        except:
            pass


def fill_get_started_page(first_name_generated_, last_name_generated_, payload):
    driver.find_element_by_id(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_First_name_id).send_keys(tester + "_" + first_name_generated_)
    driver.find_element_by_id(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_last_name_id).send_keys(last_name_generated_)
    wait_get_started_page_state_list(driver)
    # What state are you are calling from?
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_state_list_id)
    for option in elem.find_elements_by_tag_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
        if option.text == payload.state:
            option.click()
    # Is Your Name on the Utility Bill?
    if payload.state == "Maryland":
        # Is Your Name on the Utility Bill?
        try:
            elem = driver.find_element_by_xpath(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_name_utility_yes_xpath).click()
        except:
            pass
    # What account are you calling about today? - gas or electric
    try:
        if payload.account_type_1 == 'Electric':
            try:
                elem = driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_call_account_electric_class_name).click()
            except:
                pass
        if payload.account_type_1 == 'Gas':
            try:
                elem = driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_call_account_gas_class_name).click()
            except:
                pass
    except:
        pass
    # Who is the provider for your electric account?
    if payload.account_type_1 == 'Electric':
        elem = driver.find_element_by_name(
            Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_EL_utility_1_class_name)
        for option in elem.find_elements_by_tag_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
            if option.text == payload.utility_1:
                option.click()
    if payload.account_type_1 == 'Gas':
        try:
            elem = driver.find_element_by_xpath(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_Gas_utility_1_xpath)
            for option in elem.find_elements_by_tag_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                if option.text == payload.utility_1:
                    option.click()
        except:
            elem = driver.find_element_by_xpath(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_Gas_utility_NJ_xpath)
            for option in elem.find_elements_by_tag_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                if option.text == payload.utility_1:
                    option.click()
    # Is this electric account a residential or business address?try:
    try:
        if payload.type == 'Residential':
            elem = driver.find_element_by_class_name(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_resident_class_name).click()
        elif payload.type == 'Business':
            elem = driver.find_element_by_class_name(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_business_class_name).click()
    except:
        pass
    # if payload.account_type_1 == "Gas" or payload.account_type_2 == "Gas":
    #     try:  # - not necessery for Massachusetts
    #         if payload.account_type_1 == 'Gas':
    #             if payload.gas_option == 'Heating Only':
    #                 driver.find_element_by_class_name(
    #                     Inbound.States.tags.get_started_gas_HeatingOnly_class_name).click()
    #             if payload.gas_option == 'Cooking Only':
    #                 driver.find_element_by_class_name(
    #                     Inbound.States.tags.get_started_gas_CookingOnly_class_name).click()
    #             if payload.gas_option == 'Both Heating & Cooking':
    #                 driver.find_element_by_class_name(Inbound.States.tags.get_started_gas_Both_class_name).click()
    #     except:
    #         pass
    ##2 accounts test:
    if payload.account_type_2 == "Electric" or payload.account_type_2 == "Gas":
        elem = driver.find_element_by_id(
            Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_add_second_account_id).click()
        time.sleep(1)
        # if payload.account_type_2 == "Gas":
        elem = driver.find_element_by_xpath(get_started_select_state_for_secondAC_xpath)  # second state
        for option in elem.find_elements_by_tag_name(options_tag_name):
            if option.text == payload.state:
                option.click()
        time.sleep(1)
        if payload.account_type_2 == "Gas":
            elem = driver.find_element_by_xpath(get_started_second_account_is_gas_xpath).click()  # choose second_gas
            # elem = driver.find_element_by_xpath(get_started_secon_provider_xpath).click()
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
            both_buttons = driver.find_elements_by_class_name(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_gas_Both_class_name)
            for x in range(0, len(both_buttons)):
                if both_buttons[x].is_displayed():
                    both_buttons[x].click()

        # if payload.account_type_2 == "Electric":
        #
        #     time.sleep(1)
        #     elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[1]/select")
        #     for option in elem.find_elements_by_tag_name('option'):
        #         if option.text == payload.state:
        #             option.click()
        #     time.sleep(1)
        #
        #     # What account are you calling about today? 2nd electric account
        #     elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[3]/select")
        #     for option in elem.find_elements_by_tag_name('option'):
        #         if option.text == payload.utility_2:
        #             option.click()
        #
        #     # Is this electric account a residential or business address?
        #     elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[4]/label[1]/input").click()
    if payload.brand == 'GreenMT' and payload.state == 'New York':
        try:
            elem = driver.find_element_by_name("zone")
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == ("Westchester"):
                    option.click()
        except:
            pass
    # Save and continue button
    elem = driver.find_element_by_id(
        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_save_and_con_but_id).click()


def fill_greenMT_offer(payload):
    # if payload.categorie_1 == 'Carbon Conscious plan':
    #     driver.find_element_by_xpath('//span[contains(text(), "Carbon Conscious plan")]').click()
    #     driver.find_element_by_id(payload.categorie_1).click()
    # if payload.categorie_1 == 'SolarSPARC 10%12':
    #     driver.find_element_by_xpath('//span[contains(text(), "SolarSPARC")]').click()
    #     driver.find_element_by_id(payload.categorie_1).click()
    # if payload.categorie_1 == 'SolarSPARC 10% 12':
    #     driver.find_element_by_xpath('//span[contains(text(), "SolarSPARC")]').click()
    #     driver.find_element_by_id(payload.categorie_1).click()
    # if payload.categorie_1 == 'Pollution Free Farm to Market Reliable Rate' or 'Pollution Free TimeWise 12': #'Pollution Free Reliable Rate' or 'Pollution Free TimeWise 12'
    #     if payload.categorie_1 == 'Pollution Free Farm to Market Reliable Rate':  # Pollution Free Farm to Market Reliable Rate
    #         try:
    #             driver.find_element_by_xpath('//span[contains(text(), "Pollution Free Farm to Market Reliable Rate")]').click()
    #             driver.find_element_by_id(payload.categorie_1).click()
    #         except:
    #             driver.find_element_by_xpath('//span[contains(text(), "Pollution Free Farm to Market")]').click()
    #             driver.find_element_by_id(payload.categorie_1).click()
    #     else:
    #         try:
    #             driver.find_element_by_id(payload.categorie_1).click()
    #         except:
    #             driver.find_element_by_xpath('//span[contains(text(), "Pollution Free Reliable Rate")]').click()
    #             driver.find_element_by_id(payload.categorie_1).click()
    #
    # if payload.categorie_1 == 'Pollution Free with Goal Zero 6' or 'Pollution Free with Goal Zero 24' or 'Pollution Free with Goal Zero 12':
    #     driver.find_element_by_xpath('//span[contains(text(), "Goal Zero")]').click()
    #     driver.find_element_by_id(payload.categorie_1).click()
    #
    # else:
        pass


