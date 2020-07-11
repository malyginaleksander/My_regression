from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os

prices = [
	['/html/body/div/div[2]/ul/li[3]/span/div/table/tbody/tr[1]/td[2]',	'Atlantic City Electric - Residential', '$0.11449'],
	['/html/body/div/div[2]/ul/li[3]/span/div/table/tbody/tr[1]/td[3]',	'Atlantic City Electric - Business', '$0.11449'],
	['/html/body/div/div[2]/ul/li[3]/span/div/table/tbody/tr[2]/td[2]',	'JCP&L - Residential', '$0.10486'],
	['/html/body/div/div[2]/ul/li[3]/span/div/table/tbody/tr[2]/td[3]',	'JCP&L - Business',	'$0.09416'],
	['/html/body/div/div[2]/ul/li[3]/span/div/table/tbody/tr[3]/td[2]',	'O&R - Residential', '$0.11900'],
	['/html/body/div/div[2]/ul/li[3]/span/div/table/tbody/tr[3]/td[3]', 'O&R - Business', '$0.09400'],
	['/html/body/div/div[2]/ul/li[3]/span/div/table/tbody/tr[4]/td[2]',	'PSE&G - Residential', '$0.11984'],
	['/html/body/div/div[2]/ul/li[3]/span/div/table/tbody/tr[4]/td[3]',	'PSE&G - Business', '$0.11984']
]

if os.environ.get('USE_PHANTOM'):
    print("using PhantomJS")

    driver = webdriver.PhantomJS()
    driver.implicitly_wait(5)
    driver.set_window_size(1120, 550)
else:
    print("using Firefox")
    driver = webdriver.Firefox()

driver.get("http://www.energypluscompany.com/combined/cashback/nj/?apptype=WE&cellcode=01&campaign=0000&pc=015&pcb=015")

if "We're sorry, this offer has expired." in driver.page_source:
    elem = driver.find_element_by_link_text("click here")
    elem.click()

if "There is a problem" in driver.page_source:
    elem = driver.find_element_by_link_text("Continue to this website (not recommended).")
    elem.click()

for current_row in prices:
    xpath = current_row[0]
    given_utiity = current_row[1]
    price = current_row[2]

#Landing Page
    elem = driver.find_element_by_id('show_price_table').click()
    time.sleep (2)

    element = driver.find_element_by_xpath(xpath)
    if element.text == price:
        print ("Price Pass - ", given_utiity)
    else:
        print ("Price Failed - ", given_utiity)

driver.close()