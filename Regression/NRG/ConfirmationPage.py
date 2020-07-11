import csv
import os
import os.path
from os import path

import pyodbc
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from Regression.ECC.TestScripts.NRG_regression.test_selectelectricplan_NRG_ import sheet_name_for_test
# from Regression.ECC.TestScripts.NRG_regression.nrg_settings import sheet_name_for_test
# from Regression.NRG_regression.test_selectelectricplan_NRG import test_name
from Regression.PageFactory.BasePage import BasePage
# from selenium.webdriver.common.keys import Keys
# from selenium import webdriver
import logging
import Regression.ConfigFiles.logger as cl
import time
import datetime
import uuid
from datetime import datetime

# z= sheet_name_for_test
# print(z)
# from Regression.generators.zip_city_generator_ import generator_zip_city_

class ConfirmationPage(BasePage):
    log = cl.genericLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver


    def get_confirmation_number(self, env, payload, firstname, lastname, address, zipcode_, city, accountNo, email,
                             account_number, phonenumber):
        sap_numbers_list = []
        global emailMarketing

        WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.ID,  "confirmation")))

        self.confirm_text = self.driver.find_element_by_xpath( "//*[@class='section row personal-info-section']/../div/div[2]")
        self.confirm_text_data = self.confirm_text.text
        try:
           if payload.emailMarketing =='emailmarketing':
               self.driver.find_element_by_id('email_marketing_consent_span').click()
           else: pass
        except:
           pass
        conf_text = self.confirm_text.text
        try:
            self.driver.find_element_by_id('communication_preferences_agree').click()
        except:
            pass

        query_text = 'http://nerf.api.'+env+'.nrgpl.us/api/v1/orders/?enrollment_number='+ str(conf_text)
        response = requests.get(query_text)
        data = response.json()
        order_status= data[0]['order_status']
        sap_request = data[0]['order_items'][0]['href']
        response_sap = requests.get(sap_request)
        data_sap = response_sap.json()
        sap_enrollment_confirmation = data_sap['sap_enrollment_confirmation']
        sap_conf_ = str("'"+str(sap_enrollment_confirmation))
        query_customer = data[0]['customer']['href']
        sap_numbers_list.append(sap_conf_)

        folder_name = './outbox_folder'

        if path.exists(folder_name) == True:
           pass
        else:
           os.mkdir(folder_name)


        now = datetime.now()
        time_for_csv_report = now.strftime("%Y-%m-%d")
        date = now.strftime("_%Y_%m_%d_")
        csv_filename = ("./outbox_folder/_NRG_web_"+ str(date) + "_tests_results.csv")
        print(csv_filename)

        if os.path.isfile(csv_filename):
            f = open(csv_filename, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(
                [payload.ts, payload.SKU, payload.ChannelSlug, payload.BrandSlug, payload.PremiseType,
                 payload.TermsOfServiceType, payload.ProductName, payload.ProductSlug, payload.StateSlug,
                 payload.Commodity, payload.UtilitySlug, firstname, lastname, address,
                 str(zipcode_), city, str("'" + str(accountNo)),
                 email, payload.emailmarketing, str(time_for_csv_report), conf_text, order_status,  "Passed"])
        else:
            f = open(csv_filename, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(
                ['ts', 'SKU', 'ChannelSlug', 'BrandSlug', 'PremiseType',
                 'TermsOfServiceTyp', 'ProductName', 'ProductSlug', 'StateSlug',
                 'Commodity', 'UtilitySlug', 'first_name', 'last_name', 'ServiceAddress1',
                 'zip_code', 'city', 'account_no',
                 'email', 'emailmarketing', 'time_for_csv_report', 'sap_enrollment_conf_','order_status',
                 "test_status"])
            csv_a.writerow(
                [payload.ts, payload.SKU, payload.ChannelSlug, payload.BrandSlug, payload.PremiseType,
                 payload.TermsOfServiceType, payload.ProductName, payload.ProductSlug, payload.StateSlug,
                 payload.Commodity, payload.UtilitySlug, firstname, lastname, address,
                 str(zipcode_), city, str("'" + str(accountNo)),
                 email, payload.emailmarketing, str(time_for_csv_report), conf_text, order_status,  "Passed"])

        time.sleep(1)

        min_sap = min(sap_numbers_list)
        max_sap = max(sap_numbers_list)
        print(min_sap)
        print(max_sap)















