
def choose_brand(payload, driver):
    if payload.brand == 'EP':
        driver.find_element_by_id("brandId_1").click()
    elif payload.brand == 'NRG':
        driver.find_element_by_id("brandId_2").click()
    elif payload.brand == 'GME':
        driver.find_element_by_id("brandId_5").click()
    elif payload.brand == 'Cirro':
        driver.find_element_by_id("brandId_6").click()
    driver.find_element_by_id('btn_continue').click()