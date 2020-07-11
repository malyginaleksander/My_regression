import csv
from collections import namedtuple
from datetime import datetime
from random import randint

import pytest
import xlrd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from webdriver_manager.chrome import ChromeDriverManager

from Inbound.States.Inbound_Enrollments_4brands_test.address_and_name_generator import random_zip, random_City_in_the_state
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_BrandPage import BrandPage
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_accountNO_generator import account_generator_accountNo_1, account_generator_accountNo_2, servicereference_generator
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_loginPage import LoginPage
from Inbound.States.Inbound_Enrollments_4brands_test.InboundEnrollments_tests_Settings import URL, tester, chosen_driver, workbook_name, start_string, data_sheet_name
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_pages_methods import summary, wait_offer_page, \
    wait_get_started_page, wait_get_started_page_state_list, wait_costumer_info_page, wait_billing_page, \
    wait_grab_code_page, wait_finish_page, declouser_EP, declouser_GreenME, declouser_NRG
import Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags
import Inbound.States.Inbound_Enrollments_4brands_test.Inbound_pages_methods


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
def test_setup():
    global driver

    if chosen_driver == "firefox":
        driver = webdriver.Firefox()
    elif chosen_driver == "chrome":
        driver = webdriver.Chrome(ChromeDriverManager("2.36").install())
    else:
        driver = webdriver.Chrome(ChromeDriverManager("2.36").install())
    yield
    driver.close()
    driver.quit()

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
        account = str(payload.accountNo_1)
        zip = str(payload.zip)
        f = open("./results.txt", 'a')
        raise ae


