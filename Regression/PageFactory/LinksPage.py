import logging
import ConfigFiles.logger as cl
import time
from Pagefactory.BasePage import BasePage


def test_state(driver, payload):
    print(payload.tc, 'EP Web Page Links - ', payload.page, payload.Section)

    driver.get(payload.page)
    elem = driver.find_element_by_xpath(payload.xpath).click()

    if  "Not Found" in driver.page_source:
        print ("Failed - Not Found")

    if  "Server Error" in driver.page_source:
        print ("Failed - Server Error")

    assert driver.current_url == payload.expected
