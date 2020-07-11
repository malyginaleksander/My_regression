import csv
import os
import os.path
from os import path
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from datetime import datetime


def get_confirmation_number(driver, env, payload, test_name, firstname, lastname, address, zipcode_, city, accountNo, email, account_number,
                            sap_list, completed_list, error_list,backend_list,epnet_file_sent_list ):
    global emailMarketing

    WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.ID,  "confirmation")))

    confirm_text = driver.find_element_by_xpath("//*[@class='section row personal-info-section']/../div/div[2]")
    conf_text = confirm_text.text
    try:
       if payload.emailmarketing =='emailmarketing':
           driver.find_element_by_id('email_marketing_consent_span').click()
       else: pass
    except:
       pass
    try:
        driver.find_element_by_id('communication_preferences_agree').click()
    except:
        pass

    query_text = 'http://nerf.api.' + env + '.nrgpl.us/api/v1/orders/?enrollment_number=' + str(conf_text)
    response = requests.get(query_text)
    data = response.json()
    order_status = data[0]['order_status']
    while order_status == 'backend_processing':
        for i in range(1, 5):
            query_text = 'http://nerf.api.' + env + '.nrgpl.us/api/v1/orders/?enrollment_number=' + str(conf_text)
            response = requests.get(query_text)
            data = response.json()
            order_status = data[0]['order_status']
    else:
        pass
    if order_status == "completed":
        completed_list.append(conf_text)
    elif order_status == "error":
        error_list.append(conf_text)
    elif order_status == "backend_processing":
        backend_list.append(conf_text)
    elif order_status == "epnet_file_sent":
        epnet_file_sent_list.append(conf_text)
    sap_request = data[0]['order_items'][0]['href']
    response_sap = requests.get(sap_request)
    data_sap = response_sap.json()
    sap_enrollment_confirmation = data_sap['sap_enrollment_confirmation']
    sap_conf_ = str("'" + str(sap_enrollment_confirmation))
    if len(sap_enrollment_confirmation) > 0:
        sap_list.append(sap_enrollment_confirmation)
    else:
        pass
    folder_name = './outbox_folder'

    if path.exists(folder_name) == True:
       pass
    else:
       os.mkdir(folder_name)


    now = datetime.now()
    date = now.strftime("%m_%d_%Y")
    csv_filename = ("./outbox_folder/PASSED_"+test_name+"_NRG_web_"+ str(date) + "_tests_results.csv")

    data_report_list = [payload.ts, payload.SKU, payload.ChannelSlug, payload.BrandSlug, payload.PremiseType,
             payload.TermsOfServiceType, payload.ProductName, payload.ProductSlug, payload.StateSlug,
             payload.Commodity, payload.UtilitySlug, firstname, lastname, address,
              str(zipcode_), city, str("'"+str(accountNo)),
             email, payload.emailmarketing, str(date), conf_text, order_status,  sap_conf_, "Passed"]

    if os.path.isfile(csv_filename):
        f = open(csv_filename, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(data_report_list)
    else:
        f = open(csv_filename, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow(
            ['ts', 'SKU', 'ChannelSlug', 'BrandSlug', 'PremiseType',
             'TermsOfServiceTyp', 'ProductName', 'ProductSlug', 'StateSlug',
             'Commodity', 'UtilitySlug', 'first_name', 'last_name', 'ServiceAddress1',
              'zip_code', 'city', 'account_no', 'email', 'emailmarketing', 'time_for_csv_report', 'conf_number',
             'order_status', 'sap_enrollment_conf_',  "test_status"])
        csv_a.writerow(data_report_list)

    time.sleep(1)















