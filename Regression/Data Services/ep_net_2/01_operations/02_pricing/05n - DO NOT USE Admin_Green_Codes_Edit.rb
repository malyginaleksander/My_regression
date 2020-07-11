require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Mismatched Green Codes")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}
browser.span(:class => 'ui-icon ui-icon-seek-next').click

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_UtilityAccountNumber').set("412313412000050")
browser.text_field(:id => 'gs_UtilityAccountNumber').set("")
browser.text_field(:id => 'gs_UtilityAccountNumber').set("412313412000050")
browser.send_keys("{ENTER}")
sleep 5
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').click
browser.span(:class => 'ui-icon ui-icon-pencil').click
browser.text_field(:id => 'BusinessName').set("test update")
browser.span(:class => 'ui-icon ui-icon-disk').click
browser.span(:class => 'ui-icon ui-icon-closethick').click
browser.close

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Mismatched Green Codes")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}
browser.span(:class => 'ui-icon ui-icon-seek-next').click

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_UtilityAccountNumber').set("412313412000050")
browser.text_field(:id => 'gs_UtilityAccountNumber').set("")
browser.text_field(:id => 'gs_UtilityAccountNumber').set("412313412000050")
browser.send_keys("{ENTER}")
sleep 7

if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "test update"
print "Edit and Verify Record - Passed", "\n"
else
print "Edit and Verify Record - Failed", "\n"
end
browser.close