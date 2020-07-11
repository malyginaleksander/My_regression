import time

from Regression.sprint_regression.Inbound_regression.Inbound_Enrollments_regression.Inbound_pages_methods import \
    wait_get_started_page_state_list


def fill_GetStartedPage(payload, driver, firstname, lastname, utility,utility_2 ):
    driver.find_element_by_id('caller-first-name').send_keys(firstname)
    driver.find_element_by_id('caller-last-name').send_keys(lastname)
    wait_get_started_page_state_list(driver)
    # What state are you are calling from?
    elem = driver.find_element_by_name('state-list')
    for option in elem.find_elements_by_tag_name('option'):
        if option.text == payload.state:
            option.click()
    # Is Your Name on the Utility Bill?
    if payload.state == "Maryland":
        # Is Your Name on the Utility Bill?
        try:
            driver.find_element_by_xpath("//div[@id='new-account-name_on_bill']/div/div/label/input").click()
        except:
            pass
    # What account are you calling about today? - gas or electric
    try:
        if payload.account_type_1.lower() == 'electric':
            driver.find_element_by_class_name('commodity-choice-electric').click()
        elif payload.account_type_1.lower() == 'gas':
            driver.find_element_by_class_name('commodity-choice-gas').click()
    except:
        pass




    # Who is the provider for your electric account?
    if payload.account_type_1.lower() == 'electric':
        elem = driver.find_element_by_name('utility-list')
        for option in elem.find_elements_by_tag_name('option'):
            a=option.text
            if option.text == utility:
                option.click()
    if payload.account_type_1.lower() == 'gas':
        try:
            elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[6]/div[4]/select')
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == utility:
                    option.click()
        except:
            elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[6]/div[3]/select')
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == utility:
                    option.click()
    # Is this electric account a residential or business address?try:
    try:
        if payload.type == 'Residential':
            driver.find_element_by_class_name('account-type-residential').click()
        elif payload.type == 'Business':
            driver.find_element_by_class_name('account-type-business').click()
    except:
        pass

    ##2 accounts test:
    if payload.account_type_2.lower() == "electric" or payload.account_type_2.lower() == "gas":

        driver.find_element_by_id('add-account-button').click()
        time.sleep(1)
        # if payload.account_type_2 == "Gas":
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/div[1]/div[7]/div[1]/select")  # second state
        for option in elem.find_elements_by_tag_name('option'):
            if option.text == payload.state:
                option.click()
        time.sleep(1)
        if payload.account_type_2.lower() == "gas":
            driver.find_element_by_xpath(
                "/html/body/div[2]/div/div[1]/div[7]/div[2]/div[2]/label/input").click()  # choose second_gas
        elem = driver.find_element_by_xpath(
            "/html/body/div[2]/div/div[1]/div[7]/div[3]/select")  # choose second utility
        a = utility_2

        for option in elem.find_elements_by_tag_name('option'):
            if option.text == utility_2 :
                option.click()

    if payload.type == "Residential":
        Residentials_buttons = driver.find_elements_by_class_name('account-type-residential')
        for x in range(0, len(Residentials_buttons)):
            if Residentials_buttons[x].is_displayed():
                Residentials_buttons[x].click()

    if payload.type == "Business":
        Business_buttons = driver.find_elements_by_class_name('account-type-business')
        for x in range(0, len(Business_buttons)):
            if Business_buttons[x].is_displayed():
                Business_buttons[x].click()

    if payload.account_type_1.lower() == "gas" or payload.account_type_2.lower() == "gas":
        if payload.gas_option == 'Heating Only':
            heating_buttons = driver.find_elements_by_class_name('account-usage-heating')
            for x in range(0, len(heating_buttons)):
                if heating_buttons[x].is_displayed():
                    heating_buttons[x].click()
        if payload.gas_option == 'Cooking Only':
            cooking_buttons = driver.find_elements_by_class_name('account-usage-cooking')
            for x in range(0, len(cooking_buttons)):
                if cooking_buttons[x].is_displayed():
                    cooking_buttons[x].click()
        if payload.gas_option == 'Both Heating & Cooking':
            both_buttons = driver.find_elements_by_class_name('account-usage-both')
            for x in range(0, len(both_buttons)):
                if both_buttons[x].is_displayed():
                    both_buttons[x].click()

    if payload.brand == 'GME' and payload.state == 'New York':
        try:
            elem = driver.find_element_by_name("zone")
            for option in elem.find_elements_by_tag_name('option'):
                if option.text == ("Westchester"):
                    option.click()
        except:
            pass
    driver.find_element_by_id('save-and-continue').click()