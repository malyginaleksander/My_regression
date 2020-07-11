from selenium.webdriver.support.ui import Select
import pytest


@pytest.mark.usefixtures("setup")
class TestCreateAndEditSegmentStrategyMapping():
    url = 'https://ccc.pt.nrgpl.us/admin/pricing/segmentstrategymapping/'

    def test_create_segment_strategy(self):
        url = self.url
        driver = self.driver
        driver.get(url)

        # Add a new strategy with a given margin and HOLD checked:
        # Add segment strategy mapping
        driver.find_element_by_partial_link_text('ADD SEGMENT').click()
        segment_name = driver.find_element_by_id('id_segment_name')
        strategy_name = Select(driver.find_element_by_id('id_strategy_name'))
        brand_name = Select(driver.find_element_by_id('id_brand'))

        # Sending Input
        segment_name.send_keys('Test Strategy')
        strategy_name.select_by_visible_text('Default nrg_residential peco')
        brand_name.select_by_visible_text('NRG_regression Home')

        # # Save and check
        save_button = driver.find_element_by_name('_save')
        save_button.click()
        assert driver.find_element_by_link_text('Test Strategy')

    def test_edit_segment_strategy(self):
        url = self.url
        driver = self.driver
        driver.get(url)
        # Select the "test strategy" filter which will only load one result: test strategy
        # Then select by xpath
        driver.find_element_by_partial_link_text('Test Strategy').click()
        driver.find_element_by_xpath('//*[@id="result_list"]/tbody/tr/th/a').click()
        segment_name = driver.find_element_by_id('id_segment_name')
        strategy_name = Select(driver.find_element_by_id('id_strategy_name'))
        brand_name = Select(driver.find_element_by_id('id_brand'))

        # Sending Input
        segment_name.clear()
        segment_name.send_keys('Test Strategy')
        strategy_name.select_by_visible_text('Default nrg_residential peco')
        brand_name.select_by_visible_text('NRG_regression Home')

        # Save and check, then delete
        driver.find_element_by_name('_save').click()
        existing_strategy = driver.find_element_by_partial_link_text('Test Strategy')
        existing_strategy.click()
        driver.find_element_by_link_text('Delete').click()
        self.driver.find_element_by_xpath("//input[@type='submit']").click()
