from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



def fill_personalinformation(driver, payload, firstname, lastname, address, zipcode_, city, accountNo, email, account_number,
                                     phonenumber):
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




    if payload.StateSlug =="MA" or payload.UtilitySlug.upper() =="PGW" or payload.UtilitySlug.upper() =="AEPS" :
        try:
            driver.find_element_by_id('id_electric-billing_uan').send_keys(account_number)
        except:
            pass


    # if test_name == 'PICK_NRG':

    # else:
    #     RewardsNumber = account_number

    try:
        RewardsNumber = '9999999999999999'
        driver.find_element_by_id('id_partner_member_number').send_keys(RewardsNumber)
    except:
        pass
    time.sleep(1)
    try:
        driver.find_element_by_id('continue-submit').click()
    except:
        pass






def fill_personalinformation_pickNRG(driver, payload, test_name, firstname, lastname, address, zipcode_, city, email, phonenumber,
                                     el_account_number, el_accountNo, gas_account_number, gas_accountNo):
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
    driver.find_element_by_id('id_electric-uan').send_keys(el_account_number)
    driver.find_element_by_id('id_service_address_1').send_keys(str(address), Keys.ENTER)
    if  len(str(payload.GasUtility))>0:
        driver.find_element_by_id('id_gas-uan').send_keys(gas_account_number)
        if payload.StateSlug.upper() == "PA":
            try:
                driver.find_element_by_id('id_gas-billing_uan').send_keys(gas_account_number)
            except:
                pass
    try:
        time.sleep(1)
        driver.find_element_by_xpath("//a[text()='Use as it is']").click().send_keys(Keys.ENTER)
    except:
        pass




    if payload.StateSlug =="MA":
        try:
            driver.find_element_by_id('id_electric-billing_uan').send_keys(el_account_number)
        except:
            pass


    # if test_name == 'PICK_NRG':
    # else:
    #     RewardsNumber = account_number

    try:
        RewardsNumber = '9999999999999999'
        driver.find_element_by_id('id_partner_member_number').send_keys(RewardsNumber)
    except:
        pass
    time.sleep(1)
    try:
        driver.find_element_by_id('continue-submit').click()
    except:
        pass