def Inbound_start_test(test_setup, payload):

    accountNo_1 = account_generator_accountNo_1(payload)
    if payload.account_type_2 =='Gas' or payload.account_type_2 == 'Electric':
        accountNo_2 = account_generator_accountNo_2(payload)
    else:
        pass
    zip_code = str(random_zip)
    city = random_City_in_the_state


    driver.get(URL)
    ###Login page
    login = LoginPage(driver)
    login.fill_login()

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


    ### Get Started page:
    wait_get_started_page(driver)
    # May I please have your name?
    driver.find_element_by_id(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_First_name_id).send_keys(tester + "_" + payload.first_name)
    driver.find_element_by_id(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_last_name_id).send_keys(payload.last_name)

    wait_get_started_page_state_list(driver)

    #What state are you are calling from?
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_state_list__id)
    for option in elem.find_elements_by_tag_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
        if option.text == payload.state:
            option.click()


    # Is Your Name on the Utility Bill?
    if payload.state =="Maryland":
        try:
            elem = driver.find_element_by_xpath(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_name_utility_yes_xpath).click()
        except:
            pass
    # What account are you calling about today? - gas or electric
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


    # # What account are you calling about today? - gas or electric
    # if payload.account_type_1 == 'Electric':
    #     try:
    #         elem = driver.find_element_by_xpath(Inbound.States.tags.get_started_provider_xpath).click()
    #     except:
    #         pass
    # if payload.account_type_1 == 'Gas':
    #     try:
    #         elem = driver.find_element_by_xpath("//input[@*='Gas']").click()
    #     except:
    #         pass

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

    # Is this electric account a residential or business address?
    if payload.type == 'Residential':
        elem = driver.find_element_by_class_name(
            Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_resident_class_name).click()
    elif payload.type == 'Business':
        elem = driver.find_element_by_class_name(
            Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_business_class_name).click()

    try: # - not necessery for Massachusetts
        if payload.account_type_1 == 'Gas':
            if payload.gas_option == 'Heating Only':
                driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_gas_HeatingOnly_class_name).click()
            if payload.gas_option == 'Cooking Only':
                driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_gas_CookingOnly_class_name).click()
            if payload.gas_option == 'Both Heating & Cooking':
                driver.find_element_by_class_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_gas_Both_class_name).click()
    except:
        pass

    ##2 accounts test:
    if payload.account_type_2 == "Electric" or payload.account_type_2 == "Gas":
        elem = driver.find_element_by_id(
            Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_add_second_account_id).click()
        time.sleep(1)
        if  payload.account_type_2 =="Gas":
            elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[1]/select") #second state
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == payload.state:
                    option.click()
            time.sleep(1)
            #second utility

            elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[2]/div[2]/label/input").click()  #choose second_gas
            elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[3]/select").click()
            elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[3]/select") #choose second utility
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == payload.utility_2:
                    option.click()
            elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[4]/label[1]/input").click() #choose residential
            # How do you use your natural gas?
            elem = driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[1]/div[7]/div[5]/div[3]/label/input").click()


        if  payload.account_type_2 =="Electric":

            # elem = driver.find_element_by_id("add-account-button").click()
            time.sleep(1)
            elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[1]/select")
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == payload.state:
                    option.click()
            time.sleep(1)
            # What account are you calling about today? 2nd electric account

            elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[3]/select")
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == payload.utility_2:
                    option.click()

            # Is this electric account a residential or business address?
            elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[4]/label[1]/input").click()



            # time.sleep(1)
            # elem = driver.find_element_by_id("save-and-continue").click()
            # time.sleep(3)
    if payload.brand == 'GreenMT' and payload.state == 'New York':
        try:
            elem = driver.find_element_by_name("zone")
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == ("Westchester"):
                    option.click()
        except:
            pass


    #Save and continue button
    elem = driver.find_element_by_id(
        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.get_started_save_and_con_but_id).click()

    ### Offer page:
    wait_offer_page(driver)
    time.sleep(2)
    # try:
    #     driver.find_element_by_xpath("//input[@class='col-md-2 form-control ng-pristine ng-valid']").send_keys(payload.categorie_1)
    # except:
    #     # driver.find_element_by_xpath("//div[@class='offer-products']/child::p[2]/span/input").send_keys(payload.categorie_1)
    #     pass
    # driver.find_element_by_id(payload.categorie_1).click()



    if payload.brand == "GreenMT":
           #todo
            try:
               from selenium.webdriver.support.wait import WebDriverWait
               WebDriverWait(driver, 1).until(
                   expected_conditions.visibility_of_element_located((By.XPATH, "//span[contains(text(),'1') and @class= 'badge default-gray ng-binding']")))
            except:
                try:
                    from selenium.webdriver.support.wait import WebDriverWait
                    WebDriverWait(driver, 1).until(
                        expected_conditions.visibility_of_element_located((By.ID, "category-*Pollution Free")))
                except:
                    WebDriverWait(driver, 1).until(expected_conditions.visibility_of_element_located((By.ID, "category-Google Products")))
            try:
                driver.find_element_by_id(payload.categorie_1).click()
            except:
                pass
            try:
                fill_greenMT_offer(payload)
            except:
                pass
            try:
                driver.find_element_by_xpath("//input[@class='col-md-2 form-control ng-pristine ng-valid']").send_keys(
                    payload.categorie_1)
                driver.find_element_by_id(payload.categorie_1).click()
            except:
                pass
    if payload.brand == 'NRG_regression':
        # time.sleep(2)
        # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "offer-category-name")))
        # driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/p[2]/span/input').send_keys(payload.categorie_1)
        try:
            from selenium.webdriver.support.wait import WebDriverWait
            WebDriverWait(driver, 1).until(
                expected_conditions.visibility_of_element_located(
                    (By.XPATH, "//span[contains(text(),'1') and @class= 'badge default-gray ng-binding']")))
        except:
            pass
        try:
            # fill_greenMT_offer(payload)
            driver.find_element_by_xpath("//input[@class='col-md-2 form-control ng-pristine ng-valid']").send_keys(
                payload.categorie_1)
            driver.find_element_by_id(payload.categorie_1).click()
        except:
            try:
                elem = driver.find_element_by_id(payload.categorie_1).click()
            except:
                pass
                # driver.find_elements_by_id('category-*Primary Plans').click()
                # driver.find_elements_by_xpath('//div[contains(@class,"offer-products")]//p[2]/span/input').click()
                # driver.find_elements_by_xpath(
                #     '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/p[2]/span/input').send_keys(
                #     payload.categorie_1)
                # driver.find_elements_by_link_text(payload.categorie_1).click()
                #
                #

            # pass

        if payload.account_type_2 == "Gas":
            driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/p[2]/span/input').send_keys(payload.categorie_1)
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="The Cash Back Plan"]').click()
            driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[2]/div/div[4]/p[2]/span/input').send_keys(payload.categorie_2)
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="Essentials Natural Gas Plan"]').click()

    # Offer - PSE_Electric "Fixed" choise


    # try:
    #     elem = driver.find_element_by_xpath(('//button[contains(text(), "Fixed")]')).click()
    # except:
    #     pass
    try:
        Fixed_buttons = driver.find_elements_by_xpath('//button[contains(text(), "Fixed")]')
        for x in range(0, len(Fixed_buttons)):
            if Fixed_buttons[x].is_displayed():
                Fixed_buttons[x].click()
    except:
        pass


    #if multichoise:
    if payload.account_type_2 == "Gas":
        # try:
        #     elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div[2]/div/p/button[1]').click()
        # except:
        #     elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div[1]/div/p/button[1]').click()

        if payload.brand == Energy_plus:
        # IF Electric choise on the TOP:
            try:
                elem = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[1]/p[1]/select")
                for option in elem.find_element_by_tag_name('option'):
                    if option.text == payload.categorie_1:
                        option.click()
                elem = driver.find_element_by_class_name("partners")
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.categorie_1:
                        option.click()
                elem = driver.find_element_by_class_name("campaigns")
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.campaign_1:
                        option.click()
                    if option.text == payload.campaign_2:
                        option.click()
                elem = driver.find_element_by_class_name("promos")
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.promo_2:
                        option.click()
                    if option.text == payload.promo_1:
                        option.click()
                time.sleep(2)
            except:
                pass

        # IF GAS choise on the TOP:
        # for gas choise
            try:
                elem = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[1]/p[1]/select")
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.categorie_2:
                        option.click()
                elem = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[1]/p[2]/select")
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.partner_2:
                        option.click()
                driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[2]/p[1]/select').click()
                elem = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[2]/p[1]/select")
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == '0000 - Unknown':
                        option.click()
                    if option.text == payload.campaign_1:
                        option.click()
                elem = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[2]/p[2]/select")
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.promo_2:
                        option.click()
                    if option.text == payload.promo_1:
                        option.click()

                # for electric choise
                elem = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/p[1]/select")
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.categorie_1:
                        option.click()
                elem = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/p[2]/select")
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.partner_1:
                        option.click()
                elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/p[1]/select")
                for option in elem.find_elements_by_tag_name('option'):
                        if option.text == '0000 - Unknown':
                            option.click()
                        else:
                            if option.text == payload.campaign_1:
                                option.click()
                elem = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/p[2]/select")
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.promo_2:
                        option.click()
                    if option.text == payload.promo_1:
                        option.click()
            except:
                pass

            try:
                elem = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[1]/p[1]/select")
                # for El choise:
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == ("Cash Back"):
                        option.click()
                elem = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[1]/p[2]/select")
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.partner_1:
                        option.click()
                elem = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[2]/p[1]/select")
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.campaign_1:
                        option.click()
                elem = driver.find_element_by_xpath(
                    "/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[2]/p[2]/select")
                for option in elem.find_elements_by_tag_name('option'):
                    if option.text == payload.promo_1:
                        option.click()
            except:

                try:
                    driver.find_element_by_xpath(
                        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_fixed_button_xpath).click()
                except:
                    pass

        if  payload.brand == 'GreenMT':
            # WebDriverWait(driver, 20).until(
            #     EC.visibility_of_element_located((By.XPATH, ('//span[contains(text(), "1")]'))))
            # time.sleep(2)
            driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/p[2]/span/input').send_keys(
                'Pollution Free Reliable Rate')
            driver.find_element_by_xpath('//*[@id="Pollution Free Reliable Rate"]').click()
            driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[2]/div/div[4]/p[2]/span/input').send_keys(
                'Carbon Conscious plan')
            driver.find_element_by_xpath('//*[@id="Carbon Conscious plan"]').click()
            # time.sleep(3)


    elif  payload.account_type_2 == "Electric":
        try:
            elem = driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[1]/div[3]/div[1]/div/p/button[1]').click()  # fixed button
        except:
            pass
        try:
            elem = driver.find_element_by_xpath(
                '/html/body/div[2]/div/div[1]/div[3]/div[2]/div/p/button[1]').click()  # fixed button
        except:
            pass


        elem = driver.find_element_by_xpath("//select[contains(@class, 'categories categories-dropdown form-control')]")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("Cash Back"):
                option.click()

        elem = driver.find_element_by_class_name("partners")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("Brand Residential - PA - BRC"):
                option.click()
        elem = driver.find_element_by_class_name("campaigns")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("6742 - Fixed Downsell"):
                option.click()
        elem = driver.find_element_by_class_name("promos")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("015 - Residential (3%/$25)"):
                option.click()
        time.sleep(2)

        # Offer: 2nd Electric account

        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/p[1]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("Cash Back"):
                option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/p[2]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("Brand Residential - PA - BRC"):
                option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/p[1]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("6742 - Fixed Downsell"):
                option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/p[2]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("015 - Residential (3%/$25)"):
                option.click()
        elem = driver.find_element_by_id("green_option_no").click()
        time.sleep(2)

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

    time.sleep(2)
    #Green option
    if payload.brand == Energy_plus:
        if payload.account_type_1 == 'Electric' or  payload.account_type_2 == 'Electric':
            if  payload.green_opt == "yes":
                elem = driver.find_element_by_id(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_green_opt_yes).click()
            elif payload.green_opt == "no":
                elem = driver.find_element_by_id(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.offer_green_opt_no).click()


            # current_state = str(payload.state)
            # if current_state == 'Maryland' or 'Massachusetts' or 'New Jersey' or 'Ohio':
            #     try:
            #         driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/p/button[1]').click()
            #     except:
            #         pass
            #     elem = driver.find_element_by_xpath(
            #         '/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/p[1]/select').click()
            #     elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/p[1]/select')
            #     time.sleep(1)
            #     for option in elem.find_elements_by_tag_name('option'):
            #         if option.text == payload.categorie:
            #             option.click()
            #     driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/p[2]/select').click()
            #     elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/p[2]/select')
            #     driver.find_element_by_xpath('//option[contains(text(), "Brand Residential")]').click()
            #
            #     driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[2]/p[1]/select').click()
            #     elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[2]/p[1]/select')
            #     driver.find_element_by_xpath('//option[contains(text(), "Fixed")]').click()
            #     driver.find_element_by_xpath('//option[contains(@class,"promo")]').click()
            #     driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[2]/p[2]/select').click()
            #     elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[2]/p[2]/select')
            #     for option in elem.find_elements_by_tag_name('option'):
            #         if option.text == "015 - Residential (3%/$25)":
            #             option.click()

    try:
        Fixed_buttons = driver.find_elements_by_name('btn_continue')
        for x in range(0, len(Fixed_buttons)):
            if Fixed_buttons[x].is_displayed():
                Fixed_buttons[x].click()
    except:
        pass

    try:
        time.sleep(2)
        elem = driver.find_element_by_xpath("//input[@type='button' and @value='Save and Continue']").click()
    except:
        pass
    ## Customer Info:
    wait_costumer_info_page(driver)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_firs_name_name).send_keys(payload.first_name)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_last_name_name).send_keys(payload.last_name)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_service_address_1_name).send_keys(payload.address)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_city_name).send_keys(city)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_zip_name).send_keys(zip_code)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_phone_area_code_name).send_keys(
        int(payload.area_code))
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_prefix_name).send_keys(int(payload.prefix))
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_last_digit_name).clear()
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_last_digit_name).send_keys(int(payload.last))

    try:
        if payload.brand ==Energy_plus:

            if payload.account_type_2 =="Gas":
                elem = driver.find_element_by_xpath('//button[contains(text(), "Check Electric PoD ID")]/preceding-sibling::input').send_keys(accountNo_1)
                elem = driver.find_element_by_xpath('//button[contains(text(), "Check Gas PoD ID")]/preceding-sibling::input').send_keys(str(payload.accountNo_gas_1))
                # elem = driver.find_element_by_xpath('//span[contains(text(), "New Jersey Natural Gas Account Number")]/parent::div/input').send_keys(str(payload.accountNo_gas_1))

                elem = driver.find_element_by_class_name("same-as-first").click()
                elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[4]/input[1]").click()
                elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/button").click()
                driver.find_element_by_xpath('//button[contains(text(), "Check Electric PoD ID")]').click()
                # driver.find_element_by_xpath('//span[contains(text(), "New Jersey Natural Gas Account Number")]/parent::div/button').click()

            elif payload.account_type_2 == "Electric":

                # elem = driver.find_element_by_class_name("uan").send_keys(int(payload.accountNo_1))
                # elem = driver.find_element_by_class_name("check-account-number").click()
                # elem = driver.find_element_by_xpath(
                #     '//span[contains(text(), "Is your billing information the same as your service information for this account? ")]/parent::div/input').click()
                # elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/div[3]/input[1]').click()
                # elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div[1]/div[3]/input[1]').click() #  biiling the same-as-first address
                time.sleep(1)
                # elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/input[1]").click()
                # elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/input").send_keys(
                #     int(payload.accountNo_el_2))
                # elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/button").click()
                #
                elem = driver.find_element_by_class_name("same-as-first").click()
                # elem = driver.find_element_by_class_name("uan").send_keys(int(accountNo))
                # elem = driver.find_element_by_class_name("check-account-number").click()
                #
                # driver.find_element_by_xpath('//span[contains(text(), "PPL Electric Utilities Account Number")]following-sibling::button').click()
                try:
                    driver.find_element_by_xpath(
                        '//span[contains(text(), "PECO Account Number")]/parent::div/input').send_keys(accountNo_1)
                except:
                    pass
                try:
                    driver.find_element_by_xpath(
                        '//span[contains(text(), "PECO Account Number")]/following-sibling::button').click()
                except:
                    pass
                try:
                    driver.find_element_by_xpath(
                        '//span[contains(text(), "PPL Electric Utilities Account Number")]/parent::div/input').send_keys(
                        int(payload.accountNo_el_2))
                except:
                    pass
                try:
                    driver.find_element_by_xpath(
                        '//span[contains(text(), "PPL Electric Utilities Account Number")]/following-sibling::button').click()
                except:
                    pass

                elem = driver.find_element_by_class_name("uan").send_keys(accountNo_1)
                elem = driver.find_element_by_class_name("check-account-number").click()
                elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/input").send_keys(
                    int(payload.accountNo_el_2))
                elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/button").click()

        elif payload.brand =='GreenMT':
            if payload.utility_1 == 'Met-Ed' or  payload.utility_1 =='PECO':
                elem = driver.find_element_by_class_name("uan").send_keys(accountNo_1)
            elif payload.utility_1 == 'Philadelphia Gas Works':
                driver.find_element_by_xpath("//span[contains(text(),'Service Point ID')]/following-sibling::input").send_keys(int(accountNo_1))
                driver.find_element_by_xpath("//span[contains(text(),'PGW Account Number')]/following-sibling::input[1]").send_keys(int(accountNo_1))
                driver.find_element_by_xpath("//span[contains(text(),'PGW  Billing Account Number')]/following-sibling::input").send_keys(int(accountNo_1))
                # driver.find_element_by_xpath("//button[text()= 'Check Account Number']").click()
                # driver.find_element_by_xpath("//button[text()= 'Check  Billing Account Number']").click()
                # driver.find_element_by_xpath("//button[text()= 'Check  Billing Account Number']").click()


        if payload.account_type_2 =="Gas" or payload.account_type_2 =="Electric":
                # elem = driver.find_element_by_class_name("uan").send_keys(int(accountNo_1))
                # elem = driver.find_element_by_class_name("check-account-number").click()
                # time.sleep(2)

                try:
                    elem = driver.find_element_by_name("Customer Key").send_keys("test")
                    elem = driver.find_element_by_class_name("check-extra-account-number").click()
                    time.sleep(2)
                except:
                    pass
                # time.sleep(2)

                elem = driver.find_element_by_class_name("same-as-first").click()
                # elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/input").click()
                # elem = driver.find_element_by_xpath(
                #     "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/input").send_keys(int(accountNo_1))
                # elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/button").click()
                # time.sleep(2)
                driver.find_element_by_xpath('//span[contains(text(),"2")]/parent::h4/following-sibling::div[5]/input').send_keys(accountNo_2)
                # elem = driver.find_element_by_id("btn_continue").click()
                # time.sleep(2)
                # driver.find_element_by_xpath('//span[contains(text(), "PECOGAS Account Number")]/parent::div/button').click()
                # driver.find_element_by_xpath('//span[contains(text(), "Duquesne Light Supplier")]/parent::div/button').click()

        if payload.brand == 'NRG_regression':
            # if payload.account_type_1 == 'Electric':
            #     driver.find_element_by_class_name('uan required').send_keys(accountNo_1)

            if payload.utility_1 == 'Philadelphia Gas Works':
                driver.find_element_by_xpath("//span[contains(text(),'Service Point ID')]/following-sibling::input").send_keys(int(randint(1000000000, 9999999999)))
                driver.find_element_by_xpath("//span[contains(text(),'PGW Account Number')]/following-sibling::input[1]").send_keys(int(randint(1000000000, 9999999999)))
                driver.find_element_by_xpath("//span[contains(text(),'PGW Billing Account Number')]/following-sibling::input").send_keys(int(randint(1000000000, 9999999999)))
                driver.find_element_by_xpath("//button[text()= 'Check Account Number']").click()
                driver.find_element_by_xpath("//span[contains(text(),'PGW Account Number')]/following-sibling::button[1]").click()
                driver.find_element_by_xpath("//span[contains(text(),'PGW Billing Account Number')]/following-sibling::input[1]/following-sibling::button[1]").click()

            # if payload.utility_1 == 'Philadelphia Gas Works':
            #     try:
            #         elem - driver.find_element_by_class_name('point-id').send_keys(accountNo_1)
            #         elem = driver.find_element_by_class_name("check-account-number").click()

            # except:
            #         pass
                time.sleep(2)
                try:
                    elem = driver.find_element_by_class_name("extra-uan").send_keys(int(payload.servicereference))
                    elem = driver.find_element_by_class_name("check-extra-account-number").click()
                except:
                    pass
                elem = driver.find_element_by_class_name("check-account-number").click()

            if payload.account_type_2 == "Gas":
                elem=driver.find_element_by_class_name("uan").send_keys(accountNo_1)
                elem = driver.find_element_by_class_name("check-account-number").click()
                time.sleep(2)

                elem = driver.find_element_by_class_name("same-as-first").click()
                elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[4]/input[1]").click()
                elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/input").send_keys(
                    int(payload.accountNo_gas_1))
                elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/button").click()
            else:
                pass
        elem = driver.find_element_by_class_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_uan_name).send_keys(accountNo_1)
        # driver.find_element_by_class_name('check-account-number btn btn-primary btn-sm').click()
        # driver.find_element_by_class_name('check-account-number btn btn-primary btn-sm').click()

    except:
        elem = driver.find_element_by_class_name(
            Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_copy_to_billing_yes_name).click()
        elem = driver.find_element_by_class_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_uan_name).send_keys(accountNo_1)
    elem = driver.find_element_by_class_name(
        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_check_account_number_namber_name).click()
    # WebDriverWait(driver, 10).until(
    #     expected_conditions.visibility_of_element_located((By.XPATH, "//span[contains(text(),'Valid')]")))

    if  payload.state == 'Massachusetts':
        # try:
        #     if payload.account_tupe_1 == 'Electric':
        #         driver.find_element_by_class_name('uan required invalid-input').send_keys(accountNo_1)
        # except:
        #     pass
        try:
            servicereference = servicereference_generator()

            elem = driver.find_element_by_name(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_customer_key_name).send_keys("test")
            driver.find_element_by_xpath(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.customer_servicereference_xpath).send_keys(int(servicereference))
            # elem = driver.find_element_by_class_name(Inbound.States.tags.customer_check_extra_number_class_name).click()



            time.sleep(2)
        except:
            pass
    if payload.type == 'Business':
        try:
            elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div/div[4]/select')
            for option in elem.find_elements_by_tag_name(
                    Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
                if option.text == payload.monthly_usage:
                    option.click()
        except:
            pass
    try:
        Check_buttons = driver.find_elements_by_xpath('//button[contains(text(), "Check")]')
        for x in range(0, len(Check_buttons)):
            if Check_buttons[x].is_displayed():
                Check_buttons[x].click()
    except:
        pass

    # Todo - finish wait
    time.sleep(2)
    elem = driver.find_element_by_id(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.continue_button_id).click()

    ## Billing Info:
    wait_billing_page(driver)
    if payload.type == 'Business':
        try:
            driver.find_element_by_xpath(
                Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_businessName_radio_yes_xpath).click()
            driver.find_element_by_xpath(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_businessName_xpath).send_keys("Tester_busines_account")
        except:
            pass


    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_address_name).send_keys(payload.address)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_city_name).send_keys(city)
    elem = driver.find_element_by_class_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_state_class_name)
    for option in elem.find_elements_by_tag_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.options_tag_name):
        if option.text == payload.state:
            option.click()
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_zip_name).send_keys(zip_code)
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_phone_area_code_name).send_keys(int(payload.area_code))
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_phone_prefix_area_name).send_keys(int(payload.prefix))
    elem = driver.find_element_by_name(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_phone_last_digits_name).send_keys(int(payload.last))
    elem = driver.find_element_by_class_name(
        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_phone_email_no_class_name).click()
    elem = driver.find_element_by_class_name(
        Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.billing_phone_email_no_no_class_name).click()

    if payload.brand ==Energy_plus and payload.account_type_2 == "Electric" or payload.account_type_2 == "Gas":
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/div[2]/div[4]/input[2]').click() #no email
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]/div[2]/div[4]/div/div/div[1]/p[2]/input[2]').click()  #no email
        try:
            driver.find_element_by_class_name("same-as-first").click()
        except:
            pass

    if payload.brand == 'GreenMT' and payload.account_type_2 == "Gas":
        elem = driver.find_element_by_class_name("same-as-first").click()
        elem = driver.find_element_by_class_name("same-emailchoice-as-first").click()

    elem = driver.find_element_by_id(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.continue_button_id).click()


    time.sleep(2)

    ## Summary:
    summary(driver)

    ## Disclosure:
    if payload.brand == 'GreenMT':
        declouser_GreenME(driver)
    elif payload.brand == 'NRG_regression':
        declouser_NRG(driver)
    else:
        declouser_EP(driver)

    ## Grab Conformation Code

    grab_code(accountNo_1, payload)

    ## Submit:

    # if payload.state == 'Illinois' or "Maryland":
    #     elem = driver.find_element_by_id(Inbound.States.tags.submit_enroll_id).click()
    try:
        elem = driver.find_element_by_id(Inbound.States.Inbound_Enrollments_4brands_test.Inbound_tags.submit_enroll_id).click()
    except:
        pass


    wait_finish_page(driver)


