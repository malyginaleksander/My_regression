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

workbook = xlrd.open_workbook("./links.xlsx")
worksheet = workbook.sheet_by_name("FAQ Links Python")

for current_row in range(1,worksheet.nrows):
    page = worksheet.row(current_row)[0].value
    link = worksheet.row(current_row)[1].value
    xpath = worksheet.row(current_row)[2].value
    expected = worksheet.row(current_row)[3].value

    driver.get(page)
    elem = driver.find_element_by_xpath(link).click()
    time.sleep(1)
    elem = driver.find_element_by_xpath(xpath).click()
	
    if  "Not Found" in driver.page_source:
        print ("failed")

    if  "Server Error" in driver.page_source:
        print ("failed")

    if driver.current_url == expected:
        print ("Passed - ",expected)
    else:
        print ("Failed - ",expected)

driver.get("http://www.pt.energypluscompany.com/care/faqs.php")
elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/ul[3]/li[1]/a").click()
elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/ul[3]/div[1]/div/p/a[2]").click()
if  "Not Found" in driver.page_source:
    print ("Failed - Not Found")

if  "Server Error" in driver.page_source:
    print ("Failed - Server Error")

if driver.current_url == "http://www.pt.energypluscompany.com/service_areas/service_areas.php":
    print ("Passed - http://www.pt.energypluscompany.com/service_areas/service_areas.php")
else:
    print ("Failed - http://www.pt.energypluscompany.com/service_areas/service_areas.php")

driver.close()