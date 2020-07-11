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

driver = webdriver.Firefox()
driver.get("http://www.pt.energypluscompany.com/myinbound/login.php")

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

#Get Started Tab
elem = driver.find_element_by_id("sop-button").click()
elem = driver.find_element_by_id("save-and-continue").click()
time.sleep(2)

elem = driver.find_element_by_class_name("campaigns")
for option in elem.find_elements_by_tag_name('option'):
    if option.text == "6666 - Rate Class RS - Residential Service":
        option.click()
elem = driver.find_element_by_class_name("promos-dropdown")
for option in elem.find_elements_by_tag_name('option'):
    if option.text == "000 - PA Standard Offer":
        option.click()
elem = driver.find_element_by_id("btn_continue").click()
time.sleep(5)
elem = driver.find_element_by_link_text("FAQs").click()
time.sleep(5)

###### Main Headers ######
workbook = xlrd.open_workbook("./FAQ_Regression_data.xlsx")
worksheet = workbook.sheet_by_name('EP-SOP')

for current_row in range(1,worksheet.nrows):
    index = worksheet.row(current_row)[0].value
    header = worksheet.row(current_row)[1].value
    passed = worksheet.row(current_row)[2].value
    fail = worksheet.row(current_row)[3].value

    if header in driver.page_source:
        print ("Passed EP SOP - ",header)
    else:
        print ("Failed EP SOP - ",header)

driver.close()