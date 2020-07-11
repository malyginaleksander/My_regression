from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os

if os.environ.get('USE_PHANTOM'):
    print("using PhantomJS")

    driver = webdriver.PhantomJS()
    driver.implicitly_wait(5)
    driver.set_window_size(1120, 550)
else:
    print("using Firefox")

workbook = xlrd.open_workbook("./NRG_Data.xlsx")
worksheet = workbook.sheet_by_name('gas')

for current_row in range(3,worksheet.nrows):
    url = worksheet.row(current_row)[4].value
    first_name = worksheet.row(current_row)[5].value
    last_name = worksheet.row(current_row)[6].value
    email_addr = worksheet.row(current_row)[9].value
    confirm_email_addr = worksheet.row(current_row)[10].value
    Service_Address1 = worksheet.row(current_row)[11].value
    city = worksheet.row(current_row)[12].value
    zipcode = worksheet.row(current_row)[13].value
    Service_phone_number = worksheet.row(current_row)[14].value
    accountNo = worksheet.row(current_row)[15].value
    gas_account = worksheet.row(current_row)[16].value    

    driver = webdriver.Firefox()    
    driver.get(url)
    time.sleep(2)

## Personal Information
    elem = driver.find_element_by_id("id_first_name").send_keys(first_name)
    elem = driver.find_element_by_id("id_last_name").send_keys(last_name)
    elem = driver.find_element_by_id("id_email").send_keys(email_addr)
    elem = driver.find_element_by_id("id_ver_email").send_keys(confirm_email_addr)
    elem = driver.find_element_by_id("id_phone").send_keys(Service_phone_number)
    elem = driver.find_element_by_id("id_service_address_1").send_keys(Service_Address1)
    elem = driver.find_element_by_id("id_service_address_city").send_keys(city)
    elem = driver.find_element_by_id("id_service_address_zip").send_keys(zipcode)
    elem = driver.find_element_by_id("id_electric-uan").send_keys(accountNo)
    try:
        elem = driver.find_element_by_id("id_electric-billing_uan").send_keys(accountNo)
    except:
        pass    
    elem = driver.find_element_by_id("id_gas-uan").send_keys(gas_account)
    time.sleep(2)
    elem = driver.find_element_by_id("continue-submit").click()
    time.sleep(4)

## Verification
    elem = driver.find_element_by_class_name("tos-section").send_keys(Keys.CONTROL, Keys.ARROW_DOWN);
    elem = driver.find_element_by_class_name("tos-section").send_keys(Keys.CONTROL, Keys.ARROW_DOWN);
    elem = driver.find_element_by_class_name("tos-section").send_keys(Keys.CONTROL, Keys.ARROW_DOWN);
    elem = driver.find_element_by_class_name("tos-section").send_keys(Keys.CONTROL, Keys.ARROW_DOWN);
    elem = driver.find_element_by_class_name("tos-section").send_keys(Keys.CONTROL, Keys.ARROW_DOWN);        
    elem = driver.find_element_by_id("id_order_authorization").click()

    if driver.find_element_by_id("id_affiliate_consent").is_displayed():
        driver.find_element_by_id("id_affiliate_consent").click()

    elem = driver.find_element_by_id("agree").click()

## Grab Conformation Code
    time.sleep(2)
    elem = driver.find_element_by_id("confirmation")
    confirmation = elem.text
    print("Passed - NRG_regression WEB GAS, Conformation =  " +confirmation + ' for ' +last_name)

## Close Session:
    driver.close()    