def grab_code(accountNo_1, payload, zip_code, city):
    wait_grab_code_page(driver)
    elem = driver.find_element_by_id("confcode")
    confcode = elem.text
    print(
        "Passed " + sheet_name + " " + payload.test_name + ", Conformation =  " + confcode + ' for ' + payload.state + ' - ' + payload.utility_1)
    # if payload.utility_1 == 'PSE&G' or payload.utility_1 == 'PSE&G Gas' or payload.utility_1 == 'NYSEG' or payload.utility_1 == 'RG&E':
    #     accountNo = str(payload.accountNo_1)
    # else:
    #     accountNo = str(int(payload.accountNo_1))
    zip = str(int(payload.zip))
    f = open("./Inbound_Enrollments_tests_results.csv", 'w', newline='')
    now = datetime.now()
    time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
    csv_w = csv.writer(f)
    csv_w.writerow(["Passed", tester, payload.first_name, payload.brand, payload.state, payload.utility_1, confcode,
                    accountNo_1, payload.partner_1, payload.campaign_1, payload.promo_1, zip_code,city, time])
    # f.write(confcode+"\n" )
    # f.write("Passed "+"|"+ "TESTER: "+ tester + "|" + payload.first_name + "|" + sheet_name + "|"  + "|" + payload.state + "|" + payload.utility_1 + "|" + confcode + "|" + accountNo+ "|" + payload.partner_1
    #          + payload.campaign_1 + "|" + payload.promo_1 + "|" + zip + "|" + payload.city + "--" + time + "\n" )


