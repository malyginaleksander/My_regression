import time


def fill_billing_info_page(driver, payload, firstname, lastname, address, zipcode_, city, accountNo, email,  phonenumber  ):
    billing_address_name = ' Billing Address'
    billing_city_name = ' City'
    billing_state_class_name = 'state-dropdown'
    billing_zip_name = ' Zip Code'
    billing_phone_area_code_name = ' Phone Area Code'
    billing_phone_prefix_area_name = ' Phone Prefix'
    billing_phone_last_digits_name = ' Phone Last Digits'
    billing_phone_email_no_class_name = 'email-no'
    billing_phone_email_yes_class_name = 'email-yes'
    billing_phone_email_no_2ndAccount_class_xpath = '/html/body/div[2]/div/div[1]/div[1]/div[2]/div[4]/input[2]'
    billing_phone_email_no_no_class_name = 'email-no-no'
    billing_phone_email_no_no_2ndAccount_class_xpath = '/html/body/div[2]/div/div[1]/div[1]/div[2]/div[4]/div/div/div[1]/p[2]/input[2]'
    billing_businessName_radio_yes_xpath = '/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/input[1]'
    billing_businessName_xpath = '/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/input'

    options_tag_name = 'option'
    continue_button_id = 'btn_continue'
    SameAsFirst_button_name = 'same-as-first'


    if payload.PremiseType.lower() == 'business':
        try:
            driver.find_element_by_xpath(billing_businessName_radio_yes_xpath).click()
            driver.find_element_by_xpath(billing_businessName_xpath).send_keys(
                "Tester_busines_account")
        except:
            pass

    driver.find_element_by_name(billing_address_name).send_keys(address)
    driver.find_element_by_name(billing_city_name).send_keys(city)
    elem = driver.find_element_by_class_name(billing_state_class_name)
    for option in elem.find_elements_by_tag_name(options_tag_name):
        if option.text == payload.State:
            option.click()
    try:
        zip = zipcode_("'", '')
    except:
        zip = zipcode_
    if len (zip)<5:
        zip = str("0"+str(zip))

    driver.find_element_by_name(billing_zip_name).send_keys(str(zip))
    driver.find_element_by_name(billing_phone_area_code_name).send_keys(str(phonenumber)[:3])
    driver.find_element_by_name(billing_phone_prefix_area_name).send_keys(str(phonenumber)[3:6])
    driver.find_element_by_name(billing_phone_last_digits_name).send_keys(str(phonenumber)[6:])

    email_no_buttons = driver.find_elements_by_class_name(billing_phone_email_no_class_name)
    for x in range(0, len(email_no_buttons)):
        if email_no_buttons[x].is_displayed():
            email_no_buttons[x].click()

    email_no_buttons = driver.find_elements_by_class_name(billing_phone_email_no_no_class_name)
    for x in range(0, len(email_no_buttons)):
        if email_no_buttons[x].is_displayed():
            email_no_buttons[x].click()

    try:
        if payload.account_type_2.lower() == "electric" or payload.account_type_2.lower() == "gas":
            driver.find_element_by_class_name(SameAsFirst_button_name).click()
    except:
        pass

    driver.find_element_by_id(continue_button_id).click()
    time.sleep(2)