import csv
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


driver = webdriver.Firefox()


list = [	'E1-GVB-KZP', 	'E1-JBK-9XR', 	'E1-GXY-WE6', 	'E1-GEY-PBQ', 	'E1-G4L-E6D', 	'E1-J8E-4KM', 	'E1-G6E-Y5N',
            'E1-GXY-W76', 	'E1-JQM-NKX', 	'E1-J8E-46M', 	'E1-GDA-KV9', 	'E1-GEY-P5Q',
]
report = ('./g_response_file/report_with_address_checking.csv')

for elem in list:

    driver.get("http://nerf.api.pt.nrgpl.us/api/v1/orders/?enrollment_number=" + str(elem))
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'List all Orders, or create a new order')]")))
    # time.sleep(5)

    driver.find_element_by_xpath("//*[@id='content']/div[1]/div[4]/pre/a[1]").click()

    # time.sleep(2)
    try:
        address_ = driver.find_element_by_xpath("//span[contains(text(),'service_address_1')]/following-sibling::span[3]").text
        first_name= driver.find_element_by_xpath("//span[contains(text(),'first_name')]/following-sibling::span[3]").text
        last_name= driver.find_element_by_xpath("//span[contains(text(),'last_name')]/following-sibling::span[3]").text
        driver.get("http://nerf.api.pt.nrgpl.us/api/v1/orders/?enrollment_number=" + str(elem))
        driver.find_element_by_xpath("//*[@id='content']/div[1]/div[4]/pre/a[2]").click()
        account_no =driver.find_element_by_xpath("//span[contains(text(),'uan')]/following-sibling::span[3]").text
        print(str(elem),str(address_), str("'"+ str(account_no)),str(first_name), last_name)
        f = open(report, 'a', newline='')
        csv_a = csv.writer(f)
        csv_a.writerow([str(elem), str(address_), str("'" + str(account_no)), str(first_name), last_name])
    except:
        print(elem, "FAILED")
        f = open(report, 'a', newline='')
        csv_a = csv.writer(f)








driver.close()
# driver.quit()