def fill_greenMT_offer(payload):
    if payload.categorie_1 == 'SolarSPARC 10%12':
        driver.find_element_by_xpath('//span[contains(text(), "SolarSPARC")]').click()
        driver.find_element_by_id(payload.categorie_1).click()
    if payload.categorie_1 == 'SolarSPARC 10% 12':
        driver.find_element_by_xpath('//span[contains(text(), "SolarSPARC")]').click()
        driver.find_element_by_id(payload.categorie_1).click()
    if payload.categorie_1 == 'Pollution Free Farm to Market Reliable Rate' or 'Pollution Free TimeWise 12': #'Pollution Free Reliable Rate' or 'Pollution Free TimeWise 12'
        if payload.categorie_1 == 'Pollution Free Farm to Market Reliable Rate':  # Pollution Free Farm to Market Reliable Rate
            try:
                driver.find_element_by_xpath('//span[contains(text(), "Pollution Free Farm to Market Reliable Rate")]').click()
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

    if payload.categorie_1 == 'Pollution Free with Goal Zero 6' or 'Pollution Free with Goal Zero 24' or 'Pollution Free with Goal Zero 12':
        driver.find_element_by_xpath('//span[contains(text(), "Goal Zero")]').click()
        driver.find_element_by_id(payload.categorie_1).click()

    else:
        pass

