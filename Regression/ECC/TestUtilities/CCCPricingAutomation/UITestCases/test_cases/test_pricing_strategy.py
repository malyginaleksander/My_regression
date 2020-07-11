import pytest
from datetime import datetime as dt


@pytest.mark.usefixtures("setup")
class TestCreateAndEditStrategies:
    url = 'https://ccc.pt.nrgpl.us/admin/pricing/pricingstrategy/'

    def test_create_margin_with_hold(self):
        url = self.url
        driver = self.driver
        driver.get(url)

        # Add a new strategy with a given margin and HOLD checked:
        # Finding elements
        add_pricing_strategy_button = driver.find_element_by_partial_link_text('ADD PRICING')
        add_pricing_strategy_button.click()
        pricing_strategy_name = driver.find_element_by_id('id_name')
        margin = driver.find_element_by_id('id_margin')
        ramp_up_percentage = driver.find_element_by_id('id_ramp_up')
        ramp_down_percentage = driver.find_element_by_id('id_ramp_down')
        hold = driver.find_element_by_id('id_hold')

        # Sending Input
        test_name = "Test Strategy:" + str(dt.now()).replace(' ', '')
        pricing_strategy_name.send_keys(test_name)
        margin.send_keys('1')
        ramp_up_percentage.send_keys('1')
        ramp_down_percentage.send_keys('1')
        hold.click()

        # Save and check
        driver.find_element_by_name('_save').click()
        assert driver.find_element_by_link_text(test_name)

    def test_create_margin_without_hold(self):
        url = self.url
        driver = self.driver
        driver.get(url)

        # Add a new strategy with a given margin and HOLD checked:
        # Finding elements
        add_pricing_strategy_button = driver.find_element_by_partial_link_text('ADD PRICING')
        add_pricing_strategy_button.click()
        pricing_strategy_name = driver.find_element_by_id('id_name')
        margin = driver.find_element_by_id('id_margin')
        ramp_up_percentage = driver.find_element_by_id('id_ramp_up')
        ramp_down_percentage = driver.find_element_by_id('id_ramp_down')
        # Sending Input
        test_name = "Test Strategy:" + str(dt.now()).replace(' ', '')
        pricing_strategy_name.send_keys(test_name)
        margin.send_keys('1')
        ramp_up_percentage.send_keys('1')
        ramp_down_percentage.send_keys('1')

        # Save and check
        driver.find_element_by_name('_save').click()
        assert driver.find_element_by_link_text(test_name)

    def test_create_target_rate_with_hold(self):
        url = self.url
        driver = self.driver
        driver.get(url)

        # Add a new strategy with a given margin and HOLD checked:
        # Finding elements
        add_pricing_strategy_button = driver.find_element_by_partial_link_text('ADD PRICING')
        add_pricing_strategy_button.click()
        pricing_strategy_name = driver.find_element_by_id('id_name')
        target_rate = driver.find_element_by_id('id_target_rate')
        ramp_up_percentage = driver.find_element_by_id('id_ramp_up')
        ramp_down_percentage = driver.find_element_by_id('id_ramp_down')
        hold = driver.find_element_by_id('id_hold')
        # Sending Input
        test_name = "Test Strategy:" + str(dt.now()).replace(' ', '')
        pricing_strategy_name.send_keys(test_name)
        target_rate.send_keys('1')
        ramp_up_percentage.send_keys('1')
        ramp_down_percentage.send_keys('1')
        hold.click()

        # Save and check
        driver.find_element_by_name('_save').click()
        assert driver.find_element_by_link_text(test_name)

    def test_create_target_rate_without_hold(self):
        url = self.url
        driver = self.driver
        driver.get(url)

        # Add a new strategy with a given margin and HOLD checked:
        # Finding elements
        add_pricing_strategy_button = driver.find_element_by_partial_link_text('ADD PRICING')
        add_pricing_strategy_button.click()
        pricing_strategy_name = driver.find_element_by_id('id_name')
        target_rate = driver.find_element_by_id('id_target_rate')
        ramp_up_percentage = driver.find_element_by_id('id_ramp_up')
        ramp_down_percentage = driver.find_element_by_id('id_ramp_down')
        # Sending Input
        test_name = "Test Strategy:" + str(dt.now()).replace(' ', '')
        pricing_strategy_name.send_keys(test_name)
        target_rate.send_keys('1')
        ramp_up_percentage.send_keys('1')
        ramp_down_percentage.send_keys('1')

        # Save and check
        driver.find_element_by_name('_save').click()
        assert driver.find_element_by_link_text(test_name)

    def test_edit_existing_strategy(self):
        url = self.url
        driver = self.driver
        driver.get(url)

        # Find Existing Strategy
        strategy = driver.find_element_by_partial_link_text('Test Strategy:')
        strategy.click()

        # Enter data
        margin = driver.find_element_by_id('id_margin')
        ramp_up_percentage = driver.find_element_by_id('id_ramp_up')
        ramp_down_percentage = driver.find_element_by_id('id_ramp_down')
        hold = driver.find_element_by_id('id_hold')

        # Sending Input
        margin.clear()
        ramp_up_percentage.clear()
        ramp_down_percentage.clear()
        margin.send_keys('1')
        ramp_up_percentage.send_keys('1')
        ramp_down_percentage.send_keys('1')
        hold.click()

        # Save and check
        driver.find_element_by_name('_save').click()
