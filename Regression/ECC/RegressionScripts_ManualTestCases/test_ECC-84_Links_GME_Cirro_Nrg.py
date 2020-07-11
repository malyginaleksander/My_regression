from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
import xlrd
import os


def run_function():
    if os.environ.get('USE_PHANTOM'):
        print("using PhantomJS")

        driver = webdriver.PhantomJS()
        driver.implicitly_wait(5)
        driver.set_window_size(1120, 550)
    else:
        print("using Firefox")
        driver = webdriver.Firefox()

    workbook = xlrd.open_workbook("./ECC_TestData/TestData.xlsx")
    worksheet = workbook.sheet_by_name('links')

    for current_row in range(1, worksheet.nrows):
        page = worksheet.row(current_row)[0].value
        xpath = worksheet.row(current_row)[1].value
        expected = worksheet.row(current_row)[2].value

        driver.get(page)
        driver.find_element_by_xpath(xpath)

        if "Not Found" in driver.page_source:
            raise Exception("Failed - Not Found")

        if "Server Error" in driver.page_source:
            raise Exception("Failed - Server Error")

        if driver.current_url == expected:
            print("Passed - ", expected)
        else:
            raise Exception("Failed - ", expected)

    driver.close()


if __name__ == 'main':
    run_function()
