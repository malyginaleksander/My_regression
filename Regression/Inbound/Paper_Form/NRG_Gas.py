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

workbook = xlrd.open_workbook("./Form_data.xlsx")
worksheet = workbook.sheet_by_name('NRG_regression GAS')

for current_row in range(1,worksheet.nrows):
    brand = worksheet.row(current_row)[0].value
    first_name = worksheet.row(current_row)[1].value
    last_name = worksheet.row(current_row)[2].value
    address = worksheet.row(current_row)[3].value
    city = worksheet.row(current_row)[4].value
    state = worksheet.row(current_row)[5].value
    zipcode = worksheet.row(current_row)[6].value
    area_code = worksheet.row(current_row)[7].value
    prefix = worksheet.row(current_row)[8].value
    last = worksheet.row(current_row)[9].value
    account_type = worksheet.row(current_row)[10].value
    email = worksheet.row(current_row)[11].value
    given_utiity = worksheet.row(current_row)[12].value
    account_number = worksheet.row(current_row)[15].value
    service_ref = worksheet.row(current_row)[16].value
    partner = worksheet.row(current_row)[17].value
    campaign = worksheet.row(current_row)[18].value
    promo = worksheet.row(current_row)[19].value

    driver = webdriver.Firefox()
    driver.get("http://www.pt.energypluscompany.com/myinbound/login.php")

#login
    elem = driver.find_element_by_name("email").send_keys("mpeters@energypluscompany.com")
    elem = driver.find_element_by_name("password").send_keys("energy")
    elem = driver.find_element_by_id("button").click()
    time.sleep(2)

    driver.get("http://www.pt.energypluscompany.com/myinbound/paper.php")
    time.sleep(2)

    elem = driver.find_element_by_id(brand).click()
    time.sleep(3)

#Customer Information
    elem = driver.find_element_by_name("customer_first_name").send_keys(first_name)
    elem = driver.find_element_by_name("customer_last_name").send_keys(last_name)
    elem = driver.find_element_by_name("customer_address1").send_keys(address)
    elem = driver.find_element_by_name("customer_city").send_keys(city)
    elem = driver.find_element_by_name("customer_state")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == state:
            option.click()
    elem = driver.find_element_by_name("customer_zip5").send_keys(zipcode)
    elem = driver.find_element_by_name("customer_area_code").send_keys(area_code)
    elem = driver.find_element_by_name("customer_prefix").send_keys(prefix)
    elem = driver.find_element_by_name("customer_line_number").clear()
    elem = driver.find_element_by_name("customer_line_number").send_keys(last)
    elem = driver.find_element_by_name("account_type")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == account_type:
            option.click()
    if 	driver.find_element_by_name("business_name").is_displayed():
        time.sleep(1)
        elem = driver.find_element_by_name("business_name").send_keys(business_name)
        time.sleep(1)
    
#Billing Information
    elem = driver.find_element_by_name("copyinfo").click()
    elem = driver.find_element_by_name("email").send_keys(email)
    if 	driver.find_element_by_id("egr_commodity_gas").is_displayed():
        elem = driver.find_element_by_id("egr_commodity_gas").click()

#Electric
    elem = driver.find_element_by_name("gas_utility")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == given_utiity:
            option.click()
    elem = driver.find_element_by_name("gas_account_number").send_keys(account_number)

#Order Information
    elem = driver.find_element_by_name("offer_types_gas")
    for option in elem.find_elements_by_tag_name('option'):
    	if option.text == ("Offer Code"):
    		option.click()
    elem = driver.find_element_by_name("partner_code_gas").send_keys(partner)
    elem = driver.find_element_by_name("campaign_code_gas").send_keys(campaign)
    if driver.find_element_by_name("promo_code_gas").is_displayed():
        elem = driver.find_element_by_name("promo_code_gas").send_keys(promo)
    time.sleep(4)

#Vendor ID
    elem = driver.find_element_by_name("vendor_id")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == ("EPIB"):
            option.click()

# Grab Conformation Code
    elem = driver.find_element_by_name("confCode")
    confCode = elem.text
    print("Passed - NRG_regression Paper - Gas, " + confCode +' for ' + state +' - ' + given_utiity)

    elem = driver.find_element_by_name("submit").click()

    driver.close()