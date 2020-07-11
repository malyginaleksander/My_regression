import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from Regression.Inbound.States.Inbound_Enrollments_4brands_test.InboundEnrollments_tests_Settings import  URL


def setUp():
    global driver
    driver = webdriver.Firefox()
    driver.get(URL)

def login(driver):
    global elem
    elem = driver.find_element_by_name("email").send_keys('aleksandr.malygin@nrg.com')
    elem = driver.find_element_by_name("password").send_keys("energy")
    elem = driver.find_element_by_id("button").click()


def if_start_manual_call(driver):
    global elem, option
    if "Start a manual call" in driver.page_source:
        elem = driver.find_element_by_link_text("Start a manual call").click()
        elem = driver.find_element_by_id("phoneNumber").send_keys("5454588883")
        elem = driver.find_element_by_id("reason").send_keys("this is a test")
        elem = driver.find_element_by_id("brand_id")
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == ("Energy Plus"):
                option.click()
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/form/input[3]").click()  # Start Call Button
        driver.switch_to.alert.accept()
    else:
        elem = driver.find_element_by_id("brandId_1").click()
        elem = driver.find_element_by_id("btn_continue").click()
    # time.sleep(2)


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
    #
    # try:
    #     elem = driver.find_element_by_id("Submit Enrollment").click()
    # except:
    #     pass




        #     elem = driver.find_element_by_xpath(
        #         "/html/body/div[2]/div/div[1]/div[7]/div[4]/label[1]/input").click()  # choose residential
        # # How do you use your natural gas?
        # elem = driver.find_element_by_xpath(
        #     "/html/body/div[2]/div/div[1]/div[7]/div[5]/div[3]/label/input").click()