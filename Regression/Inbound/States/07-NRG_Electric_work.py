import pytest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import xlrd
import os
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

@pytest.fixture(scope='session')
def driver(request):
    print('driver_setup()')
    if os.environ.get('USE_PHANTOM'):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(6000, 2000)
    else:
        print("making Chrome driver")
        _driver = webdriver.Firefox()

    _driver.get_screenshot_as_file('..\TestScripts\screenshots')
    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            _driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver

workbook = xlrd.open_workbook("./State_Data_base.xlsx")
worksheet = workbook.sheet_by_name('NRG_regression Electric')

for current_row in range(1,worksheet.nrows):
    fname = worksheet.row(current_row)[0].value
    lname = worksheet.row(current_row)[1].value
    state = worksheet.row(current_row)[2].value
    given_utiity = worksheet.row(current_row)[4].value
    plan = worksheet.row(current_row)[5].value
    address = worksheet.row(current_row)[6].value
    city = worksheet.row(current_row)[7].value
    zipcode = worksheet.row(current_row)[8].value
    area_code = worksheet.row(current_row)[9].value
    prefix = worksheet.row(current_row)[10].value
    last = worksheet.row(current_row)[11].value
    accountNo = worksheet.row(current_row)[12].value
    service_reference = worksheet.row(current_row)[13].value

    driver = webdriver.Firefox()
    driver.get("http://www.pt.energypluscompany.com/myinbound/login.php")

#login
    driver.get("http://www.pt.energypluscompany.com/myinbound/login.php")
    elem = driver.find_element_by_name("email").send_keys("gurjeet.saini@nrg.com")
    elem = driver.find_element_by_name("password").send_keys("energy")
    elem = driver.find_element_by_id("button").click()

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


### Get Started:
    WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.ID, "caller-first-name")))
    elem = driver.find_element_by_id("caller-first-name").send_keys(fname)
    elem = driver.find_element_by_id("caller-last-name").send_keys(lname)
    time.sleep(1)
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
    try:
        elem = driver.find_element_by_class_name("account-type-residential").click()
    except:
        driver.find_element(By.CSS_SELECTOR, ".state-list > option:nth-child(7)").click()
        driver.find_element(By.NAME, "utility-list").click()
        dropdown = driver.find_element(By.NAME, "utility-list")
        dropdown.find_element(By.XPATH, "//option[. = 'Eversource (Western Massachusetts)']").click()
        # driver.find_element(By.CLASS_NAME, "account-type-residential ng-invalid ng-invalid-required ng-touched").click()
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[6]/div[4]/label[1]/input').click()

    elem = driver.find_element_by_id("save-and-continue").click()

## Offer:
    WebDriverWait(driver, 200).until(EC.visibility_of_all_elements_located((By.ID, "category-*Primary Plans")))
    elem = driver.find_element_by_id(plan).click()
    elem = driver.find_element_by_id
    elem = driver.find_element_by_name("btn_continue").click()

## Customer Info:
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "caller-first-name"))).click()

    elem = driver.find_element_by_name('First Name').send_keys(fname)
    elem = driver.find_element_by_name("Last Name").send_keys(lname)
    elem = driver.find_element_by_name("Service Address 1").send_keys(address)
    elem = driver.find_element_by_name("City").send_keys(city)
    elem = driver.find_element_by_name("Zip").send_keys(str(zipcode))
    elem = driver.find_element_by_name("Phone Area Code").send_keys(str(area_code))
    elem = driver.find_element_by_name("Phone Prefix").send_keys(str(prefix))
    elem = driver.find_element_by_name("Phone Last Digits").clear()
    elem = driver.find_element_by_name("Phone Last Digits").send_keys(str(last))
    #elem = driver.find_element_by_class_name("copy-to-billing-yes").click()
    elem = driver.find_element_by_class_name("uan").send_keys(str(accountNo))
    elem = driver.find_element_by_class_name("check-account-number").click()

    #for Massachussets
    try:
        elem = driver.find_element_by_name("Customer Key").send_keys("test")
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div/div[6]/input').send_keys("54234567890")
        driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[2]/div/div[6]/button').click()
        time.sleep(2)
        try:
            elem = driver.find_element_by_class_name("check-extra-account-number").click()
        except:
            elem = driver.find_element_by_class_name("Check Electric Choice ID").click()
        elem = driver.find_element_by_class_name("extra-uan").send_keys(service_reference)

    except:
        pass

    time.sleep(6)
    elem = driver.find_element_by_id("btn_continue").click()


## Billing Info:

    WebDriverWait(driver, 200).until(EC.visibility_of_element_located((By.XPATH, '//label[contains(@class,"billing-address")]')))
    elem = driver.find_element_by_name(" Billing Address").send_keys(address)
    elem = driver.find_element_by_name(" City").send_keys(city)
    elem = driver.find_element_by_class_name("state-dropdown")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == state:
            option.click()
    elem = driver.find_element_by_name(" Zip Code").send_keys(str(zipcode))
    elem = driver.find_element_by_name(" Phone Area Code").send_keys(str(area_code))
    elem = driver.find_element_by_name(" Phone Prefix").send_keys(str(prefix))
    elem = driver.find_element_by_name(" Phone Last Digits").send_keys(str(last))
    elem = driver.find_element_by_class_name("email-no").click()
    elem = driver.find_element_by_class_name("email-no-no").click()
    elem = driver.find_element_by_id("btn_continue").click()

## Summary:
    WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.ID, "to-disclosures")))
    elem = driver.find_element(By.ID, "to-disclosures").click()
    #Todo - remove sleep?
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
    WebDriverWait(driver, 200).until(expected_conditions.visibility_of_element_located((By.ID, 'confcode')))
    elem = driver.find_element_by_id("confcode")
    confcode = elem.text
    print("Passed - NRG_regression Inbound Electric, Confirmation =  " + confcode + ' for ' + state + ' - ' + given_utiity)
    f = open("./results.txt", 'a')
    f.write( confcode +" " + "NRG_regression Electric" + "\n")
## Submit:	
    try:
        elem = driver.find_element_by_id("submit_tpv_button").click()
    except:
        elem = driver.find_element_by_id("submit_enroll").click()

## Close Session:
    driver.close()