import csv
import os
from collections import namedtuple
from datetime import datetime
import pytest
import requests
import xlrd
from webdriver_manager.chrome import ChromeDriverManager

from Regression.Inbound.Inbound_Enrollments_promo_JULY_xlsx_test.InboundPromo_tests_Settings import *
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_BrandPage import BrandPage
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_accountNO_generator import account_generator_accountNo_1, servicereference_generator
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_loginPage import LoginPage
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_pages_methods import *
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_tags import *
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_generator_names_and_address import generator_names_and_address_work



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
    driver.maximize_window()
    def resource_a_teardown():
        request.addfinalizer(resource_a_teardown)
        driver.close()
        driver.quit()
        return driver


def grab_code(payload,  promo_text,  first_name, last_name, ServiceAddress1, account_number, offer_1,offer_2, offer_3, offer_4, ):
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
    date_for_report = now.strftime("%m.%d.%Y")
    csv_filename="./c_web_test_result/_Inbound" + test_name + date + "_passed_tests_results.csv"

    promo_text_cleaned = promo_text.replace(" ", "")
    ProductName_cleaned = payload.ProductName.replace(" ","")
    if promo_text_cleaned == ProductName_cleaned:
        text_checking = "text_passed"
    else:
        text_checking = 'text_failed'




    if os.path.isfile(csv_filename):
        f = open(csv_filename, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(
            [payload.ts, payload.StateSlug, payload.BrandSlug, payload.PartnerCode, payload.TermsOfServiceType,
              payload.PremiseType, payload.Commodity, payload.ChannelSlug, payload.SKU, payload.Bonus,
              payload.Ongoing_Earn, payload.promo_compaign_code, payload.PromoCode, payload.UtilitySlug, payload.Offer,
              payload.ECF_NoECF, payload.ProductName, payload.Bundle_Description, payload.ProductSlug, payload.System,
              payload.State_full_name, payload.utility_inb, payload.first_name, payload.last_name,
              payload.ServiceAddress1, payload.city, payload.zip_code, payload.account_no, payload.phone,
              payload.emailmarketing, payload.email, confcode, offer_1,offer_2, offer_3, offer_4,text_checking, date_for_report])

    else:
        f = open(csv_filename, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(
        ['ts', 'StateSlug', 'BrandSlug', 'PartnerCode', 'TermsOfServiceType', 'PremiseType', 'Commodity', 'ChannelSlug',
         'SKU', 'Bonus', 'Ongoing_Earn', 'promo_compaign_code', 'PromoCode', 'UtilitySlug', 'Offer', 'ECF_NoECF',
         'ProductName', 'Bundle_Description', 'ProductSlug', 'System', 'State_full_name', 'utility_inb', 'first_name',
         'last_name', 'ServiceAddress1', 'city', 'zip_code', 'account_no', 'phone', 'emailmarketing', 'email',
         'confcode', 'offer_1', 'offer_2', 'offer_3', 'offer_4', 'text_checking','date_for_report'])
        csv_a.writerow(
             [payload.ts, payload.StateSlug, payload.BrandSlug, payload.PartnerCode, payload.TermsOfServiceType,
              payload.PremiseType, payload.Commodity, payload.ChannelSlug, payload.SKU, payload.Bonus,
              payload.Ongoing_Earn, payload.promo_compaign_code, payload.PromoCode, payload.UtilitySlug, payload.Offer,
              payload.ECF_NoECF, payload.ProductName, payload.Bundle_Description, payload.ProductSlug, payload.System,
              payload.State_full_name, payload.utility_inb, payload.first_name, payload.last_name,
              payload.ServiceAddress1, payload.city, payload.zip_code, payload.account_no, payload.phone,
              payload.emailmarketing, payload.email, confcode, offer_1,offer_2, offer_3, offer_4,text_checking, date_for_report])


@pytest.mark.parametrize("payload", tests_values, ids=[p.ts for p in tests_values])
def test_state(test_setup, payload):
    now = datetime.now()
    time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")

    try:
        Inbound_start_test(driver, payload)
    except Exception as ae:
        filename = ("./failed/" + sheet_name + "_"+ str(time)+"_fail_{}_{}.png").format(payload.ts, time)
        driver.get_screenshot_as_file(filename)
        print("Saving screenshot of failed test - ", payload.ts)
        print("filename:", filename)
        print(str(ae))

        now = datetime.now()
        date = now.strftime("_%m_%d_%Y_")
        # failed_file = "./c_web_test_result/" + test_name + date + "_FAILED_tests_results.csv"
        # failed_file_list = "./c_web_test_result/FAILED.csv"
        add_filed = open("./c_web_test_result/FAILED.csv", 'a', newline='')
        csv_failed = csv.writer(add_filed)
        csv_failed.writerow([payload.ts])
        raise ae


def Inbound_start_test(test_setup, payload):

    global promo_code, campaign_code,  offer_1,offer_2, offer_3, offer_4, offer_5, offer_6
    address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generator_names_and_address_work()


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
    fill_get_started_page(payload, first_name_generated, last_name_generated)

    #Offer page:

    wait_offer_page(driver)
    time.sleep(2)
    #PROMO


    if payload.PromoCode[0:2] =="'0":
        promo_ = payload.PromoCode.replace("'0", '')
        promo_code= str("0")+str(promo_)
    else:
        promo_code = payload.PromoCode.replace("'", '')

    driver.find_element_by_xpath(offer_promo_partner_xpath).send_keys(payload.PartnerCode)
    driver.find_element_by_xpath(offer_promo_Campaign_xpath).send_keys(int(payload.promo_compaign_code))
    driver.find_element_by_xpath(offer_promo_Promo_xpath).send_keys(str(promo_code))
    driver.find_element_by_xpath(offer_submit_promoCode_xpath).click()
    #todo - changed to sku path
    wait_PROMO_OfferPlans_page(driver)
    # promo_text = driver.find_element_by_xpath("//*[@class='offer-category-product-listing ng-scope'][1]/div[2]/ul/li").text
    # a= payload.sku
    test_time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")


    # z= str (offer_path.replace('\', ''))
    offer_link_list = []
    offer_name_list = []

    try:
        offer_link = ("//div[@class='offer-products']/div/div/div[2]")
        offer_1 = driver.find_element_by_xpath(offer_link).text
        offer_link_list.append(offer_link)
        offer_name_list.append(offer_1)
    except:
        offer_1= ''
    try:
        offer_link_2 = ("//div[@class='offer-products']/div/div/div[3]")
        offer_2 = driver.find_element_by_xpath(offer_link_2).text
        a=offer_2
        offer_link_list.append(offer_link_2)
        offer_name_list.append(offer_2)

    except:
        offer_2 = ''
    try:
        offer_link_3= ("//div[@class='offer-products']/div/div/div[4]")
        offer_3 = driver.find_element_by_xpath(offer_link_3).text
        a=offer_3
        offer_link_list.append(offer_link_3)
        offer_name_list.append(offer_3)

    except:
        offer_3 = ''
    try:
        offer_link_4= ("//div[@class='offer-products']/div/div/div[5]")
        offer_4 = driver.find_element_by_xpath(offer_link_4).text
        offer_link_list.append(offer_link_4)
        offer_name_list.append(offer_4)

    except:
        offer_4 = ''
    # try:
    #     offer_link = ('/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/div[1]/div/div[6]/ul/li[1]')
    #     offer_5 = driver.find_element_by_xpath(offer_link).text
    #     offer_link_list.append(offer_link)
    #     offer_name_list.append(offer_5)
    #
    # except:
    #     offer_5 = ''
    # try:
    #     offer_link = '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/div[1]/div/div[7]/ul/li[1]'
    #     offer_6 = driver.find_element_by_xpath(offer_link).text
    #     offer_link_list.append(offer_link)
    #     offer_name_list.append(offer_6)
    #
    #
    # except:
    #     offer_6 = ''

    try:
            offer_path = "//li[contains(@id,'"+payload.SKU+"')]"
            promo_text_ = driver.find_element_by_xpath(offer_path).text
            driver.find_element_by_xpath(offer_path).click()

    except:
        for offer, link in zip(offer_name_list, offer_link_list):
            if offer == payload.ProductName:
                offer_link = link
                promo_text_ = driver.find_element_by_xpath(offer_link).text
                driver.find_element_by_xpath(offer_link).click()

            else:
                promo_text_=''





    if len(promo_text_)>0:
        promo_text = promo_text_
    else:
        promo_text = driver.find_element_by_xpath("//*[@class='offer-category-product-listing ng-scope'][1]/div[2]/ul/li").text

    driver.find_element_by_name(continue_button_name).click()
    filename = ("./screenshots/" + test_name + "_{}_{}_{}.png").format(payload.ts, payload.StateSlug, payload.UtilitySlug, test_time)
    driver.get_screenshot_as_file(filename)

    #Costomer Info page:

    wait_costumer_info_page(driver)
    zip_= payload.zip_code
    try:
        zipcode = zip_.replace ("'", "")
    except:
        zipcode = str(payload.zip_code)
    if len(zipcode)==4:
        zipcode_=(str('0')+str(zipcode))
    elif len(zipcode)==3:
        zipcode_=(str('00')+str(zipcode))
    elif len(zipcode) == 2:
        zipcode_ = (str('000') + str(zipcode))
    else:
        zipcode_ = zipcode


    if len (payload.first_name)>0:
        first_name = payload.first_name
    else:
        first_name = first_name_generated

    if len (payload.last_name)>0:
        last_name = payload.last_name
    else:
        last_name = last_name_generated


    if len (payload.ServiceAddress1)>0:
        ServiceAddress1 = payload.ServiceAddress1
    else:
        ServiceAddress1 = address_house_street_generated

    if len (payload.account_no)>0:
        accountNo = payload.account_no
    else:
        given_utiity = payload.UtilitySlug
        accountNo = str(account_generator_accountNo_1(given_utiity))



    elem = driver.find_element_by_name(customer_firs_name_name).send_keys(first_name)
    elem = driver.find_element_by_name(customer_last_name_name).send_keys(last_name)
    elem = driver.find_element_by_name(customer_service_address_1_name).send_keys(ServiceAddress1)
    # elem = driver.find_element_by_name(customer_service_address_2_name).send_keys(payload.ServiceAddress2)
    elem = driver.find_element_by_name(customer_city_name).send_keys(payload.city)
    elem = driver.find_element_by_name(customer_zip_name).send_keys(str(zipcode))
    phone_nuber = str(payload.phone)
    phone_area_code = phone_nuber[:3]
    phone_prefix=phone_nuber[3:6]
    phone_last = phone_nuber[6:10]
    elem = driver.find_element_by_name(customer_phone_area_code_name).send_keys(int(phone_area_code))
    elem = driver.find_element_by_name(customer_prefix_name).send_keys(int(phone_prefix))
    elem = driver.find_element_by_name(customer_last_digit_name).send_keys(phone_last)
    try:
        account_number = (accountNo.replace("'", ''))
    except:
        account_number = accountNo
    elem = driver.find_element_by_class_name(customer_uan_name).send_keys(account_number)



    if payload.StateSlug == 'MA':
        servicereference = servicereference_generator(payload)
        try:
            elem = driver.find_element_by_name(customer_customer_key_name).send_keys("test")
            driver.find_element_by_xpath(customer_servicereference_xpath).send_keys(int(servicereference))
            time.sleep(2)
        except:
            pass


    if payload.UtilitySlug == 'PGW':
        driver.find_element_by_xpath(costumer_ServicePointID_input_Xpath).send_keys(int(account_number))
        driver.find_element_by_xpath(costumer_PGW_Account_input_xpath).send_keys(int(account_number))
        driver.find_element_by_xpath(costumer_PGW_BillingAccount_NRG_input_xpath).send_keys(int(account_number))

    time.sleep(2)
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
    fill_billing_info_page(payload, address_house_street_generated)

    # Summary:
    summary(driver)


    # Disclosure:
    declouser_NRG(driver, payload)

    #Grab Conformation Code
    grab_code(payload, promo_text,  first_name, last_name, ServiceAddress1, account_number, offer_1, offer_2, offer_3, offer_4 )

    ## Submit        :
    try:
        elem = driver.find_element_by_id(submit_enroll_id).click()
    except:
        pass
    #
    wait_finish_page(driver)
    driver.find_element_by_id(start_new_call_id).click()

def fill_billing_info_page(payload, address_house_street_generated):
    if len (payload.ServiceAddress1)>0:
        ServiceAddress1 = payload.ServiceAddress1
    else:
        ServiceAddress1 = address_house_street_generated



    elem = driver.find_element_by_name(billing_address_name).send_keys(ServiceAddress1)
    # elem = driver.find_element_by_name(billing_address_name_2).send_keys(payload.ServiceAddress2)
    elem = driver.find_element_by_name(billing_city_name).send_keys(payload.city)
    elem = driver.find_element_by_class_name(billing_state_class_name)

    for option in elem.find_elements_by_tag_name(options_tag_name):
        if option.text == payload.State_full_name:
            option.click()
    zip_ = payload.zip_code
    try:
        zipcode = zip_.replace("'", "")
    except:
        zipcode = str(payload.zip_code)
    if len(zipcode)==4:
        zipcode_=(str('0')+str(zipcode))
    elif len(zipcode)==3:
        zipcode_=(str('00')+str(zipcode))
    elif len(zipcode) == 2:
        zipcode_ = (str('000') + str(zipcode))
    else:
        zipcode_ = zipcode

    phone_nuber = str(payload.phone)
    phone_area_code = phone_nuber[:3]
    phone_prefix=phone_nuber[3:6]
    phone_last = phone_nuber[6:10]
    elem = driver.find_element_by_name(billing_zip_name).send_keys(str(zipcode_))
    elem = driver.find_element_by_name(billing_phone_area_code_name).send_keys(int(phone_area_code))
    elem = driver.find_element_by_name(billing_phone_prefix_area_name).send_keys(int(phone_prefix))
    elem = driver.find_element_by_name(billing_phone_last_digits_name).send_keys(int(phone_last))

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


def fill_get_started_page(payload,first_name_generated, last_name_generated):

    if len (payload.first_name)>0:
        first_name = payload.first_name
    else:
        first_name = first_name_generated

    if len (payload.last_name)>0:
        last_name = payload.last_name
    else:
        last_name = last_name_generated
    driver.find_element_by_id(get_started_First_name_id).send_keys(first_name)
    driver.find_element_by_id(get_started_last_name_id).send_keys(last_name)
    wait_get_started_page_state_list(driver)
    # What state are you are calling from?
    elem = driver.find_element_by_name(get_started_state_list_id)
    for option in elem.find_elements_by_tag_name(options_tag_name):
        if option.text == payload.State_full_name:
            option.click()
    # Is Your Name on the Utility Bill?
    if payload.StateSlug.upper()== "MD":
        # Is Your Name on the Utility Bill?
        try:
            elem = driver.find_element_by_xpath(get_started_name_utility_yes_xpath).click()
        except:
            pass
    # What account are you calling about today? - gas or electric
    try:
        if payload.Commodity.lower() == 'electric':
            elem = driver.find_element_by_class_name(get_call_account_electric_class_name).click()
        if payload.Commodity.lower() == 'gas':
            elem = driver.find_element_by_class_name(get_call_account_gas_class_name).click()

    except:
        pass
    # Who is the provider for your electric account?

    # elem = driver.find_element_by_name(get_started_EL_utility_1_class_name)

    if payload.UtilitySlug == 'ace':
        utility = 'Atlantic City Electric'
    elif payload.UtilitySlug == 'aepn':
        utility = 'AEP Ohio'
    elif payload.UtilitySlug == 'aeps':
        utility = 'AEP Ohio'
    elif payload.UtilitySlug == 'Ameren':
        utility = 'Ameren'
    elif payload.UtilitySlug == 'apmd':
        utility = 'Potomac Edison'
    elif payload.UtilitySlug == 'beco':
        utility = 'Eversource (Eastern Massachusetts)'
    elif payload.UtilitySlug == 'bge':
        utility = 'BGE'
    elif payload.UtilitySlug.upper() == 'CEI':
        utility = 'The Illuminating Company'
    elif payload.UtilitySlug == 'come':
        utility = payload.utility_inb
    elif payload.UtilitySlug.lower() == 'comed':
        utility = 'ComEd'
    elif payload.UtilitySlug == 'delmarva':
        utility = 'Delmarva Power'
    elif payload.UtilitySlug == 'dpl':
        utility = 'Dayton Power & Light'
    elif payload.UtilitySlug == 'dukeoh':
        utility = 'Duke Energy Ohio'
    elif payload.UtilitySlug == 'duq':
        utility = 'Duquesne Light Company'
    elif payload.UtilitySlug == 'jcpl':
        utility = 'Jersey Central Power & Light (JCP&L)'
    elif payload.UtilitySlug == 'meco':
        utility = 'National Grid'
    elif payload.UtilitySlug == 'meted':
        utility = 'Met-Ed'
    elif payload.UtilitySlug == 'ngntkt':
        utility = 'National Grid'
    elif payload.UtilitySlug.upper() == 'OE':
        utility = 'Ohio Edison'
    elif payload.UtilitySlug == 'peco':
        utility = 'PECO'
    elif payload.UtilitySlug == 'penelec':
        utility = 'Penelec'
    elif payload.UtilitySlug == 'penn':
        utility = 'Penn Power'
    elif payload.UtilitySlug == 'pepco':
        utility = 'Pepco'
    elif payload.UtilitySlug == 'ppl':
        utility = 'PPL Electric Utilities'
    elif payload.UtilitySlug == 'pseg':
        utility = 'PSE&G'
    elif payload.UtilitySlug.lower() == 'reco':
        utility = 'Rockland Electric Company (O&R)'
    elif payload.UtilitySlug == 'te':
        utility = 'Toledo Edison'
    elif payload.UtilitySlug == 'wmeco':
        utility = 'Eversource (Western Massachusetts)'
    elif payload.UtilitySlug == 'camb':
        utility = 'Eversource (Eastern Massachusetts)'
    elif payload.UtilitySlug.lower() == 'come':
        utility = 'Eversource (Western Massachusetts)'
    elif payload.UtilitySlug == 'wpp':
        utility = 'West Penn Power'
    elif payload.UtilitySlug == 'PEOPGAS':
        utility = 'Peoples Gas'
    elif payload.UtilitySlug == 'NICOR':
        utility = 'Nicor Gas'
    elif payload.UtilitySlug == 'PSEG Gas':
        utility = 'PSE&G Gas'
    elif payload.UtilitySlug == 'NJNG':
        utility = 'South Jersey Gas'
    elif payload.UtilitySlug == 'SJersey':
        utility = 'South Jersey Gas'
    elif payload.UtilitySlug == 'COLOHG':
        utility = 'Columbia Gas of Ohio'
    elif payload.UtilitySlug == 'DUKEOHG':
        utility = 'Duke Energy Ohio'
    elif payload.UtilitySlug == 'DEOHG':
        utility = 'Dominion East Ohio'
    elif payload.UtilitySlug == 'COLPAG':
        utility = 'Columbia Gas of Pennsylvania'
    elif payload.UtilitySlug == 'PNGPA':
        utility = 'Peoples Gas'
    elif payload.UtilitySlug == 'UGIG':
        utility = 'UGI South'
    elif payload.UtilitySlug == 'PECO-GAS':
        utility = 'PECO Gas'
    elif payload.UtilitySlug == 'PGW':
        utility = 'Philadelphia Gas Works'
    elif payload.UtilitySlug == 'NFGPA':
        utility = 'National Fuel Gas Company (PA)'
    elif payload.UtilitySlug == 'BGG':
        utility = 'BGE'
    elif payload.UtilitySlug == 'WGL':
        utility = 'Washington Gas'
    else:
        utility = payload.UtilitySlug

    # if payload.UtilitySlug == 'aeps':
    #     for option in elem.find_elements_by_tag_name(options_tag_name):
    #         c=option.text
    #         if option.text == 'AEP Ohio':
    #             option.click()
    # else:
    elem = driver.find_element_by_name(get_started_EL_utility_1_class_name)
    for option in elem.find_elements_by_tag_name(options_tag_name):
        a=option.text
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

    try:
        if payload.Commodity.lower() == 'gas':
            driver.find_element_by_class_name(get_started_gas_Both_class_name).click()
        else:
            pass
    except:
        pass


    # Save and continue button
    elem = driver.find_element_by_id(get_started_save_and_con_but_id).click()


