import csv

import time

from selenium import webdriver

driver = webdriver.Firefox()




list = [
'E1-G4L-N56 ',
'E1-JRQ-6BN ',
'E1-G6E-WRP ',
'E1-JL9-LQD ',
'E1-JQM-DBD ',
'E1-J8E-W8L ',
'E1-GDA-W8N ',
'E1-G54-WMZ ',
'E1-JW9-6NV ',
'E1-JN5-LZW ',


]


csv_filename = "./outbox_files/added_from_api_tests_results.csv"

for conf in list:
    driver.get("http://nerf.api.pt.nrgpl.us/api/v1/orders/?enrollment_number=" + str(conf))
    driver.find_element_by_xpath("//*[@id='content']/div[1]/div[4]/pre/a[2]").click()
    time.sleep(3)

    try:
        # sku = driver.find_element_by_xpath(
        # "//span[contains(text(),'sap')]/following-sibling::span[3]").text
        sap = driver.find_element_by_xpath(
        "//span[contains(text(),'sap_enrollment_confirmation')]/following-sibling::span[3]").text
        # uan_number = str("'"+str(sku))
        sap = sap.replace('"','')
    except:
        sku = 'empty'
        sap = 'empty'
    sap_enrollment_confirmation  = " couldn't find"
    # print(conf,sku[1:-1])
    print(conf,sap)

    # f = open(csv_filename, 'a', newline='')
    # csv_a = csv.writer(f)
    # csv_a.writerow(
    #     [conf, sku[1:-1]])