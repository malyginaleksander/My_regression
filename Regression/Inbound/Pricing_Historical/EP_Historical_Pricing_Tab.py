from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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
time.sleep(2)

elem = driver.find_element_by_id("brandId_1").click()
elem = driver.find_element_by_id("btn_continue").click()
time.sleep(2)

elem = driver.find_element_by_link_text("Historical Pricing").click()
time.sleep(2)

workbook = xlrd.open_workbook("./Historical_Pricing.xlsx")
worksheet = workbook.sheet_by_name('EP-pricing')

for current_row in range(1,worksheet.nrows):
    state = worksheet.row(current_row)[0].value
    commodity = worksheet.row(current_row)[1].value
    given_utiity = worksheet.row(current_row)[2].value

    elem = driver.find_element_by_id("state")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == state:
            option.click()
    elem = driver.find_element_by_id("commodity")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == commodity:
            option.click()
    elem = driver.find_element_by_id("utility")
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == given_utiity:
            option.click()
    time.sleep(3)

    if driver.find_element_by_id("tbl_histpricing").is_displayed():
        print("Passed - EP Historic Pricing for " + state +' ' + commodity +' - ' + given_utiity)
    else:
       	print("Passed - EP Historic Pricing for " + state +' ' + commodity +' - ' + given_utiity)

driver.close()

### Pennsylvania ###
driver = webdriver.Firefox()
driver.get("http://www.pt.energypluscompany.com/myinbound/login.php")

#login
elem = driver.find_element_by_name("email").send_keys("mpeters@energypluscompany.com")
elem = driver.find_element_by_name("password").send_keys("energy")
elem = driver.find_element_by_id("button").click()
time.sleep(2)

elem = driver.find_element_by_id("brandId_1").click()
elem = driver.find_element_by_id("btn_continue").click()
time.sleep(2)

elem = driver.find_element_by_link_text("Historical Pricing").click()
time.sleep(2)

elem = driver.find_element_by_id("state")
for option in elem.find_elements_by_tag_name('option'):
    if option.text == ("Pennsylvania"):
        option.click()
time.sleep(3)
if driver.find_element_by_link_text("www.energypluscompany.com/PAHistoricalPricing").is_displayed():
    print ("Passed - EP Historic Pricing for Pennsylvania")
else:
    print ("Failed - EP Historic Pricing for Pennsylvania")
driver.close()