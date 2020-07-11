from selenium.webdriver.common.by import By
from PageFactory.BasePage import BasePage
from selenium import webdriver
import ConfigFiles.logger as cl
import logging
import time

class EnergyPlusPage(BasePage):
    log = cl.genericLogger(logging.DEBUG)

    def __init__(self,driver):
        super().__init__(driver)
        self.driver = driver
        self.driver.implicitly_wait(15)

    def select_option(self, selectValue, elem):
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == selectValue:
                option.click()
                break
        time.sleep(1)


    #locators
    email_locator= "email"
    pwd_locator= "password"
    login_submit_locator= "button"
    fname_locator= "customer_first_name"
    lname_locator= "customer_last_name"
    addr1_locator= "customer_address1"
    city_locator= "customer_city"
    state_locator= "customer_state"
    zip5_locator= "customer_zip5"
    area_code_locator= "customer_area_code"
    prefix_locator= "customer_prefix"
    line_num_locator= "customer_line_number"
    account_type_locator= "account_type"
    disclosure_locator = "to-disclosures"
    business_name_locator= "business_name"
    copy_information_locator= "copyinfo"
    commodity_gas_locator= "egr_commodity_gas"
    gas_utility_locator= "gas_utility"
    gas_account_num_locator= "gas_account_number"
    coned_zone_locator= "coned_zone"
    spanishbill_locator= "spanishbill"
    electric_green_locator = "electric_green"
    electric_utility_locator= "electric_utility"
    electric_account_number_locator= "electric_account_number"
    electric_account_number2_locator= "electric_extra_account_number"
    offertypes_gas_locator= "offer_types_gas"
    partnercodegas_locator= "partner_code_gas"
    campaign_codegas_locator= "campaign_code_gas"
    promo_codegas_locator= "promo_code_gas"
    partner_code_epgas_locator = "partner_code"
    campaign_code_epgas_locator= "campaign_code"
    promo_code_epgas_locator= "gas_promo_code"
    offer_types_electric_locator= "offer_types_electric"
    partner_code_locator= "partner_code"
    campaign_code_offer_locator= "campaign_code_offer"
    promo_code_locator= "promo_code"
    campaign_code_locator= "campaign_code"
    elec_promo_code_locator= "elec_promo_code"
    electric_products_gme_locator = "electric_products_gme"
    vendor_id_locator= "vendor_id"
    conf_code_locator = "confcode"
    submit_locator = "submit"
    submit_enroll_locator = "submit_enroll"
    manual_call_locator= "Start a manual call"
    phone_number_locator= "phoneNumber"
    reason_locator= "reason"
    brand_id_locator= "brand_id"
    start_call_locator= "/html/body/div[2]/div/div[1]/form/input[3]"
    nrg_brand_locator= "brandId_2"
    energyPlus_brand_locator= "brandId_1"
    save_continue_inbound_brand_page_locator= "btn_continue"
    caller_fname_locator = "caller-first-name"
    caller_lname_locator= "caller-last-name"
    state_list_locator= "state-list"
    greenmountain_brand_locator = "brandId_5"
    commodity_choice_electric_locator= "commodity-choice-electric"
    inbound_account_provider_locator= "/html/body/div[2]/div/div[1]/div[6]/div[3]/div[1]/label/input"
    inbound_utilitylist_locator= "utility-list"
    egr_commodity_electric_locator= "egr_commodity"
    acctype_residential_locator= "account-type-residential"
    nrg_add_acct_locator= "add-account-button"
    calling_state_locator= "/html/body/div[2]/div/div[1]/div[7]/div[1]/select"
    electric_for_acc2_locator= "/html/body/div[2]/div/div[1]/div[7]/div[2]/div[1]/label/input"
    select_electricutility_in_addacc_locator= "/html/body/div[2]/div/div[1]/div[7]/div[3]/select"
    addacctype_residential_locator= "/html/body/div[2]/div/div[1]/div[7]/div[4]/label[1]/input"
    save_continue_locator= "save-and-continue"
    gas_for_acc2_locator= "/html/body/div[2]/div/div[1]/div[7]/div[2]/div[2]/label/input"
    cashback_plan_locator= "/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/div[1]/div[1]/div[2]"
    primary_plans_arrow_locator= "/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[2]/div/div[4]/div[1]/p/span[1]/a"
    cashback_plan_for_acc2_locator= "/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[2]/div/div[4]/div[1]/div[1]/div[2]"
    offer_continue_locator= "btn_continue"
    variable_acc1_locator= "/html/body/div[2]/div/div[1]/div[3]/div[1]/div/p/button[2]"
    categories_locator= "categories"
    nrgElec_acctTpe_locator = "commodity-choice-electric"
    partners_locator= "partners"
    campaigns_locator= "campaigns"
    promos_locator= "promos"
    variable_acc2_locator= "/html/body/div[2]/div/div[1]/div[3]/div[2]/div/p/button[2]"
    category_for_acc2_locator= "/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/p[1]/select"
    partner_for_acc2_locator= "/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[1]/p[2]/select"
    campaign_for_acc2_locator= "/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/p[1]/select"
    promo_for_acc2_locator= "/html/body/div[2]/div/div[1]/div[3]/div[2]/div/div[2]/div[2]/p[2]/select"
    green_option_no_locator= "green_option_no"
    inbound_firstName_locator = "First Name"
    inbound_lastname_locator= "Last Name"
    inbound_service_add1_locator= "Service Address 1"
    inbound_city_locator= " City"
    inbound_customer_city_locator= "City"
    inbound_zipcode_locator= "Zip"
    inbound_phone_area_code_locator= " Phone Area Code"
    inbound_phone_prefix_locator= " Phone Prefix"
    inbound_phone_last_digits_locator= " Phone Last Digits"
    inbound_cust_phone_area_code_locator= "Phone Area Code"
    inbound_cust_phone_prefix_locator= "Phone Prefix"
    inbound_cust_phone_last_digits_locator= "Phone Last Digits"
    inbound_uan_locator= "uan"
    inbound_check_account_number_locator= "check-account-number"
    inbound_same_information_locator= "//*[contains(@class,'same-as-first')]"
    account_number_for_acc2_locator= "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[6]/input[1]"
    account_number__for_acc2_locator= "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[6]/input"
    btn_elem_locator= "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[6]/button"
    account2_locator= "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/input[1]"
    billing_addr1_locator= "//*[contains(@id,'billing-baddr1')]"
    state_dropdown_locator= "state-dropdown"
    zip_code1_locator= " Zip Code"
    billing_info_email1_locator= "email-no"
    billing_info_email2_locator= "email-no-no"
    same_email_locator= "same-emailchoice-as-first"
    customer_key_locator= "Customer Key"
    extra_uan_locator= "extra-uan"
    extra_account_number_locator= "check-extra-account-number"
    disclosures_yes_verify_accnumber_billingadd_locator= "toggle_1_no"
    disclosure_yes_authorization_pause_for_response_locator= "toggle_2_no"
    disclosure_yes_note_to_tsr_locator= "toggle_3_no"
    dislosure_yes_accept_terms_as_read_locator= "toggle_4_no"
    disclosure_yes_tpv_answer_any_questions_locator= "toggle_5_no"
    disclosure_no_tpv_answer_any_questions_locator= "toggle_5_yes"
    disclosure_no_continue_enrollment_locator= "toggle_6_yes"
    disclosure_yes_continue_enrollment_locator= "toggle_6_no"
    disclosure_yes_anything_icando_today_locator= "toggle_8_no"
    disclosure_no_anything_icando_today_locator= "toggle_8_yes"
    tpv_btn_locator= "submit_tpv_button"
    disclosure_yes_ma_locator= "toggle_9_no"
    disclosure_no_ma_locator = "toggle_9_yes"
    disclosure_no_transfer_tpv_locator= "toggle_7_yes"
    disclosure_yes_transfer_tpv_locator = "toggle_7_no"
    show_price_table_locator= "show_price_table"
    offer_locator= "/html/body/div[2]/div/div[1]/div[3]/div/div/p/button[2]"
    customer_info_account2_locator= "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/input"
    save_account2_locator= "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/button"
    ep_acc2_locator= "/html/body/div[2]/div/div[1]/div[2]/div[2]/div[6]/input"
    gm_electric_add_acc_locator= "/html/body/div[2]/div/div[1]/div[7]/div[3]/select"
    acc2_residential_locator= "/html/body/div[2]/div/div[1]/div[7]/div[4]/label[1]/input"
    nrg_electric_account_provider_locator= "/html/body/div[2]/div/div[1]/div[6]/div[3]/div[1]/label/input"
    nrg_electric_utility_list_locator= "utility-list"
    nrg_elctric_account_type_residential_locator= "account-type-residential"



    #LOGIN INBOUND
    def login(self,payload):
        self.driver.find_element_by_name(self.email_locator).send_keys("mpeters@energypluscompany.com")
        self.driver.find_element_by_name(self.pwd_locator).send_keys("energy")
        self.driver.find_element_by_id(self.login_submit_locator).click()
        time.sleep(2)


    # CALL PROCESS:

    #Call process EP Electric
    def start_call_EP_electric(self):
        elem = self.driver.find_element_by_id(self.energyPlus_brand_locator).click()
        elem = self.driver.find_element_by_id(self.save_continue_inbound_brand_page_locator).click()
        time.sleep(2)

    # Call process GM Electric
    def start_call_GM_electric(self):
        elem = self.driver.find_element_by_id(self.greenmountain_brand_locator).click()
        elem = self.driver.find_element_by_id(self.save_continue_inbound_brand_page_locator).click()
        time.sleep(2)


    # Call process NRG_regression Electric
    def start_call_NRG_electric(self):
        elem = self.driver.find_element_by_id(self.nrg_brand_locator).click()
        elem = self.driver.find_element_by_id(self.save_continue_inbound_brand_page_locator).click()


    # GET STARTED

    def get_started_in_call(self,payload):
        elem = self.driver.find_element_by_id(self.caller_fname_locator).send_keys(payload.fname)
        elem = self.driver.find_element_by_id(self.caller_lname_locator).send_keys(payload.lname)
        elem = self.driver.find_element_by_name(self.state_list_locator)
        self.select_option( payload.state, elem)


    # ACCOUNT TYPE, PROVIDER, UTILITYLIST, RESIDENTIAL/BUSINESS- ELECTRIC

    def inbound_ep_electric_steps(self, payload):
        elem = self.driver.find_element_by_name(self.inbound_utilitylist_locator)
        self.select_option(payload.utility, elem)
        elem = self.driver.find_element_by_class_name(self.acctype_residential_locator).click()
        elem = self.driver.find_element_by_id(self.save_continue_locator).click()


    def inbound_ep_electric_steps_new(self, payload):
        # Is Your Name on the Utility Bill?
        elem = self.driver.find_element_by_name(self.inbound_utilitylist_locator)
        self.select_option(payload.utility, elem)
        # Is this electric account a residential or business address?
        elem = self.driver.find_element_by_class_name(self.acctype_residential_locator).click()
        elem = self.driver.find_element_by_id(self.save_continue_locator).click()


    def ep_multi_electric_acct_steps(self,payload):
        elem = self.driver.find_element_by_name(self.inbound_utilitylist_locator)
        self.select_option(payload.utility, elem)
        elem = self.driver.find_element_by_class_name(self.acctype_residential_locator).click()
        elem = self.driver.find_element_by_id(self.nrg_add_acct_locator).click()
        time.sleep(1)
        elem = self.driver.find_element_by_xpath(self.calling_state_locator)
        self.select_option(payload.state, elem)
        time.sleep(1)
        elem = self.driver.find_element_by_xpath(self.select_electricutility_in_addacc_locator)
        self.select_option(payload.utility, elem)
        elem = self.driver.find_element_by_xpath(self.addacctype_residential_locator).click()
        time.sleep(1)
        elem = self.driver.find_element_by_id(self.save_continue_locator).click()
        time.sleep(2)


    def gm_electric_acct_steps(self,payload):
        elem = self.driver.find_element_by_name(self.inbound_utilitylist_locator)
        self.select_option(payload.utility, elem)
        elem = self.driver.find_element_by_class_name(self.acctype_residential_locator).click()
        elem = self.driver.find_element_by_id(self.save_continue_locator).click()
        time.sleep(2)


    def gm_electric_multiple_acct_steps(self, payload):
        elem = self.driver.find_element_by_name(self.nrg_electric_utility_list_locator)
        self.select_option(payload.utility, elem)
        elem = self.driver.find_element_by_class_name(self.nrg_elctric_account_type_residential_locator).click()
        elem = self.driver.find_element_by_id(self.nrg_add_acct_locator).click()
        time.sleep(1)
        elem = self.driver.find_element_by_xpath(self.calling_state_locator)
        self.select_option(payload.state, elem)
        time.sleep(1)
        elem = self.driver.find_element_by_xpath(self.gm_electric_add_acc_locator)
        self.select_option(payload.utility, elem)
        elem = self.driver.find_element_by_xpath(self.acc2_residential_locator).click()
        time.sleep(1)
        elem = self.driver.find_element_by_id(self.save_continue_locator).click()
        time.sleep(2)

    def nrg_electric_acct_steps(self, payload):
        elem = self.driver.find_element_by_class_name(self.nrgElec_acctTpe_locator).click()
        elem = self.driver.find_element_by_name(self.inbound_utilitylist_locator)
        self.select_option(payload.utility, elem)
        elem = self.driver.find_element_by_class_name(self.acctype_residential_locator).click()
        elem = self.driver.find_element_by_id(self.save_continue_locator).click()
        time.sleep(2)

    def nrg_multi_electric_acct_steps(self,payload):
        elem = self.driver.find_element_by_class_name(self.nrgElec_acctTpe_locator).click()
        elem = self.driver.find_element_by_name(self.inbound_utilitylist_locator)
        self.select_option(payload.utility, elem)
        elem = self.driver.find_element_by_class_name(self.acctype_residential_locator).click()
        elem = self.driver.find_element_by_id(self.nrg_add_acct_locator).click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath(self.calling_state_locator)
        self.select_option(payload.state, elem)
        time.sleep(1)
        elem = self.driver.find_element_by_xpath(self.electric_for_acc2_locator).click()
        elem = self.driver.find_element_by_xpath(self.select_electricutility_in_addacc_locator)
        self.select_option(payload.utility, elem)
        elem = self.driver.find_element_by_xpath(self.addacctype_residential_locator).click()
        elem = self.driver.find_element_by_id(self.save_continue_locator).click()
        time.sleep(2)

    ## OFFER:

    # CATEGORIES, PARTNERS, CAMPAIGNS. PROMOS
    def ep_elec_offer1(self,payload):
        if self.driver.find_element_by_xpath(self.offer_locator).is_displayed():
            elem = self.driver.find_element_by_xpath(self.offer_locator).click()
        elem = self.driver.find_element_by_class_name(self.categories_locator)
        self.select_option("Cash Back", elem)
        elem = self.driver.find_element_by_class_name(self.partners_locator)
        self.select_option(payload.partner, elem)
        elem = self.driver.find_element_by_class_name(self.campaigns_locator)
        self.select_option(payload.campaign, elem)
        elem = self.driver.find_element_by_class_name(self.promos_locator)
        self.select_option(payload.promo, elem)
        elem = self.driver.find_element_by_id(self.green_option_no_locator).click()
        elem = self.driver.find_element_by_id(self.offer_continue_locator).click()
        time.sleep(1)

    def ep_elec_offer1_new(self,payload):
        elem = self.driver.find_element_by_xpath(self.offer_locator).click()
        elem = self.driver.find_element_by_class_name(self.categories_locator)
        self.select_option("Cash Back", elem)
        elem = self.driver.find_element_by_class_name(self.partners_locator)
        self.select_option(payload.partner, elem)
        elem = self.driver.find_element_by_class_name(self.campaigns_locator)
        self.select_option(payload.campaign, elem)
        elem = self.driver.find_element_by_class_name(self.promos_locator)
        self.select_option(payload.promo, elem)
        elem = self.driver.find_element_by_id(self.green_option_no_locator).click()
        elem = self.driver.find_element_by_id(self.offer_continue_locator).click()
        time.sleep(1)

    def ep_multi_elec_offer1(self):
        if self.driver.find_element_by_xpath(self.variable_acc1_locator).is_displayed():
            elem = self.driver.find_element_by_xpath(self.variable_acc1_locator).click()
        elem = self.driver.find_element_by_class_name(self.categories_locator)
        self.select_option("Cash Back", elem)
        elem = self.driver.find_element_by_class_name(self.partners_locator)
        self.select_option("Brand Residential - PA - BRC", elem)
        elem = self.driver.find_element_by_class_name(self.campaigns_locator)
        self.select_option("0000 - Unknown", elem)
        elem = self.driver.find_element_by_class_name(self.promos_locator)
        self.select_option("015 - $25 bonus / 3%", elem)
        time.sleep(2)

    def ep_multi_elec_offer2(self):
        if self.driver.find_element_by_xpath(self.variable_acc2_locator).is_displayed():
            elem = self.driver.find_element_by_xpath(self.variable_acc2_locator).click()
        elem = self.driver.find_element_by_xpath(self.category_for_acc2_locator)
        self.select_option("Cash Back", elem)
        elem = self.driver.find_element_by_xpath(self.partner_for_acc2_locator)
        self.select_option("Brand Residential - PA - BRC", elem)
        elem = self.driver.find_element_by_xpath(self.campaign_for_acc2_locator)
        self.select_option("0000 - Unknown", elem)
        elem = self.driver.find_element_by_xpath(self.promo_for_acc2_locator)
        self.select_option("015 - $25 bonus / 3%", elem)
        time.sleep(2)
        elem = self.driver.find_element_by_id(self.green_option_no_locator).click()
        elem = self.driver.find_element_by_id(self.offer_continue_locator).click()
        time.sleep(2)

    ## Offer for GM and NRG_regression elec
    def Inbound_Offers(self, payload):
        time.sleep(2)
        elem = self.driver.find_element_by_id(payload.plan).click()
        elem = self.driver.find_element_by_id
        elem = self.driver.find_element_by_name(self.save_continue_inbound_brand_page_locator).click()
        time.sleep(2)


    ## Offer for green mountain Multiplte
    def green_mountain_elec_multiple_offer(self, payload):
        elem = self.driver.find_element_by_id(payload.plan).click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath(self.primary_plans_arrow_locator).click()
        elem = self.driver.find_element_by_xpath(self.cashback_plan_for_acc2_locator).click()
        time.sleep(3)
        elem = self.driver.find_element_by_name(self.offer_continue_locator).click()
        time.sleep(2)


    ## Offer for nrg multi electric
    def nrg_multi_elec_offer(self):
        elem = self.driver.find_element_by_xpath(self.cashback_plan_locator).click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath(self.primary_plans_arrow_locator).click()
        elem = self.driver.find_element_by_xpath(self.cashback_plan_for_acc2_locator).click()
        time.sleep(3)
        elem = self.driver.find_element_by_name(self.offer_continue_locator).click()
        time.sleep(2)



    ## CUSTOMER INFORMATION
    def customer_info(self, payload):
        elem = self.driver.find_element_by_name(self.inbound_firstName_locator).send_keys(payload.fname)
        elem = self.driver.find_element_by_name(self.inbound_lastname_locator).send_keys(payload.lname)
        elem = self.driver.find_element_by_name(self.inbound_service_add1_locator).send_keys(payload.address)
        elem = self.driver.find_element_by_name(self.inbound_customer_city_locator).send_keys(payload.city)
        elem = self.driver.find_element_by_name(self.inbound_zipcode_locator).send_keys(payload.zipcode)
        elem = self.driver.find_element_by_name(self.inbound_cust_phone_area_code_locator).send_keys(str(payload.area_code))
        elem = self.driver.find_element_by_name(self.inbound_cust_phone_prefix_locator).send_keys(str(payload.prefix))
        elem = self.driver.find_element_by_name(self.inbound_cust_phone_last_digits_locator).clear()
        elem = self.driver.find_element_by_name(self.inbound_cust_phone_last_digits_locator).send_keys(str(payload.last))
        # elem = driver.find_element_by_class_name("copy-to-billing-yes").click()
        elem = self.driver.find_element_by_class_name(self.inbound_uan_locator).send_keys(str(payload.accountNo))
        time.sleep(1)
        elem = self.driver.find_element_by_class_name(self.inbound_check_account_number_locator).click()
        time.sleep(3)
        elem = self.driver.find_element_by_id(self.save_continue_inbound_brand_page_locator).click()
        time.sleep(2)


    def gm_multi_electric_customer_info(self, payload):
        elem = self.driver.find_element_by_name(self.inbound_firstName_locator).send_keys(payload.fname)
        elem = self.driver.find_element_by_name(self.inbound_lastname_locator).send_keys(payload.lname)
        elem = self.driver.find_element_by_name(self.inbound_service_add1_locator).send_keys(payload.address)
        elem = self.driver.find_element_by_name(self.inbound_customer_city_locator).send_keys(payload.city)
        elem = self.driver.find_element_by_name(self.inbound_zipcode_locator).send_keys(payload.zipcode)
        elem = self.driver.find_element_by_name(self.inbound_cust_phone_area_code_locator).send_keys(str(payload.area_code))
        elem = self.driver.find_element_by_name(self.inbound_cust_phone_prefix_locator).send_keys(str(payload.prefix))
        elem = self.driver.find_element_by_name(self.inbound_cust_phone_last_digits_locator).clear()
        elem = self.driver.find_element_by_name(self.inbound_cust_phone_last_digits_locator).send_keys(str(payload.last))
        # elem = driver.find_element_by_class_name("copy-to-billing-yes").click()
        elem = self.driver.find_element_by_class_name(self.inbound_uan_locator).send_keys(str(payload.accountNo))
        time.sleep(1)
        elem = self.driver.find_element_by_class_name(self.inbound_check_account_number_locator).click()
        time.sleep(1)


    def nrg_multi_electric_customer_info(self, payload):
        elem = self.driver.find_element_by_name(self.inbound_firstName_locator).send_keys(payload.fname)
        elem = self.driver.find_element_by_name(self.inbound_lastname_locator).send_keys(payload.lname)
        elem = self.driver.find_element_by_name(self.inbound_service_add1_locator).send_keys(payload.address)
        elem = self.driver.find_element_by_name(self.inbound_customer_city_locator).send_keys(payload.city)
        elem = self.driver.find_element_by_name(self.inbound_zipcode_locator).send_keys(payload.zipcode)
        elem = self.driver.find_element_by_name(self.inbound_cust_phone_area_code_locator).send_keys(str(payload.area_code))
        elem = self.driver.find_element_by_name(self.inbound_cust_phone_prefix_locator).send_keys(str(payload.prefix))
        elem = self.driver.find_element_by_name(self.inbound_cust_phone_last_digits_locator).clear()
        elem = self.driver.find_element_by_name(self.inbound_cust_phone_last_digits_locator).send_keys(str(payload.last))
        # elem = driver.find_element_by_class_name("copy-to-billing-yes").click()
        elem = self.driver.find_element_by_class_name(self.inbound_uan_locator).send_keys(str(payload.accountNo))
        time.sleep(1)
        elem = self.driver.find_element_by_class_name(self.inbound_check_account_number_locator).click()
        time.sleep(1)


    def customer_info_submit_Inbound(self, payload):
        elem = self.driver.find_element_by_id(self.save_continue_inbound_brand_page_locator).click()
        time.sleep(1)


    # customer info ep multi elec: part 2
    def fill_ep_multi_elec_cust_info_submit(self,payload):
        elem = self.driver.find_element_by_class_name(self.inbound_same_information_locator).click()
        time.sleep(1)
        elem = self.driver.find_element_by_xpath(self.account2_locator).click()
        elem = self.driver.find_element_by_xpath(self.ep_acc2_locator).send_keys(str(payload.accountNo2))
        elem = self.driver.find_element_by_xpath(self.btn_elem_locator).click()
        time.sleep(2)
        elem = self.driver.find_element_by_id(self.save_continue_inbound_brand_page_locator).click()
        time.sleep(2)


    ## cust info part 2 for green mountain
    def fill_green_mountain_cust_info_2(self,payload):
        elem = self.driver.find_element_by_name(self.customer_key_locator).send_keys("test")
        elem = self.driver.find_element_by_class_name(self.extra_uan_locator).send_keys(payload.service_reference)
        elem = self.driver.find_element_by_class_name(self.extra_account_number_locator).click()
        time.sleep(2)


    def fill_green_mountain_elec_cust_info_3_submit(self, payload):
        elem = self.driver.find_element_by_xpath(self.inbound_same_information_locator).click()
        elem = self.driver.find_element_by_xpath(self.customer_info_account2_locator).click()
        elem = self.driver.find_element_by_xpath(self.customer_info_account2_locator).send_keys(str(payload.accountNo))
        elem = self.driver.find_element_by_xpath(self.save_account2_locator).click()
        time.sleep(2)
        elem = self.driver.find_element_by_id(self.save_continue_inbound_brand_page_locator).click()
        time.sleep(2)


    # customer info: Part 2 and submit
    def fill_nrg_multi_elec_cust_info_submit(self, payload):
        elem = self.driver.find_element_by_xpath(self.inbound_same_information_locator).click()
        elem = self.driver.find_element_by_xpath(self.account_number_for_acc2_locator).click()
        elem = self.driver.find_element_by_xpath(self.account_number__for_acc2_locator).send_keys(str(payload.accountNo))
        elem = self.driver.find_element_by_xpath(self.btn_elem_locator).click()
        time.sleep(2)
        elem = self.driver.find_element_by_id(self.save_continue_inbound_brand_page_locator).click()
        time.sleep(2)



    # BILLING INFORMATION

    def billing_info_Inbound(self, payload):
        ## Billing Info:
        self.driver.find_element_by_xpath(self.billing_addr1_locator).send_keys(payload.address)
        self.driver.find_element_by_name(self.inbound_city_locator).send_keys(payload.city)
        elem = self.driver.find_element_by_class_name(self.state_dropdown_locator)
        self.select_option(payload.state, elem)
        elem = self.driver.find_element_by_name(self.zip_code1_locator).send_keys(payload.zipcode)
        elem = self.driver.find_element_by_name(self.inbound_phone_area_code_locator).send_keys(str(payload.area_code))
        elem = self.driver.find_element_by_name(self.inbound_phone_prefix_locator).send_keys(str(payload.prefix))
        elem = self.driver.find_element_by_name(self.inbound_phone_last_digits_locator).send_keys(str(payload.last))
        elem = self.driver.find_element_by_class_name(self.billing_info_email1_locator).click()
        elem = self.driver.find_element_by_class_name(self.billing_info_email2_locator).click()
        elem = self.driver.find_element_by_id(self.save_continue_inbound_brand_page_locator).click()
        time.sleep(2)


    def billing_Info_Multi_Electric(self, payload):
        ## Billing Info:
        elem = self.driver.find_element_by_xpath(self.billing_addr1_locator).send_keys(payload.address)
        elem = self.driver.find_element_by_name(self.inbound_city_locator).send_keys(payload.city)
        elem = self.driver.find_element_by_class_name(self.state_dropdown_locator)
        self.select_option(payload.state, elem)
        elem = self.driver.find_element_by_name(self.zip_code1_locator).send_keys(payload.zipcode)
        elem = self.driver.find_element_by_name(self.inbound_phone_area_code_locator).send_keys(str(payload.area_code))
        elem = self.driver.find_element_by_name(self.inbound_phone_prefix_locator).send_keys(str(payload.prefix))
        elem = self.driver.find_element_by_name(self.inbound_phone_last_digits_locator).send_keys(str(payload.last))
        elem = self.driver.find_element_by_class_name(self.billing_info_email1_locator).click()
        elem = self.driver.find_element_by_class_name(self.billing_info_email2_locator).click()
        time.sleep(2)
        elem = self.driver.find_element_by_xpath(self.inbound_same_information_locator).click()
        elem = self.driver.find_element_by_class_name(self.same_email_locator).click()
        elem = self.driver.find_element_by_id(self.save_continue_inbound_brand_page_locator).click()
        time.sleep(2)

    # SUMMARY:
    def inbound_Summary(self):
        elem = self.driver.find_element_by_id(self.disclosure_locator).click()


           ## ALL DISCLOSURES PER STATE:

    # DISClOSURES

    # Disclosure for EP
    def disclosure_activity_Inbound(self, payload):
        self.disclosure_toggle()
        self.disclosure_PA1(payload)
        self.disclosure_IL1(payload)
        self.disclosure_MD1(payload)
        self.disclosure_MA1(payload)
        self.disclosure_NJ1(payload)
        self.disclosure_OH1(payload)

    def disclosure_activity_Inbound_new(self, payload):
        self.disclosure_toggle()
        self.disclosure_PA1_new(payload)

    #Disclosure for GM Electric:
    def GM_elec_disclosure_activity(self,payload):
        self.disclosure_toggle()
        self.disclosure_IL1(payload)
        self.disclosure_MD1(payload)
        self.disclosure_MA(payload)
        self.disclosure_NJ1(payload)
        self.disclosure_OH1(payload)
        self.disclosure_PA(payload)
        self.disclosure_DC(payload)
        self.disclosure_NY(payload)


    ## Disclosure for NRG_regression Electric
    def nrg_elec_disclosure_activity(self, payload):
        self.disclosure_toggle()
        self.disclosure_IL(payload)
        self.disclosure_MD1(payload)
        self.disclosure_MA(payload)
        self.disclosure_NJ1(payload)
        self.disclosure_OH1(payload)
        self.disclosure_PA(payload)
        self.disclosure_DC(payload)
        self.disclosure_NY(payload)

    def disclosure_toggle(self):
        elem = self.driver.find_element_by_id(self.disclosures_yes_verify_accnumber_billingadd_locator).click()
        time.sleep(2) #Need to add time.sleep here as selenium is very quick and it finds the toggle_2_no_loc element even though the toggle_1_no_loc is clicked and is still loading
        elem = self.driver.find_element_by_id(self.disclosure_yes_authorization_pause_for_response_locator).click()


    def disclosure_IL(self, payload):
        if self.driver.current_url == payload.state_url:
            elem = self.driver.find_element_by_id(self.disclosure_yes_note_to_tsr_locator).click()
            elem = self.driver.find_element_by_id(self.dislosure_yes_accept_terms_as_read_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_no_tpv_answer_any_questions_locator).click()


    def disclosure_IL1(self, payload):
        if self.driver.current_url == payload.state_url:
            elem = self.driver.find_element_by_id(self.disclosure_yes_note_to_tsr_locator).click()
            elem = self.driver.find_element_by_id(self.dislosure_yes_accept_terms_as_read_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_tpv_answer_any_questions_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_no_continue_enrollment_locator).click()


    def disclosure_MD1(self, payload):
        if self.driver.current_url == payload.state_url:
            elem = self.driver.find_element_by_id(self.disclosure_yes_note_to_tsr_locator).click()
            elem = self.driver.find_element_by_id(self.dislosure_yes_accept_terms_as_read_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_no_tpv_answer_any_questions_locator).click()

    def disclosure_MA1(self, payload):
        if self.driver.current_url == payload.state_url:
            elem = self.driver.find_element_by_id(self.disclosure_yes_note_to_tsr_locator).click()
            elem = self.driver.find_element_by_id(self.dislosure_yes_accept_terms_as_read_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_tpv_answer_any_questions_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_no_continue_enrollment_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_anything_icando_today_locator).click()
            elem = self.driver.find_element_by_id(self.tpv_btn_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_ma_locator).click()
            elem = self.driver.find_element_by_id("toggle_10_yes").click()


    def disclosure_MA(self, payload):
        if self.driver.current_url == payload.state_url:
            elem = self.driver.find_element_by_id(self.disclosure_yes_note_to_tsr_locator).click()
            elem = self.driver.find_element_by_id(self.dislosure_yes_accept_terms_as_read_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_tpv_answer_any_questions_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_continue_enrollment_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_transfer_tpv_locator).click()
            elem = self.driver.find_element_by_id(self.tpv_btn_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_anything_icando_today_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_no_ma_locator).click()



    def disclosure_NJ1(self, payload):
        if self.driver.current_url == payload.state_url:
            elem = self.driver.find_element_by_id(self.disclosure_yes_note_to_tsr_locator).click()
            elem = self.driver.find_element_by_id(self.dislosure_yes_accept_terms_as_read_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_no_tpv_answer_any_questions_locator).click()


    def disclosure_OH1(self, payload):
        if self.driver.current_url == payload.state_url:
            elem = self.driver.find_element_by_id(self.disclosure_yes_note_to_tsr_locator).click()
            elem = self.driver.find_element_by_id(self.dislosure_yes_accept_terms_as_read_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_tpv_answer_any_questions_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_continue_enrollment_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_no_transfer_tpv_locator).click()


    def disclosure_PA(self, payload):
        if "PA" == payload.state_disclosure:
            elem = self.driver.find_element_by_id(self.disclosure_yes_note_to_tsr_locator).click()
            elem = self.driver.find_element_by_id(self.dislosure_yes_accept_terms_as_read_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_tpv_answer_any_questions_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_continue_enrollment_locator).click()
            elem = self.driver.find_element_by_id(self.tpv_btn_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_transfer_tpv_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_no_anything_icando_today_locator).click()



    def disclosure_PA1(self,payload):
        if "PA" == payload.state_disclosure:
            elem = self.driver.find_element_by_id(self.disclosure_yes_note_to_tsr_locator).click()
            elem = self.driver.find_element_by_id(self.dislosure_yes_accept_terms_as_read_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_no_tpv_answer_any_questions_locator).click()
            elem = self.driver.find_element_by_id(self.tpv_btn_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_continue_enrollment_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_no_transfer_tpv_locator).click()

    def disclosure_PA1_new(self,payload):
        elem = self.driver.find_element_by_id(self.disclosure_yes_note_to_tsr_locator).click()
        elem = self.driver.find_element_by_id(self.dislosure_yes_accept_terms_as_read_locator).click()
        elem = self.driver.find_element_by_id(self.disclosure_no_tpv_answer_any_questions_locator).click()
        elem = self.driver.find_element_by_id(self.tpv_btn_locator).click()
        elem = self.driver.find_element_by_id(self.disclosure_yes_continue_enrollment_locator).click()
        elem = self.driver.find_element_by_id(self.disclosure_no_transfer_tpv_locator).click()



    def disclosure_NY(self, payload):
        if self.driver.current_url == payload.state_url:
            elem = self.driver.find_element_by_id(self.disclosure_yes_note_to_tsr_locator).click()
            elem = self.driver.find_element_by_id(self.dislosure_yes_accept_terms_as_read_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_no_tpv_answer_any_questions_locator).click()
            elem = self.driver.find_element_by_id(self.tpv_btn_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_continue_enrollment_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_no_transfer_tpv_locator).click()


    def disclosure_DC(self, payload):
        if self.driver.current_url == payload.state_url:
            elem = self.driver.find_element_by_id(self.disclosure_yes_note_to_tsr_locator).click()
            elem = self.driver.find_element_by_id(self.dislosure_yes_accept_terms_as_read_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_tpv_answer_any_questions_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_yes_continue_enrollment_locator).click()
            elem = self.driver.find_element_by_id(self.disclosure_no_transfer_tpv_locator).click()


    # SUBMIT DATA- INBOUND

    def submitEnrollData(self):
        elem = self.driver.find_element_by_id(self.submit_enroll_locator).click()


                                 #PAPER


    # LOADING INBOUND-PAPER URL
    def load_url(self,payload):
        self.driver.get("http://www.pt.energypluscompany.com/myinbound/paper.php")
        time.sleep(2)
        self.driver.find_element_by_id(payload.brand).click()
        time.sleep(3)

    # CUSTOMER INFORMATION
    def fill_cust_info(self,payload):
        elem = self.driver.find_element_by_name(self.fname_locator).send_keys(payload.first_name)
        elem = self.driver.find_element_by_name(self.lname_locator).send_keys(payload.last_name)
        elem = self.driver.find_element_by_name(self.addr1_locator).send_keys(payload.address)
        elem = self.driver.find_element_by_name(self.city_locator).send_keys(payload.city)
        elem = self.driver.find_element_by_name(self.state_locator)
        self.select_option(payload.state,elem)
        elem = self.driver.find_element_by_name(self.zip5_locator).send_keys(payload.zipcode)
        elem = self.driver.find_element_by_name(self.area_code_locator).send_keys(str(payload.area_code))
        elem = self.driver.find_element_by_name(self.prefix_locator).send_keys(str(payload.prefix))
        elem = self.driver.find_element_by_name(self.line_num_locator).clear()
        elem = self.driver.find_element_by_name(self.line_num_locator).send_keys(str(payload.last))

    # SELECT ACCOUNT TYPE: RESIDENTIAL/BUSINESS
    def select_acct_type(self, acct_type):
        elem = self.driver.find_element_by_name(self.account_type_locator)
        self.select_option(acct_type,elem)


    # FILL BUSINESS INFORMATION
    def fill_business_info(self, payload):
        if self.driver.find_element_by_name(self.business_name_locator).is_displayed():
            time.sleep(1)
            elem = self.driver.find_element_by_name(self.business_name_locator).send_keys(payload.business_name)
            time.sleep(1)


    # BILLING INFORMATION- GAS
    def fill_billing_info_gas(self, payload):
        elem = self.driver.find_element_by_name(self.copy_information_locator).click()
        elem = self.driver.find_element_by_name(self.email_locator).send_keys(payload.email)
        if self.driver.find_element_by_id(self.commodity_gas_locator).is_displayed():
            elem = self.driver.find_element_by_id(self.commodity_gas_locator).click()

    # BILLING INFORMATION- ELECTRIC
    def fill_billing_info_electric(self,payload):
        elem = self.driver.find_element_by_name(self.copy_information_locator).click()
        elem = self.driver.find_element_by_name(self.email_locator).send_keys(payload.email)
        if self.driver.find_element_by_name(self.egr_commodity_electric_locator).is_displayed():
            elem = self.driver.find_element_by_name(self.egr_commodity_electric_locator).click()

    # BILLING INFORMATION GM ELECTRIC
    def fill_billing_info_GM_electric(self,payload):
        elem = self.driver.find_element_by_name(self.copy_information_locator).click()
        elem = self.driver.find_element_by_name(self.email_locator).send_keys(payload.email)

    # BILLING INFORMATION EP ELECTRIC
    def fill_billing_info_EP_electric(self, payload):
        elem = self.driver.find_element_by_name(self.copy_information_locator).click()
        elem = self.driver.find_element_by_name(self.email_locator).send_keys(payload.email)


    # BILLING INFORMATION EP GAS
    def fill_billing_info_EP_Gas(self,payload):
        elem = self.driver.find_element_by_name(self.copy_information_locator).click()
        elem = self.driver.find_element_by_name(self.email_locator).send_keys(payload.email)


    # FILL GAS INFORMATION
    def fill_gas_info(self,payload):
        elem = self.driver.find_element_by_name(self.gas_utility_locator)
        self.select_option(payload.utility,elem)
        elem = self.driver.find_element_by_name(self.gas_account_num_locator).send_keys(str(payload.account_number))


    # FILL ELECTRIC INFORMATION
    def fill_electric_info(self,payload):
        elem = self.driver.find_element_by_name(self.electric_utility_locator)
        self.select_option(payload.utility, elem)
        elem = self.driver.find_element_by_name(self.electric_account_number_locator).send_keys(payload.account_number)
        if self.driver.find_element_by_name(self.electric_account_number2_locator).is_displayed():
            element = self.driver.find_element_by_name(self.electric_account_number2_locator).send_keys(payload.service_ref)


    # GM Electric
    def fill_GM_electric_info(self,payload):
        elem = self.driver.find_element_by_name(self.electric_utility_locator)
        self.select_option(payload.utility, elem)
        elem = self.driver.find_element_by_name(self.electric_account_number_locator).send_keys(str(payload.account_number))
        if self.driver.find_element_by_name(self.electric_account_number2_locator).is_displayed():
            element = self.driver.find_element_by_name(self.electric_account_number2_locator).send_keys(str(payload.service_ref))
        if self.driver.find_element_by_name(self.coned_zone_locator).is_displayed():
            element = self.driver.find_element_by_name(self.coned_zone_locator).click()
        if self.driver.find_element_by_name(self.spanishbill_locator).is_displayed():
            elememt = self.driver.find_element_by_name(self.spanishbill_locator).click()

    # EP Electric
    def fill_EP_electric_info(self, payload):
        elem = self.driver.find_element_by_name(self.electric_utility_locator)
        self.select_option(payload.utility, elem)
        elem = self.driver.find_element_by_name(self.electric_account_number_locator).send_keys(str(payload.account_number))
        if self.driver.find_element_by_name(self.electric_account_number2_locator).is_displayed():
            element = self.driver.find_element_by_name(self.electric_account_number2_locator).send_keys(str(payload.service_ref))
        elem = self.driver.find_element_by_name(self.electric_green_locator).click()


    # Order Information gas
    def fill_order_info_gas(self, payload):
        elem = self.driver.find_element_by_name(self.offertypes_gas_locator)
        self.select_option("Offer Code",elem)
        elem = self.driver.find_element_by_name(self.partnercodegas_locator).send_keys(payload.partner)
        elem = self.driver.find_element_by_name(self.campaign_codegas_locator).send_keys(payload.campaign)
        if self.driver.find_element_by_name(self.promo_codegas_locator).is_displayed():
            elem = self.driver.find_element_by_name(self.promo_codegas_locator).send_keys(payload.promo)
        time.sleep(4)


    # Order Information EP Gas
    def fill_order_info_EP_Gas(self,payload):
        elem = self.driver.find_element_by_name(self.partner_code_epgas_locator).send_keys(payload.partner)
        elem = self.driver.find_element_by_name(self.campaign_code_epgas_locator).send_keys(payload.campaign)
        elem = self.driver.find_element_by_name(self.promo_code_epgas_locator).send_keys(payload.promo)
        time.sleep(4)


    # Order Information electric only
    def fill_order_info_electric(self,payload):
        elem = self.driver.find_element_by_name(self.offer_types_electric_locator)
        self.select_option("Offer Code", elem)
        elem = self.driver.find_element_by_name(self.partner_code_locator).send_keys(payload.partner)
        elem = self.driver.find_element_by_name(self.campaign_code_offer_locator).send_keys(payload.campaign)
        if self.driver.find_element_by_name(self.promo_code_locator).is_displayed():
            elem = self.driver.find_element_by_name(self.promo_code_locator).send_keys(payload.promo)
        time.sleep(4)


    # Order Information EP electric
    def fill_order_info_EP_electric(self, payload):
        elem = self.driver.find_element_by_name(self.partner_code_locator).send_keys(payload.partner)
        elem = self.driver.find_element_by_name(self.campaign_code_locator).send_keys(payload.campaign)
        if self.driver.find_element_by_name(self.promo_code_locator).is_displayed():
            elem = self.driver.find_element_by_name(self.promo_code_locator).send_keys(payload.promo)
        else:
            elem=self.driver.find_element_by_name(self.elec_promo_code_locator).send_keys(payload.promo)
        time.sleep(4)


    # Order Information GM Electric
    def fill_order_info_GM_electric(self,payload):
        time.sleep(4)
        elem = self.driver.find_element_by_name(self.electric_products_gme_locator)
        self.select_option(payload.product, elem)


    # Vendor ID
    def fill_vendor_info(self,payload):
        elem = self.driver.find_element_by_name(self.vendor_id_locator)
        self.select_option("EPIB",elem)


    def getConfirmCode(self):
        elem = self.driver.find_element_by_id(self.conf_code_locator)
        confCode = elem.text
        return confCode


    def submitData(self):
        elem = self.driver.find_element_by_name(self.submit_locator).click()


    def ep_nj_check_offer(self):
        if "We're sorry, this offer has expired." in self.driver.page_source:
            elem = self.driver.find_element_by_link_text("click here")
            elem.click()
        if "There is a problem" in self.driver.page_source:
            elem = self.driver.find_element_by_link_text("Continue to this website (not recommended).")
            elem.click()

    def ep_nj_landing_page(self,payload):
        # Landing Page
        elem = self.driver.find_element_by_id(self.show_price_table_locator).click()
        time.sleep(2)
        element = self.driver.find_element_by_xpath(payload.xpath)
        assert element.text == payload.price