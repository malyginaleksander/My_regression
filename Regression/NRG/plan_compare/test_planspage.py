from __future__ import print_function
import unittest
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui
import time
import json
import os
import sys
from selenium.webdriver.common.by import By
import urllib
import socket
import requests
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import xlrd
import pytest
from collections import namedtuple

Payload = namedtuple('payload', ['tc','url'])

zipcode = [
    ['tc-01','http://www.pt.nrghomepower.com/pa'],
]

zipcode_data = [
    Payload(tc = current_row[0],
            url = current_row[1],
            )
    for current_row in zipcode
]

@pytest.fixture(scope='module')
def driver(request):
    print('driver_setup()')
    if os.environ.get('USE_PHANTOM'):
        print("making PhantomJS driver")

        _driver = webdriver.PhantomJS()
        _driver.implicitly_wait(5)
        _driver.set_window_size(1120, 550)
    else:
        print("making Firefox driver")
        _driver = webdriver.Firefox()

    def resource_a_teardown():
        print('driver_setup teardown()')
        if _driver:
            print(_driver.current_url)
            _driver.close()
        else:
            assert False, "can't close driver"

    request.addfinalizer(resource_a_teardown)
    return _driver

@pytest.mark.parametrize("payload", zipcode_data, ids=[
    p.tc.lower() for p in zipcode_data
])
def test_plans_page_format(driver, payload):
    print(payload.tc, 'NRG_regression Plans utility selection')

    driver.get(payload.url)
    driver.maximize_window()

    main_window = driver.current_window_handle
    print(main_window)
    driver.find_element_by_xpath(".//*[@id='global-upper-nav']/div/ul/li[1]/a").click()
    utility_select = driver.find_element_by_id("plan-utility-header")
    zipcode_box = driver.find_element_by_id("plan-zipcode-header")
    utility_select.click()
    peco = driver.find_element_by_xpath(".//*[@id='plan-utility-header']/div[1]/div/div/a[3]")
    peco.click()
    utility_name = driver.find_element_by_xpath(".//*[@id='utility-message']/span").text
    assert utility_name == 'PECO'

    # Fixed, variable selection with plan count
    plan_count_org = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[4]/span/span").text
    fixed_box = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[4]/div[1]/label[1]")
    variable_box = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[4]/div[1]/label[2]")

    fixed_box.click()
    term_in_product = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[5]/div[1]/div[1]/div[1]/div[1]/span[1]").text
    assert term_in_product.strip() == '3 months variable'

    fixed_box.click()
    variable_box.click()
    term_in_product = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[5]/div[1]/div[1]/div[1]/div[1]/span[1]").text
    assert term_in_product.strip() != '6 months variable'


    new_plan_count = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[4]/span/span").text

    assert int(new_plan_count) != 0
    assert (int(plan_count_org)) > (int(new_plan_count))
    driver.refresh()

    term_length_filter = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[4]/div[2]/a").click()
    driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[4]/div[2]/div/a[2]").click()

    new_plan_count = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[4]/span/span").text
    assert (int(plan_count_org)) > (int(new_plan_count))
    variable_box= driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[4]/div[1]/label[2]").click()
    new_plan_count = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[4]/span/span").text
    assert int(new_plan_count) == 0
    driver.refresh()

    # all term type exists
    term_length_filter = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[4]/div[2]/a").click()
    six_month = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[4]/div[2]/div/a[3]").text

    assert six_month.strip() == '6 Months'
    twelve_month = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[4]/div[2]/div/a[4]").text
    assert twelve_month.strip() == '12 Months'
    # fifteen_month = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[3]/div[2]/div/div/a[5]").text
    # assert fifteen_month.strip() == '15 months'
    three_month = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[4]/div[2]/div/a[2]").text
    assert three_month.strip() == '3 Months'

    # zip cpde box exists
    zipcode_box = driver.find_element_by_id("plan-zipcode-header").is_displayed
    # utility selection exists
    utility_select = driver.find_element_by_id("plan-utility-header").is_displayed

    utility_select_plan = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[5]/div[1]/div[1]/div[2]/div/div/div/a")
    utility_select_plan.click()
    driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[5]/div[1]/div[1]/div[2]/div/div/div/div/a[1]").click()

    price = driver.find_element_by_class_name("price").text

    quick_compare = driver.find_element_by_id("quick-compare")
    compare_box = driver.find_element_by_class_name("checkbox")


    #Checking quick compare compares the two plans
    quick_compare.click()

    no_of_plan = driver.find_element_by_xpath(".//*[@id='plan-compare-message']/span").text
    assert no_of_plan == '2 plans'

    #Checking benefits is displayed
    benefits = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[7]/div[3]/div[1]/div/div[2]/ul/li[1]")
    benefits.is_displayed\

    # Checking TOS link
    tos = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[7]/div[3]/div[1]/div/div[3]/a[2]")
    tos.click()

    tos_header = driver.find_element_by_xpath(".//*[@id='modal-tos']/div/div[1]/h2").text
    assert tos_header.strip() == 'Terms Of Service'
    driver.find_element_by_xpath(".//*[@id='modal-tos']/div/div[1]/a").click()

    # select gas
    select_electric = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[7]/div[3]/div[1]/div/a/button").click()

    gas_utility_select = driver.find_element_by_xpath(".//*[@id='utility-selected']/div[1]/div[1]/div/div/a")
    gas_utility_select.click()
    driver.find_element_by_xpath(".//*[@id='utility-selected']/div[1]/div[1]/div/div/div/a[1]").click()

    #gas benefits is displayed

    benefits_gas = driver.find_element_by_xpath(".//*[@id='utility-selected']/div[2]/div[1]/div/div[2]/ul/li")

    # select gas

    select_gas_prod = driver.find_element_by_xpath(".//*[@id='utility-selected']/div[2]/div[1]/div/a/button")
    select_gas_prod.click()
    select_diff_gas = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[6]/div[2]/div[1]/div[2]/a[1]")
    remove_plan = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[6]/div[2]/div[1]/div[2]/a[2]")
    select_diff_elec = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[6]/div[2]/div[1]/div[1]/a")
    # checking'remove plan'
    remove_plan.click()
    select_gas_prod = driver.find_element_by_xpath(".//*[@id='utility-selected']/div[2]/div[1]/div/a/button")
    select_gas_prod.click()
    # checking'select a diff gas plan'
    select_diff_gas.click()
    select_gas_prod = driver.find_element_by_xpath(".//*[@id='utility-selected']/div[2]/div[1]/div/a/button")
    select_gas_prod.click()
    # getting to enroll form
    continue_button = driver.find_element_by_xpath(".//*[@id='bg-container']/div[2]/div[6]/div[2]/div[2]/button").click()
