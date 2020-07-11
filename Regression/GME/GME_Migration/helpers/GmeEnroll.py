import csv

import os
import time
import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
from Regression.GME.GME_Migration.helpers.generator_names_and_address import generator_names_and_address_work
from Regression.GME.GME_Migration.helpers.generator import find_zip_city
from Regression.GME.GME_Migration.helpers.accountNO_generator import  account_generator_accountNo_1



def fill_personalinformation(driver,  payload):
    global generated_zipCode_, first_name, ServiceAddress1, accountNo, email_given, zipCode, city
    zipcode_mainpage_loc = "zip-code"
    view_plans_loc = 'zip-search'
    firstName_loc = "id_first_name"
    lastName_loc = "id_last_name"
    email_loc = "id_email"
    verifyEmail_loc = "id_ver_email"
    phoneNum_loc = "id_phone"
    streetAdd_loc = "id_service_address_1"
    city_loc = "id_service_address_city"
    zipcode_loc = "id_service_address_zip"
    agreementId_loc = "id_electric-uan"
    ac_wmeco_number  = "id_electric-billing_uan"
    continueBtn = "//*[@class='button green continue']"
    acctNo_loc = "id_electric-billing_uan"
    verification_chkbox_loc = 'id_order_authorization'  # id
    tos_verification_page_loc = 'tos-section'  # class
    submit_ver_page_loc = "//*[@class='button  continue']"

    authLabel_loc = "//*[contains(text(),'Authorization')]"
    termsCond1_loc = "id_order_authorization"

    # termsCond2_loc = "id_affiliate_consent"
    tosSection_loc = "tos-section"
    afferm_loc = "id_crs_order_authorization"
    ptc_loc = "id_ptc_consent"
    LowIncome_loc = "id_li_consent"

    address_house_street_generated, first_name_generated, last_name_generated, phone_area_code_generated, phone_last_generated, phone_prefix_generated= generator_names_and_address_work()
    generated_zipCode,generated_city = find_zip_city(payload.UtilitySlug, payload.StateSlug)
    accountNo_1 = account_generator_accountNo_1(payload.UtilitySlug)

    try:
        driver.switch_to.alert()
        driver.find_element_by_id("mcx_decline").click()
        # time.sleep(1)
    except:
        pass

    try:
        driver.switch_to.alert()
        driver.find_element_by_id("mcx_decline").click()
        # time.sleep(1)
    except:
        pass
    # time.sleep(4)
    a=payload.zip_code
    try:
        driver.find_element_by_id('close-uds').click()
    except:
        pass
    if len(payload.zip_code)>0:
        try:
            generated_zipCode_ = payload.zip_code.replace("'", '')
        except:
            generated_zipCode_=payload.zip
        b=generated_zipCode_
        if len (str(generated_zipCode_))==4:
            zipCode = str("0")+str(generated_zipCode_)
        else:
            zipCode = payload.zip_code.replace("'", '')
    else:
        zipCode=payload.zip_code.replace("'", '')



    if len(payload.city)>0:
        city = payload.city
    else:
        city =   generated_city


    if len(payload.first_name) > 0:
        first_name = payload.first_name
    else:
        first_name = first_name_generated

    if len(payload.last_name) > 0:
        last_name = payload.last_name
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

    driver.find_element_by_id(firstName_loc).send_keys(first_name)
    driver.find_element_by_id(lastName_loc).send_keys(last_name)
    driver.find_element_by_id(email_loc).send_keys(email_given)
    # driver.find_element_by_id(verifyEmail_loc).send_keys(email_given)
    if payload.emailmarketing=='emailmarketing' or payload.emailmarketing=='bounce':
        pass
    else:
        driver.find_element_by_id('id_newsletter').click()
    driver.find_element_by_id(phoneNum_loc).send_keys(phone_number)
    driver.find_element_by_id(streetAdd_loc).send_keys(ServiceAddress1)
    driver.find_element_by_id(city_loc).send_keys(city)
    driver.find_element_by_id(zipcode_loc).send_keys(str(zipCode))
    # driver.switch_to.alert()
    try:
        driver.switch_to.alert()
        driver.find_element_by_id("mcx_decline").click()
    except:
        pass
    try:
        driver.find_element_by_id('close-uds').click()
    except:
        pass
    try:
        driver.dismiss_alert()
    except:
        pass
    time.sleep(2)
    try:
        assert driver.find_element_by_id(firstName_loc).get_attribute('value') == first_name
    except:
        driver.find_element_by_id(firstName_loc).send_keys(first_name)
    try:
        assert driver.find_element_by_id(lastName_loc).get_attribute('value') == last_name
    except:
        driver.find_element_by_id(lastName_loc).send_keys(last_name)
    try:
        assert driver.find_element_by_id(email_loc).get_attribute('value') == email_given
    except:
        driver.find_element_by_id(email_loc).send_keys(email_given)
    # try:
    #     assert driver.find_element_by_id(verifyEmail_loc).get_attribute('value') == email_given
    # except:
    #     driver.find_element_by_id(verifyEmail_loc).send_keys(email_given)
    try:
        assert driver.find_element_by_id(phoneNum_loc).get_attribute('value') == phone_number
    except:
        driver.find_element_by_id(phoneNum_loc).send_keys(phone_number)
    try:
        assert driver.find_element_by_id(streetAdd_loc).get_attribute('value') == ServiceAddress1
    except:
        driver.find_element_by_id(streetAdd_loc).send_keys(ServiceAddress1)
    try:
        assert driver.find_element_by_id(city_loc).get_attribute('value') == city
    except:
        driver.find_element_by_id(city_loc).send_keys(city)
    try:
        assert driver.find_element_by_id(zipcode_loc).get_attribute('value') == str(zipCode)
    except:
        driver.find_element_by_id(zipcode_loc).send_keys(str(zipCode))

    #close allert
    try:
        driver.dismiss_alert()
    except:
        pass
    try:
        driver.switch_to.alert()
        driver.find_element_by_id("mcx_decline").click()
    except:
        pass
    #verify - the name fields is full
    # check_fields_are_filled(driver, address, generated_city, first_name_generated, generated_zipCode, phone_number, email_given)

    #check full name of utility
    utility_grabbed = driver.find_element_by_xpath("//div[@class='cell cell-account-number']/span[2]").text

    try:
        account_number = (accountNo.replace("'", ''))
    except:
        account_number = accountNo

    driver.find_element_by_id(agreementId_loc).send_keys(account_number)
    if payload.UtilitySlug.lower() == 'wmeco':
        driver.find_element_by_id(ac_wmeco_number).send_keys(account_number)




    try:
      account_details_loc = driver.find_element_by_xpath("//div//div//*[contains(text(),'Account Details')]")
      driver.execute_script("return arguments[0].scrollIntoView();", account_details_loc)
    except:

      pass
    try:
        driver.switch_to.alert()
        driver.find_element_by_id("mcx_decline").click()
    except:
        pass

    try:
      # time.sleep(3)
      United_MileagePlusMiles_loc = driver.find_element_by_xpath("//div//div//*[contains(text(),'United MileagePlus Miles')]")
      # time.sleep(4)
      driver.execute_script("return arguments[0].scrollIntoView();", United_MileagePlusMiles_loc)
      # time.sleep(2)
    except:
     pass
    # time.sleep(30)
    try:
        driver.switch_to.alert()
        driver.find_element_by_id("mcx_decline").click()
    except:
        pass
    time.sleep(10)
    driver.find_element_by_xpath("//input[@class='button green continue']").click()
    WebDriverWait(driver, 30).until(expected_conditions.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'About You')]")))


