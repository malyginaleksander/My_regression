from __future__ import print_function

import os

import pytest
import time
from selenium import webdriver

import config

@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('USE_PHANTOM'):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
    else:
        print("making Firefox driver")
        _driver = webdriver.Firefox()
    _driver.implicitly_wait(5)
    _driver.set_window_size(1120, 550)

    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            _driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver


@pytest.mark.skipif('os.environ.get("HUDSON_URL")=="http://ci.nrgpl.us:8080/"')
def test_login(driver):
    print('testing login')
    # span.pull-right

    driver.get(config.INBOUND_LOGIN_URL)

    # login
    elem = driver.find_element_by_name("email").send_keys(config.INBOUND_LOGIN_EMAIL)
    elem = driver.find_element_by_name("password").send_keys(config.INBOUND_LOGIN_PASSWORD)
    elem = driver.find_element_by_id("button").click()

    for loop in range(10):
        print(driver.current_url)
        if driver.current_url == 'http://www.pt.energypluscompany.com/myinbound/tab_brand.php':
            break
        else:
            print('waiting')
            time.sleep(2)

    try:
        assert driver.current_url == \
               'http://www.pt.energypluscompany.com/myinbound/tab_brand.php'
        # look for login name
        elem = driver.find_element_by_css_selector('span.pull-right')

        assert elem.text == "Michael Peters"
        print('passing')
        driver.save_screenshot('./failed/inbound_login_success.png')
    except AssertionError:
        print('failing! saving screenshot in /tmp/inbound_regression.png')
        driver.save_screenshot('./failed/inbound_login_fail.png')
        raise
