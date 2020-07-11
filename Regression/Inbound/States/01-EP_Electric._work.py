from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
import time
import xlrd
import os
from Inbound.States.Inbound_Enrollments_4brands_test.Inbound_pages_methods import login
from selenium.webdriver.support.wait import WebDriverWait

if os.environ.get('USE_PHANTOM'):
    print("using PhantomJS")

    driver = webdriver.PhantomJS()
    driver.implicitly_wait(5)
    driver.set_window_size(1120, 550)
else:
    print("using Firefox")


workbook = xlrd.open_workbook("./State_Data_base.xlsx")
worksheet = workbook.sheet_by_name('EP Electric')

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
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "caller-first-name")))
    elem = driver.find_element_by_id("caller-first-name").send_keys(fname)
    elem = driver.find_element_by_id("caller-last-name").send_keys(lname)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, ('state-list'))))
    elem = driver.find_element_by_name("state-list")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == state:
            option.click()

    #For Massachusetts choice:
    current_state = str(state)
    if current_state == 'Massachusetts':
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[6]/div[3]/select').click()
        elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[6]/div[3]/select')
        for option in elem.find_elements_by_tag_name('option'):
             if option.text == "Eversource Energy (Western Massachusetts)":
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

## Offer:

    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, ('//span[contains(text(), "1")]'))))

# 1    try:
#         elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/p[1]/select').click()
#         for option in elem.find_elements_by_tag_name('option'):
#             if option.text == ("Cash Back"):
#                 option.click()
#         elem = driver.find_element_by_class_name("partners")
#         for option in elem.find_elements_by_tag_name('option'):
#             if option.text == 'Brand Residential - IL - BRC':
#                 option.click()
#         elem = driver.find_element_by_class_name("campaigns")
#         for option in elem.find_elements_by_tag_name('option'):
#             if option.text == '0000 - Unknown':
#                 option.click()
#         elem = driver.find_element_by_class_name("promos")
#         for option in elem.find_elements_by_tag_name('option'):
#             if option.text == '015 - $25 bonus / 3%':
#                 option.click()
#     except:
#         pass
    elem = driver.find_element_by_id("green_option_no").click()
    #For Maryland or 'Massachusetts'
    current_state = str(state)
    if current_state == 'Maryland' or 'Massachusetts' or 'New Jersey' or 'Ohio':
        try:
            driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/p/button[1]').click()
        except:
            pass
        elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/p[1]/select').click()
        elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/p[1]/select')
        time.sleep(1)
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == "Cash Back":
                option.click()
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/p[2]/select').click()
        # act = ActionChains(driver)
        elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/p[2]/select')
        driver.find_element_by_xpath('//option[contains(text(), "Brand Residential")]').click()



        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[2]/p[1]/select').click()
        elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[2]/p[1]/select')
        driver.find_element_by_xpath('//option[contains(text(), "Fixed")]').click()
        driver.find_element_by_xpath('//option[contains(@class,"promo")]').click()
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[2]/p[2]/select').click()
        elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[3]/div/div/div[2]/div[2]/p[2]/select')
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == "015 - Residential (3%/$25)":
                option.click()


    time.sleep(2)
    elem = driver.find_element_by_id("btn_continue").click()



## Customer Info:
    WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.ID, "caller-first-name"))).click()

    elem = driver.find_element_by_name('First Name').send_keys(fname)
    elem = driver.find_element_by_name("Last Name").send_keys(lname)
    elem = driver.find_element_by_name("Service Address 1").send_keys(address)
    elem = driver.find_element_by_name("City").send_keys(city)
    elem = driver.find_element_by_name("Zip").send_keys(int(zipcode))
    elem = driver.find_element_by_name("Phone Area Code").send_keys(int(area_code))
    elem = driver.find_element_by_name("Phone Prefix").send_keys(int(prefix))
    elem = driver.find_element_by_name("Phone Last Digits").clear()
    elem = driver.find_element_by_name("Phone Last Digits").send_keys(int(last))
    elem = driver.find_element_by_class_name("copy-to-billing-yes").click()
    time.sleep(2)
    elem = driver.find_element_by_class_name("uan").send_keys(str(accountNo))
    elem = driver.find_element_by_class_name("check-account-number").click()
    time.sleep(2)


    #Eversource Energy (Western Massachusetts) Account Number
    # if  current_state == 'Massachusetts':
    try:
        elem = driver.find_element_by_name("Customer Key").send_keys("test")
        elem = driver.find_element_by_name("Customer Key").send_keys("test")
        driver.find_element_by_xpath('//input[contains(@id,"service-extra")]').send_keys(int(service_reference))
        elem = driver.find_element_by_class_name("check-extra-account-number").click()
        time.sleep(2)
    except:
        pass

    #Todo - finish wait
    time.sleep(6)
    elem = driver.find_element_by_id("btn_continue").click()

## Billing Info:
    time.sleep(5)

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
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_yes").click()
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
    time.sleep(2)
    print("Passed - EP Inbound Electric, Conformation =  " + confcode + ' for ' + state + ' - ' + given_utiity)

## Submit:
    try:
        elem = driver.find_element_by_id("submit_tpv_button").click()
    except:
        elem = driver.find_element_by_id("submit_enroll").click()
## Close Session:
    driver.close()