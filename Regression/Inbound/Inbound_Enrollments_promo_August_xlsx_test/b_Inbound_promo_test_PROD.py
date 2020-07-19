import csv
import os
import random
from collections import namedtuple
from datetime import datetime
import pytest
import xlrd
from webdriver_manager.chrome import ChromeDriverManager
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_BrandPage import BrandPage
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_accountNO_generator import account_generator_accountNo_1, servicereference_generator
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_loginPage import LoginPage
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_pages_methods import *
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_tags import *
from Regression.Inbound.Inbound_Enrollments_promo_MAY_xlsx_test._helpers.Inbound_generator_names_and_address import generator_names_and_address_work

test_name = "_May_campaign"
chosen_driver = "chrome"  #choose "firefox" or "chrome"
env = 'pt'
# start_page = 'http://www.pt.energypluscompany.com/myinbound/tab_brand.php'

# URL = "http://www.energypluscompany.com/myinbound/login.php"
# start_page = 'http://www.pt.energypluscompany.com/myinbound/tab_brand.php'
# URL = "http://www.pt.energypluscompany.com/myinbound/tab_brand.php"
start_page = "http://www.energypluscompany.com/myinbound/login.php"
URL = "http://www.energypluscompany.com/myinbound/login.php"

# login_email_data = "aleksandr.malygin@nrg.com"
# login_password_data = "energy"
login_email_data = "Gurjeet.Saini@nrg.com"
login_password_data = "energy"
tester = "Alex"
workbook_name = "./b_files_for_testing_02/MAY_inbound_data_file.xlsx"
# data_sheet_name = 'Inbound_Test_Data'
data_sheet_name = 'Sheet1'

start_string = "242"


phone_area_code_generated = random.randint(100, 999)
phone_prefix_generated = random.randint(100, 999)
phone_last_generated = random.randint(1000, 9999)



promo_text_gas = 'Cash Back Natural Gas Plan'
promo_text_electric = 'Cash Back Electric Plan'

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


def grab_code(payload,  offer_1, offer_2, offer_3, offer_4, offer_5, offer_6, promo_text ):
    # global confcode
    # wait_grab_code_page(driver)
    #
    # try:
    #     confcode = driver.find_element_by_id("confcode").text
    # except:
    #     pass
    #
    # if payload.emailmarketing =='emailmarketing':
    #     driver.find_element_by_id('toggle_xsell_consent_yes').click()
    # else:
    #     pass


    now = datetime.now()
    date = now.strftime("_%m_%d_%Y_")
    csv_filename="./c_web_test_result/prod_Inbound" + test_name + date + "_passed_tests_results.csv"



    if promo_text == payload.ProductName:
        text_checking = "text_passed"
    else:
        text_checking = 'text_failed'


    f = open(csv_filename, 'a', newline='')
    csv_a = csv.writer(f)
    csv_a.writerow(
        [payload.ts, 	payload.PremiseType, 	payload.sku, 	payload.BrandSlug, 	payload.ChannelSlug,
         payload.ProductName, 	payload.TermsOfServiceTyp,
            payload.UtilitySlug, 	 payload.PartnerCode, payload.PromoCode,   payload.promo_compaign_code, payload.Commodity,
            payload.StateSlug,
         payload.email, 	payload.emailmarketing, date_,   text_checking,  offer_1, offer_2, offer_3, offer_4, offer_5, offer_6 ])


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

        f = open("./c_web_test_result/_" + test_name + date + "_FAILED_tests_results.csv", 'a', newline='')
        now = datetime.now()
        # time = now.strftime("%m_%d_%Y_%I_%M_%S_%p")
        csv_a = csv.writer(f)
        # address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generaot_names_and_address_work()
        csv_a.writerow(
            [payload.ts, 	payload.PremiseType, 	payload.sku, 	payload.BrandSlug, 	payload.ChannelSlug,
             payload.ProductName, 	payload.TermsOfServiceTyp, 		str(payload.account_no),
             payload.first_name, 	payload.last_name, 	payload.UtilitySlug, 	payload.Commodity,
             payload.ServiceAddress1, 	payload.ServiceAddress2, 	payload.city, 	payload.StateSlug, 	str("'" + str(int(payload.zip_code))),
             payload.email, 	payload.emailmarketing, date_,  "Failed"])
        raise ae


