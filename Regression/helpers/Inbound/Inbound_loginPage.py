
def fill_login(driver, login_email_data, login_password_data ):
    driver.find_element_by_name("email").send_keys(login_email_data)
    driver.find_element_by_name( "password").send_keys(login_password_data)
    driver.find_element_by_id("button").click()