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

workbook = xlrd.open_workbook("./Production_data.xlsx")
worksheet = workbook.sheet_by_name('IB-EP')

for current_row in range(1,worksheet.nrows):
    fname = worksheet.row(current_row)[0].value
    lname = worksheet.row(current_row)[1].value
    state = worksheet.row(current_row)[2].value
    commodity = worksheet.row(current_row)[3].value
    given_utiity = worksheet.row(current_row)[4].value
    partner = worksheet.row(current_row)[5].value
    campaign = worksheet.row(current_row)[6].value
    promo = worksheet.row(current_row)[7].value
    address = worksheet.row(current_row)[8].value
    city = worksheet.row(current_row)[9].value
    zipcode = worksheet.row(current_row)[10].value
    area_code = worksheet.row(current_row)[11].value
    prefix = worksheet.row(current_row)[12].value
    last = worksheet.row(current_row)[13].value
    accountNo = worksheet.row(current_row)[14].value
    service_reference = worksheet.row(current_row)[15].value
	
    driver = webdriver.Firefox()
    driver.get("http://www.energypluscompany.com/myinbound/login.php")

#login
    elem = driver.find_element_by_name("email").send_keys("mpeters@energypluscompany.com")
    elem = driver.find_element_by_name("password").send_keys("energy")
    elem = driver.find_element_by_id("button").click()

    if  "Start a manual call" in driver.page_source:
        elem = driver.find_element_by_link_text("Start a manual call").click()
        elem = driver.find_element_by_id("phoneNumber").send_keys("5454588883")
        elem = driver.find_element_by_id("reason").send_keys("this is a test")
        elem = driver.find_element_by_id("brand_id")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("Energy Plus"):
        	    option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/form/input[3]").click() #Start Call Button
        driver.switch_to.alert.accept()

    else:
        elem = driver.find_element_by_id("brandId_1").click()
        elem = driver.find_element_by_id("btn_continue").click()

    time.sleep(2)

### Get Started:
    elem = driver.find_element_by_id("caller-first-name").send_keys(fname)
    elem = driver.find_element_by_id("caller-last-name").send_keys(lname)
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
        elem = driver.find_element_by_class_name("commodity-choice-electric").click()
    except:
        pass	

#Who is the provider for your electric account?
    try:
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[6]/div[3]/div[1]/label/input").click()        	
    except:
        pass       

    elem = driver.find_element_by_name("utility-list")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == given_utiity:
            option.click()

#Is this electric account a residential or business address? 
    elem = driver.find_element_by_class_name("account-type-residential").click()
    
    elem = driver.find_element_by_id("save-and-continue").click()
    time.sleep(4)
		
## Offer:
    if driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div/div/p/button[2]").is_displayed():
    	elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div/div/p/button[2]").click()

    elem = driver.find_element_by_class_name("categories")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == ("Cash Back"):
            option.click()
    elem = driver.find_element_by_class_name("partners")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == partner:
            option.click()
    elem = driver.find_element_by_class_name("campaigns")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == campaign:
            option.click()
    elem = driver.find_element_by_class_name("promos")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == promo:
            option.click()
    elem = driver.find_element_by_id("green_option_no").click()
    elem = driver.find_element_by_id("btn_continue").click()
    time.sleep(2)

## Customer Info:
    elem = driver.find_element_by_name('First Name').send_keys(fname)
    elem = driver.find_element_by_name("Last Name").send_keys(lname)
    elem = driver.find_element_by_name("Service Address 1").send_keys(address)
    elem = driver.find_element_by_name("City").send_keys(city)
    elem = driver.find_element_by_name("Zip").send_keys(zipcode)
    elem = driver.find_element_by_name("Phone Area Code").send_keys(area_code)
    elem = driver.find_element_by_name("Phone Prefix").send_keys(prefix)
    elem = driver.find_element_by_name("Phone Last Digits").clear()
    elem = driver.find_element_by_name("Phone Last Digits").send_keys(last)
    #elem = driver.find_element_by_class_name("copy-to-billing-yes").click()
    elem = driver.find_element_by_class_name("uan").send_keys(accountNo)
    elem = driver.find_element_by_class_name("check-account-number").click()
    time.sleep(2)

    try:
        elem = driver.find_element_by_name("Customer Key").send_keys("test")
        elem = driver.find_element_by_class_name("extra-uan").send_keys(service_reference)
        elem = driver.find_element_by_class_name("check-extra-account-number").click()
        time.sleep(2)
    except:
        pass    

    elem = driver.find_element_by_id("btn_continue").click()	
    time.sleep(2)

## Billing Info:
    elem = driver.find_element_by_name(" Billing Address").send_keys(address)
    elem = driver.find_element_by_name(" City").send_keys(city)
    elem = driver.find_element_by_class_name("state-dropdown")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == state:
            option.click()
    elem = driver.find_element_by_name(" Zip Code").send_keys(zipcode)
    elem = driver.find_element_by_name(" Phone Area Code").send_keys(area_code)
    elem = driver.find_element_by_name(" Phone Prefix").send_keys(prefix)
    elem = driver.find_element_by_name(" Phone Last Digits").send_keys(last)
    elem = driver.find_element_by_class_name("email-no").click()
    elem = driver.find_element_by_class_name("email-no-no").click()
    elem = driver.find_element_by_id("btn_continue").click()
    time.sleep(1)	

## Summary:
    elem = driver.find_element_by_id("to-disclosures").click()
    time.sleep(1)

## Disclosure:
    elem = driver.find_element_by_id("toggle_1_no").click()
    elem = driver.find_element_by_id("toggle_2_no").click()

    if  driver.current_url == "http://www.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=IL":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_yes").click()
    if driver.current_url == "http://www.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MD":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
    if driver.current_url == "http://www.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MA":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_yes").click()
        elem = driver.find_element_by_id("toggle_8_no").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_9_no").click()
        elem = driver.find_element_by_id("toggle_10_yes").click()
    if driver.current_url == "http://www.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=NJ":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
    if driver.current_url == "http://www.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=OH":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("toggle_7_yes").click()
    if driver.current_url == "http://www.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=PA":
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
    print("Passed - EP Inbound Electric Production, Confirmation =  " + confcode + ' for ' + state + ' - ' + given_utiity)

## Submit:	
    elem = driver.find_element_by_id("submit_enroll").click()	

## Close Session:
    driver.close()