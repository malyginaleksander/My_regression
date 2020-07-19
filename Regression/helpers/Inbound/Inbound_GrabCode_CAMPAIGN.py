import csv
import os
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def grab_code_CAMPAIGN(driver, payload, test_name, firstname, lastname, address, zipcode_, city, accountNo, email,
                       phonenumber,promo_text, offer_1, offer_2, offer_3, offer_4, offer_5, offer_6 ):
    global confcode
    WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.ID, 'confcode')))
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


    report_list = [payload.ts, payload.Brand,  payload.StateSlug, payload.State, payload.BrandSlug, payload.PartnerCode, payload.TermsOfServiceType,
              payload.PremiseType, payload.Commodity, payload.ChannelSlug, payload.SKU, payload.Bonus,
              payload.Ongoing_Earn, payload.promo_compaign_code, payload.PromoCode, payload.UtilitySlug, payload.Offer,
              payload.ECF_NoECF, payload.ProductName, payload.Bundle_Description, payload.ProductSlug, payload.System,
               payload.utility_inb, firstname,lastname,
              address, zipcode_, city, accountNo, phonenumber, email,
              payload.emailmarketing,  confcode,
              offer_1, offer_2, offer_3, offer_4, offer_5, offer_6,
              text_checking, date_for_report]



    if os.path.isfile(csv_filename):
        f = open(csv_filename, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(report_list)

    else:
        f = open(csv_filename, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(
        ['ts', 'Brand', 'StateSlug', 'State_full_name', 'BrandSlug', 'PartnerCode', 'TermsOfServiceType',
         'PremiseType', 'Commodity', 'ChannelSlug', 'SKU', 'Bonus',
         'Ongoing_Earn', 'promo_compaign_code', 'PromoCode', 'UtilitySlug', 'Offer',
         'ECF_NoECF', 'ProductName', 'Bundle_Description', 'ProductSlug', 'System',
          'utility_inb', 'first_name','last_name',
         'ServiceAddress1', 'zip_code', 'city',  'account_no', 'phone',  'email',
         'emailmarketing', 'confcode',
         'offer_1', 'offer_2', 'offer_3', 'offer_4', 'offer_5','offer_6',
         'text_checking','date_for_report'])
        csv_a.writerow(report_list)

