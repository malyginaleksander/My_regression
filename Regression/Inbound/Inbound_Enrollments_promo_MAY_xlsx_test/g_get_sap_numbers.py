import csv
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


driver = webdriver.Firefox()



directory_for_base_file = "./f_query_result/"
files_dir = os.listdir(directory_for_base_file)
input_files_list = []
for name in files_dir:
    input_files_list.append(name)

for file in input_files_list:
    input_file_dict  =  csv.DictReader(open(str(directory_for_base_file)+str(file)))

sap_enrollment_confirmation_list = []
enrollment_number_list= []
sap_enrollment_confirmation_list_= []
sku_list = []
oder_status_list= []
for row in input_file_dict:
# for row in input_file_epenet:

        dict_zip = row
        enrollment_number = dict_zip.get('enrollment_number','')
        sap_enrollment_confirmation = dict_zip.get('sap_enrollment_confirmation','')
        sku = dict_zip.get('sku','')
        order_status = dict_zip.get('order_status','')
        enrollment_number_list.append(enrollment_number)
        sap_enrollment_confirmation_list.append(sap_enrollment_confirmation)
        sku_list.append(sku)
        oder_status_list.append(order_status)
report = ('./g_response_file/report_with_address.csv')

for elem, sap_enrollment_confirmation, sku, order_status  in zip(enrollment_number_list, sap_enrollment_confirmation_list, sku_list, oder_status_list):

    # if sap_enrollment_confirmation in sap_enrollment_confirmation_list_:
    #     pass
    # else:
    #     sap_enrollment_confirmation_list_.append(sap_enrollment_confirmation)

        driver.get("http://nerf.api.pt.nrgpl.us/api/v1/orders/?enrollment_number=" + str(elem))
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'List all Orders, or create a new order')]")))
        # time.sleep(5)

        driver.find_element_by_xpath("//*[@id='content']/div[1]/div[4]/pre/a[1]").click()

        time.sleep(2)
        # address = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[1]/div[4]/pre/span[43]').text()
        address_ = driver.find_element_by_xpath(
            "//span[contains(text(),'service_address_1')]/following-sibling::span[3]").text
        service_address_zip = driver.find_element_by_xpath(
            "//span[contains(text(),'service_address_zip')]/following-sibling::span[3]").text
        service_address_state = driver.find_element_by_xpath(
            "//span[contains(text(),'service_address_state')]/following-sibling::span[3]").text
        allow_email_marketing = driver.find_element_by_xpath(
            "//span[contains(text(),'allow_email_marketing')]/following-sibling::span[3]").text
        print((str(address_)[1:-1]), str(elem),  str(sap_enrollment_confirmation), str(sku), (str("'")+ str(service_address_zip[1:-1])),
                            str(service_address_state[1:-1]), allow_email_marketing, order_status)
        # print(str(elem) + ' ' + str(address_) + " "+ str(sap_enrollment_confirmation) + " "+ str(sku), order_status)



        if os.path.isfile(report):
            f = open(report, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow([(str(address_)[1:-1]), str(elem),  str(sap_enrollment_confirmation), str(sku), (str("'")+ str(service_address_zip[1:-1])),
                            str(service_address_state[1:-1]), allow_email_marketing, order_status])
        else:
            f = open(report, 'a', newline='')
            csv_a = csv.writer(f)
            csv_a.writerow(
                ['address', 'conf_number', 'idoc', 'sku', 'service_address_zip',
                            'service_address_state', 'allow_email_marketing','order_status' ])
            csv_a.writerow([(str(address_)[1:-1]), str(elem),  str(sap_enrollment_confirmation), str(sku), (str("'")+ str(service_address_zip[1:-1])),
                            str(service_address_state[1:-1]), allow_email_marketing, order_status])


driver.close()
# driver.quit()

