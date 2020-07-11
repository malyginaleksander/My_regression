import pytest
from selenium.webdriver.support.ui import Select
from collections import namedtuple


# Service id must be unique and no more than 7 characters. Utility slug must be unique
PricingWindow = namedtuple('PricingWindow',
                           ['service_id', 'utility_slug', 'window_start', 'bill_period_reference'])
PricingWindow.__new__.__defaults__ = ('test_id', 'test_slug_1', 99, 'BP_START')


@pytest.mark.usefixtures("setup")
class TestAddPricingWindow:
    def test_go_to_main_page(self):
        self.driver.get('https://ccc.pt.nrgpl.us/admin/pricing/utilitypricingwindow/')

    def test_create_with_build_period_start(self):
        target_row = self.can_create_pricing_window('BP_START')
        # Assert row was found
        assert target_row

    def test_create_with_build_period_end(self):
        target_row = self.can_create_pricing_window('BP_END')
        # Assert row was found
        assert target_row

    def can_create_pricing_window(self, bill_period_reference):
        """
        Create a pricing window with the Bill Period Reference set to BP_START
        """
        pricing_window = PricingWindow()
        pricing_window._replace(bill_period_reference=bill_period_reference)
        pricing_window_record = ''.join('{} '.format(val) for val in pricing_window._asdict().values())

        # We're now on the Courtesy Credit Administration page. Begin by removing the test row if it exists.
        # Click on the Add Utility Pricing Window button
        target_row = self.find_target_row(pricing_window)
        if target_row:
            self.remove_target_row(target_row)

        self.driver.find_element_by_partial_link_text('ADD UTILITY PRICING WINDOW').click()

        # We're now on the Courtesy Credit Administration / Add Utility pricing window form page, edit and submit the
        # the form.
        self.edit_pricing_window_form(pricing_window)

        # We should now be back on the Courtesy Credit Administration page. Find the pricing window that we just created
        # and match it's entries to ensure they are as we entered.
        results_table = self.driver.find_element_by_id('result_list')
        results_table_body = results_table.find_element_by_tag_name('tbody')
        rows = results_table_body.find_elements_by_tag_name('tr')

        return next(filter(lambda x: x.text in pricing_window_record,  rows))

    def find_target_row(self, pricing_window):
        """
        Find target row based on the row's service id
        :return: target row if found else None
        """
        results_table = self.driver.find_element_by_id('result_list')
        results_table_body = results_table.find_element_by_tag_name('tbody')
        rows = results_table_body.find_elements_by_tag_name('tr')

        try:
            target_row = next(filter(lambda x: pricing_window.service_id in x.text,  rows))
        except StopIteration:
            # Row not found do nothing
            return None
        else:
            return target_row

    def remove_target_row(self, target_row):
        """
        Remove the test row
        """
        ele_target_id = target_row.find_element_by_class_name('field-service_id')
        ele_target_id.find_element_by_tag_name('a').click()

        # We should now be on the Change utility pricing window form page, click the delete button to delete
        # our test entry. Then click the Yes, I'm sure button the verify this action
        self.driver.find_element_by_link_text('Delete').click()
        self.driver.find_element_by_xpath("//input[@type='submit']").click()

    def edit_pricing_window_form(self, pricing_window):
        # We're now on the Courtesy Credit Administration / Add Utility pricing window form page
        # Get form field elements
        ele_service_id = self.driver.find_element_by_id('id_service_id')
        ele_utility_slug = self.driver.find_element_by_id('id_utility_slug')
        ele_window_start = self.driver.find_element_by_id('id_window_start')
        ele_bill_period_reference = Select(self.driver.find_element_by_id('id_bill_period_reference'))

        # Enter field data
        ele_service_id.clear()
        ele_utility_slug.clear()
        ele_window_start.clear()
        ele_service_id.send_keys(pricing_window.service_id)
        ele_utility_slug.send_keys(pricing_window.utility_slug)
        ele_window_start.send_keys(pricing_window.window_start)
        ele_bill_period_reference.select_by_visible_text(pricing_window.bill_period_reference)

        # Obtain the form save btn element and submit the test entries.
        ele_save_pricing_window_button = \
            self.driver.find_element_by_xpath('//*[@id="utilitypricingwindow_form"]/div/div/input[1]')
        ele_save_pricing_window_button.click()


