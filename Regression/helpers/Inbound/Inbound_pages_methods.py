import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Regression.Inbound.States.Inbound_Enrollments_4brands_test.InboundEnrollments_tests_Settings import  URL




def submit(driver):
    global elem
    time.sleep(2)
    try:
        elem = driver.find_element_by_id("submit_tpv_button").click()
    except:
        pass
    try:
        driver.find_element_by_id('toggle_7_no').click()
    except:
        pass
    try:
        elem = driver.find_element_by_id("submit_enroll").click()
    except:
        print("SUBMIT failed")

def summary(driver):
    global elem
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "to-disclosures")))
    elem = driver.find_element_by_id("to-disclosures").click()

def wait_offer_page(driver):
    WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, ('//span[contains(text(), "1")]'))))

def wait_get_started_page(driver):
    # time.sleep(5)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "caller-first-name")))

def wait_get_started_page_state_list(driver):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, ('state-list'))))

def wait_costumer_info_page(driver):
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "caller-first-name"))).click()

def wait_billing_page(driver):
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//label[contains(@class,"billing-address")]')))

def wait_grab_code_page(driver):
    WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.ID, 'confcode')))

def wait_finish_page(driver):
    WebDriverWait(driver, 50).until(expected_conditions.visibility_of_element_located((By.ID, 'start-new-call')))
# def wait_greenOption_page(driver):
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, ('state-list'))))



def declouser_EP(driver):
    elem = driver.find_element_by_id("toggle_1_no").click()
    elem = driver.find_element_by_id("toggle_2_no").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=IL":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_yes").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        driver.find_element_by_id('toggle_7_no').click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MD":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_yes").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        driver.find_element_by_id('toggle_7_no').click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MA":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_yes").click()
        elem = driver.find_element_by_id("toggle_8_no").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_9_no").click()
        elem = driver.find_element_by_id("toggle_10_yes").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MA":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_yes").click()
        elem = driver.find_element_by_id("toggle_8_no").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_9_no").click()
        elem = driver.find_element_by_id("toggle_10_yes").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=NY":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_6_no").click()


    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=NJ":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=OH":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id('toggle_7_yes').click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=PA":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        driver.find_element_by_id('toggle_6_no').click()
        driver.find_element_by_id('toggle_7_yes').click()


def declouser_GreenME(driver):
    elem = driver.find_element_by_id("toggle_1_no").click()
    elem = driver.find_element_by_id("toggle_2_no").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=IL":
        elem = driver.find_element_by_id("toggle_1_yes").click()
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MD":
        elem = driver.find_element_by_id("toggle_1_yes").click()
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
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
def declouser_GreenME_(driver):
    elem = driver.find_element_by_id("toggle_1_no").click()
    elem = driver.find_element_by_id("toggle_2_no").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=IL":
        elem = driver.find_element_by_id("toggle_1_yes").click()
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MD":
        elem = driver.find_element_by_id("toggle_1_yes").click()
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MA":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("toggle_7_no").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_8_no").click()
        elem = driver.find_element_by_id("toggle_9_yes").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=NJ":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=OH":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("toggle_7_yes").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=PA":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_7_no").click()
        elem = driver.find_element_by_id("toggle_8_yes").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=DC":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("toggle_7_yes").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=NY":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("toggle_7_yes").click()




def declouser_GreenME_GME_env(driver):
    elem = driver.find_element_by_id("toggle_1_no").click()
    elem = driver.find_element_by_id("toggle_2_no").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=IL":
        elem = driver.find_element_by_id("toggle_1_yes").click()
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MD":
        elem = driver.find_element_by_id("toggle_1_yes").click()
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MA":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("toggle_7_no").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_8_no").click()
        elem = driver.find_element_by_id("toggle_9_yes").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=NJ":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=OH":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("toggle_7_yes").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=PA":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_7_no").click()
        elem = driver.find_element_by_id("toggle_8_yes").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=DC":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_no").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("toggle_7_yes").click()
    if driver.current_url == "http://www.gme-plus.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=NY":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("toggle_7_yes").click()




def declouser_NRG(driver):
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
        # try:
        #     elem = driver.find_element_by_id("toggle_7_yes").click()
        # except:
        #     pass

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
    if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=DE":
        elem = driver.find_element_by_id("toggle_3_no").click()
        elem = driver.find_element_by_id("toggle_4_no").click()
        elem = driver.find_element_by_id("toggle_5_yes").click()
        elem = driver.find_element_by_id("toggle_6_no").click()
        elem = driver.find_element_by_id("submit_tpv_button").click()
        elem = driver.find_element_by_id("toggle_7_no").click()
        elem = driver.find_element_by_id("toggle_8_yes").click()




    try:
        elem = driver.find_element_by_id("submit_tpv_button").click()
    except:
        pass
    try:
        elem = driver.find_element_by_id('toggle_6_no').click()
    except:
        pass
    try:
        if driver.current_url == "http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=OH":
            elem = driver.find_element_by_id("toggle_8_no").click()
    except:
        pass
