from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import xlrd
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Regression.Inbound.States.Inbound_Enrollments_4brands_test.Inbound_pages_methods import login, wait_billing_page

if os.environ.get('USE_PHANTOM'):
    print("using PhantomJS")

    driver = webdriver.PhantomJS()
    driver.implicitly_wait(5)
    driver.set_window_size(1120, 550)
else:
    print("using Firefox")

workbook = xlrd.open_workbook("./State_Data.xlsx")
worksheet = workbook.sheet_by_name('NRG_regression Gas')

for current_row in range(1,worksheet.nrows):
    fname = worksheet.row(current_row)[0].value
    lname = worksheet.row(current_row)[1].value
    state = worksheet.row(current_row)[2].value
    given_utiity = worksheet.row(current_row)[3].value
    plan = worksheet.row(current_row)[4].value
    address = worksheet.row(current_row)[5].value
    city = worksheet.row(current_row)[6].value
    zipcode = worksheet.row(current_row)[7].value
    area_code = worksheet.row(current_row)[8].value
    prefix = worksheet.row(current_row)[9].value
    last = worksheet.row(current_row)[10].value
    accountNo = worksheet.row(current_row)[11].value
    service_reference = worksheet.row(current_row)[12].value
	
    driver = webdriver.Firefox()
    driver.get("http://www.pt.energypluscompany.com/myinbound/login.php")

#login
    login(driver)

    if  "Start a manual call" in driver.page_source:
        elem = driver.find_element_by_link_text("Start a manual call").click()
        elem = driver.find_element_by_id("phoneNumber").send_keys("5454588883")
        elem = driver.find_element_by_id("reason").send_keys("this is a test")
        elem = driver.find_element_by_id("brand_id")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("NRG_regression Home"):
        	    option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/form/input[3]").click() #Start Call Button
        driver.switch_to.alert.accept()

    else:
        elem = driver.find_element_by_id("brandId_2").click()
        elem = driver.find_element_by_id("btn_continue").click()

    time.sleep(2)

### Get Started:
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "caller-first-name")))
    elem = driver.find_element_by_id("caller-first-name").send_keys(fname)
    elem = driver.find_element_by_id("caller-last-name").send_keys(lname)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "state-list")))
    elem = driver.find_element_by_name("state-list")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == state:
            option.click()	

#Is Your Name on the Utility Bill?
    try:
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[6]/div[2]/div/div/label[1]/input").click()
    except:
        pass
    #What account are you calling about today? 
    try:
        elem = driver.find_element_by_class_name("commodity-choice-gas").click()
    except:
        pass	

    elem = driver.find_element_by_name("utility-list")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == given_utiity:
            option.click()
            time.sleep (1)
    elem = driver.find_element_by_class_name("account-type-residential").click()

#How do you use your natural gas?    
    elem = driver.find_element_by_class_name("account-usage-both").click()
    time.sleep(1)
    elem = driver.find_element_by_id("save-and-continue").click()
    time.sleep(2)

## Offer:
    time.sleep(2)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, ('//span[contains(text(), "1")]'))))
    # elem = driver.find_element_by_xpath(('//span[contains(text(), "The Cash Back Plan")]'))
    driver.find_element_by_id('Carbon Offset Plan').click()
    elem = driver.find_element_by_name("btn_continue").click()
    time.sleep(2)

## Customer Info:

    elem = driver.find_element_by_name('First Name').send_keys(fname)
    elem = driver.find_element_by_name("Last Name").send_keys(lname)
    elem = driver.find_element_by_name("Service Address 1").send_keys(address)
    elem = driver.find_element_by_name("City").send_keys(city)
    elem = driver.find_element_by_name("Zip").send_keys(int(zipcode))
    elem = driver.find_element_by_name("Phone Area Code").send_keys(int(area_code))
    elem = driver.find_element_by_name("Phone Prefix").send_keys(int(prefix))
    elem = driver.find_element_by_name("Phone Last Digits").clear()
    elem = driver.find_element_by_name("Phone Last Digits").send_keys(int(last))
    #elem = driver.find_element_by_class_name("copy-to-billing-yes").click()
    elem = driver.find_element_by_class_name("uan").send_keys(int(accountNo))
    #elem = driver.find_element_by_class_name("extra-uan").send_keys(int(service_reference))
    #todo return fail?
    try:
        elem - driver.find_element_by_class_name('point-id').send_keys(str(accountNo))
        elem = driver.find_element_by_class_name("check-account-number").click()

    except:
        pass
    # elem - driver.find_element_by_class_name('point-id').send_keys(str(accountNo))
    time.sleep(2)
    try:
        elem = driver.find_element_by_class_name("extra-uan").send_keys(int(service_reference))
        elem = driver.find_element_by_class_name("check-extra-account-number").click()
    except:
        pass
    elem = driver.find_element_by_class_name("check-account-number").click()
    # elem = driver.find_element_by_class_name("check-bill-account-number").click()

    time.sleep(2)

    # try:
    #     # elem = driver.find_element_by_name("Customer Key").send_keys("test")
    #     # elem = driver.find_element_by_class_name("extra-uan").send_keys(service_reference)
    #     # elem = driver.find_element_by_class_name("check-extra-account-number").click()
    #     time.sleep(2)
    # except:
    #     pass

    elem = driver.find_element_by_id("btn_continue").click()	
    time.sleep(2)

## Billing Info:
    wait_billing_page(driver)
    elem = driver.find_element_by_name(" Billing Address").send_keys(address)
    elem = driver.find_element_by_name(" City").send_keys(city)
    elem = driver.find_element_by_class_name("state-dropdown")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == state:
            option.click()
    elem = driver.find_element_by_name(" Zip Code").send_keys(int(zipcode))
    elem = driver.find_element_by_name(" Phone Area Code").send_keys(int(area_code))
    elem = driver.find_element_by_name(" Phone Prefix").send_keys(int(prefix))
    elem = driver.find_element_by_name(" Phone Last Digits").send_keys(int(last))
    elem = driver.find_element_by_class_name("email-no").click()
    elem = driver.find_element_by_class_name("email-no-no").click()
    elem = driver.find_element_by_id("btn_continue").click()
    time.sleep(1)	

## Summary:
    WebDriverWait(driver, 300).until(EC.element_to_be_clickable((By.ID, "to-disclosures")))
    elem = driver.find_element_by_id("to-disclosures").click()
    time.sleep(1)

## Disclosure:
    elem = driver.find_element_by_id("toggle_1_no").click()
    elem = driver.find_element_by_id("toggle_2_no").click()

    if  driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=IL":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MD":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MA":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("toggle_7_no").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_8_no").click()
        elem = driver.find_element_by_id("toggle_9_yes").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=NJ":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=OH":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("toggle_7_yes").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=PA":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_7_no").click()
        elem = driver.find_element_by_id("toggle_8_yes").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=DC":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("toggle_7_yes").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=NY":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("toggle_7_yes").click()        
		
## Grab Conformation Code
    time.sleep(2)
    elem = driver.find_element_by_id("confcode")
    confcode = elem.text
    print("Passed - NRG_regression Inbound Electric, Conformation =  " + confcode + ' for ' + state + ' - ' + given_utiity)
    f = open("./results.txt", 'a')
    f.write( confcode +" " + "NRG_regression Gas" + "\n")
## Submit:	
    try:
        elem = driver.find_element_by_id("submit_tpv_button").click()
    except:
        elem = driver.find_element_by_id("submit_enroll").click()

## Close Session:
    driver.close()