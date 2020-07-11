import pytest
from datetime import datetime as dt


@pytest.mark.usefixtures("setup")
class TestCreateAndEditUtilityBaseRate():
    url = 'https://ccc.pt.nrgpl.us/admin/pricing/utilitybaserate/'

    def test_create_utility_base_rate(self):
        url = self.url
        driver = self.driver
        driver.get(url)

        # Add a new strategy with a given margin and HOLD checked:
        # Finding elements
        add_utility_base_rate = driver.find_element_by_partial_link_text('ADD UTILITY')
        add_utility_base_rate.click()
        brand_slug = driver.find_element_by_id('id_brand_slug')
        utility_slug = driver.find_element_by_id('id_utility_slug')
        zone = driver.find_element_by_id('id_zone')
        base_rate = driver.find_element_by_id('id_base_rate')

        # Sending Input
        test_name = "Test Value:" + str(dt.now()).replace(' ', '_')
        brand_slug.send_keys(test_name)
        utility_slug.send_keys(test_name)
        zone.send_keys('test_zone')
        base_rate.send_keys('1')

        # Save
        save_button = driver.find_element_by_name('_save')
        save_button.click()

    def test_edit_utility_base_rate(self):
        url = self.url
        driver = self.driver
        driver.get(url)

        # Select the most recent Rate (highest Id #)
        try:
            driver.find_element_by_xpath('//*[@id="result_list"]/tbody/tr[1]/th/a').click()
        except Exception as e:
            print("Failed X path: ", e)
            # Get a list of the ID links on the screen, find the largest (most recent), and click its associated object
            id_link_elements = driver.find_elements_by_class_name('field-id')
            id_link_dict = {link.text: link for link in list(id_link_elements)}
            most_recent_id = max([int(key) for key in id_link_dict.keys()])
            id_link_dict[str(most_recent_id)].click()

        # Finding and clearing elements
        brand_slug = driver.find_element_by_id('id_brand_slug')
        # Make sure the link clicked was a test strategy
        assert'Test Value' in brand_slug.get_attribute('value')
        utility_slug = driver.find_element_by_id('id_utility_slug')
        zone = driver.find_element_by_id('id_zone')
        base_rate = driver.find_element_by_id('id_base_rate')

        # Sending Input
        brand_slug.clear()
        utility_slug.clear()
        zone.clear()
        base_rate.clear()
        test_name = "Test Value-Edited:" + str(dt.now()).replace(' ', '_')
        brand_slug.send_keys(test_name)
        utility_slug.send_keys(test_name)
        zone.send_keys('test_zone')
        base_rate.send_keys('1')

        # Save
        save_button = driver.find_element_by_name('_save')
        save_button.click()
