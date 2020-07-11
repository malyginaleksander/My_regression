from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import xlrd
import os
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_pages_methods import login

if os.environ.get('USE_PHANTOM'):
    print("using PhantomJS")

    driver = webdriver.PhantomJS()
    driver.implicitly_wait(5)
    driver.set_window_size(1120, 550)
else:
    print("using Firefox")

workbook = xlrd.open_workbook("./State_data.xlsx")
worksheet = workbook.sheet_by_name('EP Electric GAS')

for current_row in range(1,worksheet.nrows):
    fname = worksheet.row(current_row)[0].value
    lname = worksheet.row(current_row)[1].value
    state = worksheet.row(current_row)[2].value
    given_utiity = worksheet.row(current_row)[3].value
    utility2 = worksheet.row(current_row)[4].value
    partner = worksheet.row(current_row)[5].value
    campaign = worksheet.row(current_row)[6].value
    promo = worksheet.row(current_row)[7].value
    address = worksheet.row(current_row)[8].value
    city = worksheet.row(current_row)[9].value
    zipcode = worksheet.row(current_row)[10].value
    area_code = worksheet.row(current_row)[11].value
    prefix = worksheet.row(current_row)[12].value
    last = worksheet.row(current_row)[13].value
    accountNo_gas = worksheet.row(current_row)[14].value
    accountNo_el = worksheet.row(current_row)[15].value
    campaign_el = worksheet.row(current_row)[16].value
    promo_el = worksheet.row(current_row)[17].value

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
    time.sleep(1)
    elem = driver.find_element_by_name("state-list")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == state:
            option.click()
    time.sleep(1)

#Is Your Name on the Utility Bill?
    try:
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[6]/div[2]/div/div/label[1]/input").click()
    except:
        pass

#What account are you calling about today? Electric
    try:
        elem = driver.find_element_by_class_name("commodity-choice-electric").click()
    except:
        pass 
    
    elem = driver.find_element_by_name("utility-list")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == given_utiity:
            option.click()

#Is this electric account a residential or business address? 
    elem = driver.find_element_by_class_name("account-type-residential").click()

#add Gas Account
    elem = driver.find_element_by_id("add-account-button").click()
    time.sleep(1)
    elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[1]/select")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == state:
            option.click()
    time.sleep(1)

#What account are you calling about today? Gas
    try:
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[2]/div[2]/label/input").click()
    except:
        pass	

    elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[3]/select")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == utility2:
            option.click()

#Is this electric account a residential or business address? 
    elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[4]/label[1]/input").click()
    time.sleep(1)
#How do you use your natural gas?    
    elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[5]/div[3]/label/input").click()
    time.sleep(1)
    elem = driver.find_element_by_id("save-and-continue").click()
    time.sleep(2)

## Offer: Electric

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, ('//span[contains(text(), "1")]'))))

#Offer - PSE_Electric "Fixed" choise
    try:
        elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div[2]/div/p/button[1]').click()
    except:
        elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div[1]/div/p/button[1]').click()

# IF Electric choise on the TOP:
    try:
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[1]/p[1]/select")
        for option in elem.find_element_by_tag_name('option'):
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
            if option.text == campaign_el:
                option.click()
        elem = driver.find_element_by_class_name("promos")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == promo:
                option.click()
            if option.text == promo_el:
                option.click()
        time.sleep(2)
    except:
        pass

#IF GAS choise on the TOP:
    #for gas choise
    try:
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[1]/p[1]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("Cash Back"):
                option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[1]/p[2]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == partner:
                option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[2]/p[1]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == campaign_el:
                option.click()
            if option.text == campaign:
                option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[2]/p[2]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == promo_el:
                option.click()
            if option.text == promo:
                option.click()

    #for electric choise
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/p[1]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("Cash Back"):
                option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/p[2]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == partner:
                option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/p[1]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == campaign:
                option.click()
            if option.text == campaign_el:
                option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/p[2]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == promo:
                option.click()
            if option.text == promo_el:
                option.click()
    except:
        pass

    try:
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[1]/p[1]/select")
    #for El choise:
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("Cash Back"):
                option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[1]/p[2]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == partner:
                option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[2]/p[1]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == campaign_el:
                option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[3]/div[1]/div/div[2]/div[2]/p[2]/select")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == promo_el:
                option.click()
    except:
        pass


    time.sleep(2)
    elem = driver.find_element_by_id("green_option_no").click()
    elem = driver.find_element_by_id("btn_continue").click()
    time.sleep(4)

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
    elem = driver.find_element_by_name("Gas PoD ID").send_keys(accountNo_gas)
    time.sleep(2)

    elem = driver.find_element_by_class_name("same-as-first").click()
    elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[4]/input[1]").click()
    elem = driver.find_element_by_name("Electric PoD ID").send_keys(accountNo_el)
    elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/button").click()
    driver.find_element_by_xpath('//button[contains(text(), "Check Electric PoD ID")]').click()
    driver.find_element_by_xpath('//button[contains(text(), "Check Gas PoD ID")]').click()


    time.sleep(2)
    elem = driver.find_element_by_id("btn_continue").click()	
    time.sleep(2)

## Billing Info:
    WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, '//label[contains(@class,"billing-address")]')))

    elem = driver.find_element_by_name(" Billing Address").send_keys(address)
    elem = driver.find_element_by_name(" City").send_keys(city)
    elem = driver.find_element_by_class_name("state-dropdown")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == state:
            option.click()
    elem = driver.find_element_by_name(" Zip Code").send_keys(zipcode)
    elem = driver.find_element_by_name(" Phone Area Code").send_keys(int(area_code))
    elem = driver.find_element_by_name(" Phone Prefix").send_keys(int(prefix))
    elem = driver.find_element_by_name(" Phone Last Digits").send_keys(int(last))
    elem = driver.find_element_by_class_name("email-no").click()
    elem = driver.find_element_by_class_name("email-no-no").click()
    time.sleep(1)
    elem = driver.find_element_by_class_name("same-as-first").click()
    elem = driver.find_element_by_class_name("same-emailchoice-as-first").click()
    elem = driver.find_element_by_id("btn_continue").click()
    time.sleep(2)

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
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_yes").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MD":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MA":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_yes").click()
        elem = driver.find_element_by_id("toggle_8_no").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_9_no").click()
        elem = driver.find_element_by_id("toggle_10_yes").click()
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
        elem = driver.find_element_by_id("toggle_5_yes").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("toggle_7_yes").click()

## Grab Conformation Code
    WebDriverWait(driver, 200).until(expected_conditions.visibility_of_element_located((By.ID, 'confcode')))
    elem = driver.find_element_by_id("confcode")
    confcode = elem.text
    print("Passed - EP Inbound Electric & Gas, Conformation =  " + confcode + ' for ' + state + ' - ' + given_utiity)
    f = open("./results.txt", 'a')
    f.write( confcode +" " + "EP Electric GAS" + "\n")
## Submit:	
    elem = driver.find_element_by_id("submit_enroll").click()	

## Close Session:
    driver.close()