def Inbound_start_test(test_setup, payload):

    global promo_code, campaign_code,  offer_1,offer_2, offer_3, offer_4, offer_5, offer_6
    address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated = generator_names_and_address_work()


    if driver.current_url == start_page:
        pass
    else:
        driver.get(start_page)
        print(URL)
        # Login page
        login = LoginPage(driver)
        email_textbox_id = "email"
        password_textbox_id = "password"
        login_button_id = "button"
        driver.find_element_by_name(email_textbox_id).send_keys(login_email_data)
        driver.find_element_by_name(password_textbox_id).send_keys(login_password_data)
        driver.find_element_by_id(login_button_id).click()

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
    #

    z=payload.PromoCode
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
    filename = ("./screenshots/prod_" + test_name + "_{}_{}_{}.png").format(payload.ts, payload.StateSlug, payload.UtilitySlug, test_time)
    driver.get_screenshot_as_file(filename)
    # z= str (offer_path.replace('\', ''))
    offer_link_list = []
    offer_name_list = []
    try:

        offer_link = ('/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/div[1]/div/div[2]/ul/li[1]')
        offer_1 = driver.find_element_by_xpath(offer_link).text
        a=offer_1
        offer_link_list.append(offer_link)
        offer_name_list.append(offer_1)
    except:
        offer_1= ''
    try:
        offer_link_2 = ('/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/div[1]/div/div[3]/ul/li[1]')
        offer_2 = driver.find_element_by_xpath(offer_link_2).text
        a=offer_2
        offer_link_list.append(offer_link_2)
        offer_name_list.append(offer_2)

    except:
        offer_2 = ''
    try:
        offer_link_3= ('/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/div[1]/div/div[4]/ul/li[1]')
        offer_3 = driver.find_element_by_xpath(offer_link_3).text
        a=offer_3
        offer_link_list.append(offer_link_3)
        offer_name_list.append(offer_3)

    except:
        offer_3 = ''
    try:
        offer_link_4= ('/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/div[1]/div/div[5]/ul/li[1]')
        offer_4 = driver.find_element_by_xpath(offer_link_4).text
        offer_link_list.append(offer_link_4)
        offer_name_list.append(offer_4)

    except:
        offer_4 = ''
    try:
        offer_link = ('/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/div[1]/div/div[6]/ul/li[1]')
        offer_5 = driver.find_element_by_xpath(offer_link).text
        offer_link_list.append(offer_link)
        offer_name_list.append(offer_5)

    except:
        offer_5 = ''
    try:
        offer_link = '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/div[1]/div/div[7]/ul/li[1]'
        offer_6 = driver.find_element_by_xpath(offer_link).text
        offer_link_list.append(offer_link)
        offer_name_list.append(offer_6)


    except:
        offer_6 = ''

    try:
            offer_path = "//li[contains(@id,'"+payload.sku+"')]"
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

    #Grab Conformation Code
    grab_code(payload,  offer_1, offer_2, offer_3, offer_4, offer_5, offer_6, promo_text )



def fill_billing_info_page(payload, address_house_street_generated):
    if len (payload.ServiceAddress1)>0:
        ServiceAddress1 = payload.ServiceAddress1
    else:
        ServiceAddress1 = address_house_street_generated



    elem = driver.find_element_by_name(billing_address_name).send_keys(ServiceAddress1)
    elem = driver.find_element_by_name(billing_address_name_2).send_keys(payload.ServiceAddress2)
    elem = driver.find_element_by_name(billing_city_name).send_keys(payload.city)
    elem = driver.find_element_by_class_name(billing_state_class_name)

    for option in elem.find_elements_by_tag_name(options_tag_name):
        if option.text == payload.StateSlug:
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
    elem = driver.find_element_by_name(billing_zip_name).send_keys(str(zipcode_))
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
        utility = 'National Grid'
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
    elif payload.UtilitySlug == 'RECO':
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