def gme_scroll_termsandconditions_and_agree(driver, payload):
    driver.execute_script("window.scrollTo(0,300);")
    end_tos = driver.find_element_by_id('greentxt2')
    driver.execute_script("return arguments[0].scrollIntoView();", end_tos)
    print('scrolled')
    driver.implicitly_wait(5)
    driver.find_element_by_id('id_order_authorization').click() # id_order_authorization
    # self.clickTermsCond2()  # id_affiliate_consent
    driver.implicitly_wait(5)
    if payload.StateSlug.upper() == "IL":

        time.sleep(2)
        driver.find_element_by_id( "id_crs_order_authorization").click()
        time.sleep(2)
        driver.find_element_by_id( "id_ptc_consent").click()
        time.sleep(2)
        driver.find_element_by_id( "id_li_consent").click()

    else:
        pass
    driver.find_element_by_xpath("//input[@class='button  continue']").click()


def get_confirmation_number( driver, payload):
    WebDriverWait(driver, 50).until(
        expected_conditions.visibility_of_element_located((By.XPATH, "//*[@class='processing']/strong")))
    time.sleep(1)
    confirm_gme_text = driver.find_element_by_xpath("//*[@class='processing']/strong").text
    print(confirm_gme_text)

    now = datetime.now()
    current_time = now.strftime("_%m_%d_%Y")

    time.sleep(2)
    account_from_page = driver.find_element_by_id("id_electric-uan").text

    driver.get("http://nerf.api.gme-plus.nrgpl.us/api/v1/orders/?enrollment_number=" + str(confirm_gme_text))
    order_status_xpath = driver.find_element_by_xpath(
        '//span[contains(text(),"order_status")] [1]/following-sibling::span[3]').text
    order_status = order_status_xpath.replace('"', '')

    driver.find_element_by_xpath("//*[@id='content']/div[1]/div[4]/pre/a[1]").click()
    allow_email_marketing = driver.find_element_by_xpath(
        "//span[contains(text(),'allow_email_marketing')]/following-sibling::span[3]").text

    driver.get("http://nerf.api.gme-plus.nrgpl.us/api/v1/orders/?enrollment_number=" + str(confirm_gme_text))
    driver.find_element_by_xpath("//*[@id='content']/div[1]/div[4]/pre/a[2]").click()
    sap = driver.find_element_by_xpath(
        "//span[contains(text(),'sap_enrollment_confirmation')]/following-sibling::span[3]").text
    sap = sap.replace('"', '')

    report_csv  = "./outbox_files/GME_Migration" +str(current_time)+".csv"
    if os.path.isfile(report_csv):
        f = open(report_csv, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(
            [payload.ts, payload.sku, payload.ChannelSlug, payload.BrandSlug, payload.PremiseType, payload.TermsOfServiceType,
             payload.ProductName, payload.ProductSlug, payload.StateSlug, payload.Commodity, payload.UtilitySlug,
             first_name, payload.UtilitySlug, ServiceAddress1,
             str("'" + str(zipCode)), city, str("'" + str(accountNo)), email_given, payload.emailmarketing,
             confirm_gme_text, order_status, allow_email_marketing, current_time, sap])

    else:
        f = open(report_csv, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(
            ['ts', 'sku', 'ChannelSlug', 'BrandSlug', 'PremiseType', 'TermsOfServiceTyp',
             'ProductName', 'ProductSlug', 'StateSlug', 'Commodity', 'UtilitySlug',
             'first_name', 'last_name', 'ServiceAddress1',
             'zip_code', 'city', 'account_no', 'email', 'emailmarketing', 'confirm_number', 'order_status', 'allow_email_marketing', "test_time", "sap_number"])
        csv_a.writerow(
            [payload.ts, payload.sku, payload.ChannelSlug, payload.BrandSlug, payload.PremiseType, payload.TermsOfServiceType,
             payload.ProductName, payload.ProductSlug, payload.StateSlug, payload.Commodity, payload.UtilitySlug,
             first_name, payload.UtilitySlug, ServiceAddress1,
             str("'" + str(zipCode)), city, str("'" + str(accountNo)), email_given, payload.emailmarketing,
             confirm_gme_text,order_status, allow_email_marketing,  current_time, sap])

    time.sleep(2)