@pytest.mark.usefixtures("setup")
class TestEditPricingWindow:
    def go_to_main_page(self):
        self.driver.get('https://ccc.pt.nrgpl.us/admin/pricing/utilitypricingwindow/')

    def test_edit_with_build_period_start(self):
        target_row = self.can_edit_pricing_window('BP_START')
        # Assert row was found
        assert target_row

    def can_edit_pricing_window(self, bill_period_reference):
        """
        Edit a pricing window with the Bill Period Reference set to BP_START
        """
        pricing_window = PricingWindow()
        pricing_window._replace(bill_period_reference='BP_START')
        pricing_window_record = ''.join('{} '.format(val) for val in pricing_window._asdict().values())

        # We're now on the Courtesy Credit Administration page. Remove the target row if it exists and Click on
        # the Add Utility Pricing Window button
        target_row = self.find_target_row(pricing_window)
        if target_row:
            self.remove_target_row(target_row)

        self.driver.find_element_by_partial_link_text('ADD UTILITY PRICING WINDOW').click()

        # We're now on the Courtesy Credit Administration / Add Utility pricing window form page. Create an entry
        # to edit. Get for elements.
        self.edit_pricing_window_form(pricing_window)

        # --------------------------------------------------------------------------------------------------
        # We should now be back on the Courtesy Credit Administration page. Find the pricing window that we just created
        # and edit it's entries.
        target_row = self.find_target_row(pricing_window)
        if not target_row:
            print("Could not find test row just created")
            raise

        ele_target_id = target_row.find_element_by_class_name('field-service_id')
        ele_target_id.find_element_by_tag_name('a').click()

        pricing_window = pricing_window._replace(utility_slug='test_slug_2',
                                                 window_start=98,
                                                 bill_period_reference='BP_END')
        pricing_window_record = ''.join('{} '.format(val) for val in pricing_window._asdict().values())
        self.edit_pricing_window_form(pricing_window)

        # We should now be back on the Courtesy Credit Administration page. Find the pricing window that we just created
        # and match it's entries to ensure they are as we entered.
        results_table = self.driver.find_element_by_id('result_list')
        results_table_body = results_table.find_element_by_tag_name('tbody')
        rows = results_table_body.find_elements_by_tag_name('tr')

        target_row = next(filter(lambda x: x.text in pricing_window_record, rows))
        return target_row

    def find_target_row(self, pricing_window):
        """
        Find target row based on the row's service id
        :return: target row if found else None
        """
        results_table = self.driver.find_element_by_id('result_list')
        results_table_body = results_table.find_element_by_tag_name('tbody')
        rows = results_table_body.find_elements_by_tag_name('tr')

        try:
            target_row = next(filter(lambda x: pricing_window.service_id in x.text, rows))
        except StopIteration:
            # Row not found do nothing
            return None
        else:
            return target_row

    def remove_target_row(self, target_row):
        """
        Remove the test row
        """
        ele_target_id = target_row.find_element_by_class_name('field-service_id')
        ele_target_id.find_element_by_tag_name('a').click()

        # We should now be on the Change utility pricing window form page, click the delete button to delete
        # our test entry. Then click the Yes, I'm sure button the verify this action
        self.driver.find_element_by_link_text('Delete').click()
        self.driver.find_element_by_xpath("//input[@type='submit']").click()

    def edit_pricing_window_form(self, pricing_window):
        # We're now on the Courtesy Credit Administration / Add Utility pricing window form page
        # Get form field elements
        ele_service_id = self.driver.find_element_by_id('id_service_id')
        ele_utility_slug = self.driver.find_element_by_id('id_utility_slug')
        ele_window_start = self.driver.find_element_by_id('id_window_start')
        ele_bill_period_reference = Select(self.driver.find_element_by_id('id_bill_period_reference'))

        # Enter field data
        ele_service_id.clear()
        ele_utility_slug.clear()
        ele_window_start.clear()
        ele_service_id.send_keys(pricing_window.service_id)
        ele_utility_slug.send_keys(pricing_window.utility_slug)
        ele_window_start.send_keys(pricing_window.window_start)
        ele_bill_period_reference.select_by_visible_text(pricing_window.bill_period_reference)

        # Obtain the form save btn element and submit the test entries.
        ele_save_pricing_window_button = \
            self.driver.find_element_by_xpath('//*[@id="utilitypricingwindow_form"]/div/div/input[1]')
        ele_save_pricing_window_button.click()
