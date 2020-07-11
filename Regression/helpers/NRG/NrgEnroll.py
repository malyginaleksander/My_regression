from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def fill_personalinformation(driver, payload, firstname, lastname, address, zipcode_, city, accountNo, email, account_number, phonenumber):
    try:
        driver.switch_to_alert()
        driver.find_element_by_class_name('close').click()
    except:
        pass
    time.sleep(1)
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'id_first_name')))
    driver.find_element_by_id('id_first_name').click()
    driver.find_element_by_id('id_first_name').send_keys(firstname)
    driver.find_element_by_id('id_last_name').send_keys(lastname)
    driver.find_element_by_id('id_email').send_keys(email)
    driver.find_element_by_id('id_ver_email').send_keys(email)
    driver.find_element_by_id('id_phone').send_keys(str(phonenumber))
    driver.find_element_by_id('id_service_address_zip').click()
    driver.find_element_by_id('id_service_address_city').send_keys(str(city))
    driver.find_element_by_id('id_service_address_zip').send_keys(str(zipcode_))
    driver.find_element_by_id('id_electric-uan').send_keys(account_number)
    driver.find_element_by_id('id_service_address_1').send_keys(str(address), Keys.ENTER)
    try:
        time.sleep(1)
        driver.find_element_by_xpath("//a[text()='Use as it is']").click().send_keys(Keys.ENTER)
    except:
        pass


    if payload.StateSlug=="PA":
        try:
            driver.find_element_by_id('id_electric-billing_uan').send_keys(account_number)
        except:
            pass

    if payload.UtilitySlug.lower() =="wmeco":
        driver.find_element_by_id('id_electric-billing_uan').send_keys(account_number)


    try:
        driver.find_element_by_id('id_partner_member_number').send_keys(account_number)
    except:
        pass
    time.sleep(1)
    try:
        driver.find_element_by_id('continue-submit').click()
    except:
        pass


