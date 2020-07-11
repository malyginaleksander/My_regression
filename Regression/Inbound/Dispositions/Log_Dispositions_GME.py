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

workbook = xlrd.open_workbook("./Dispositions_data.xlsx")
worksheet = workbook.sheet_by_name('GM-Log Dispo')

for current_row in range(1,worksheet.nrows):
    disposition = worksheet.row(current_row)[0].value

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
            if option.text == ("Green Mountain Energy"):
        	    option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/form/input[3]").click() #Start Call Button
        driver.switch_to.alert.accept()

    else:
        elem = driver.find_element_by_id("brandId_5").click()
        elem = driver.find_element_by_id("btn_continue").click()
    time.sleep(2)

    elem = driver.find_element_by_id("log-dispo").click()
    time.sleep(2)

    elem = driver.find_element_by_id("log-dispo")
    time.sleep(4)
    elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[3]/div/div/div[2]/div[1]/select") #dispo list
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == disposition:
            option.click()  	
    time.sleep (1)

    if 	driver.find_element_by_name("dispo-comments").is_displayed():
        time.sleep(1)
        elem = driver.find_element_by_name("dispo-comments").send_keys("test")
        time.sleep(1)
    else:
        elem = driver.find_element_by_id("dispo-start-new").click()
    elem = driver.find_element_by_id("dispo-start-new").click()
    time.sleep(2)
    driver.close()

    print ("Passed - GME, ",disposition)