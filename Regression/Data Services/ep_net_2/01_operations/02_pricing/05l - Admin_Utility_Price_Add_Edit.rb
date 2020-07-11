require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Utility Prices")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

#Add and Verify Record
browser.span(:class => 'ui-icon ui-icon-plus').click
browser.text_field(:id => 'EffectiveDate').set("11/03/2012")
browser.select_list(:id => 'RevenueClass').select("2")
browser.select_list(:id => 'UtilityCode').select("20")
browser.text_field(:id => 'UtilityPrice').set("666")
sleep 2
browser.span(:class => 'ui-icon ui-icon-disk').click
sleep 2
browser.span(:class => 'ui-icon ui-icon-closethick').click
browser.close

sleep 5

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Utility Prices")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_UtilityPrice').set("666")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_UtilityPrice').set("")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_UtilityPrice').set("666")
browser.send_keys("{ENTER}")
sleep 5

if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "666"
print "Add and Verify Record - Passed", "\n"
else
print "Add and Verify Record - Failed", "\n"
end
browser.text_field(:id => 'gs_UtilityPrice').set("")
browser.close

#Edit Record
browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Utility Prices")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_EffectiveDate').set("10/02/2012")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_SPL').set("i")
browser.text_field(:id => 'gs_SPL').set("")
browser.text_field(:id => 'gs_SPL').set("i")
browser.send_keys("{ENTER}")
sleep 5
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').click
browser.span(:class => 'ui-icon ui-icon-pencil').click
browser.text_field(:id, "UtilityPrice").set("3.999")
browser.span(:class => 'ui-icon ui-icon-disk').click
browser.span(:class => 'ui-icon ui-icon-closethick').click
browser.close

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Utility Prices")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5
browser.text_field(:id => 'gs_EffectiveDate').set("10/02/2012")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_SPL').set("i")
browser.text_field(:id => 'gs_SPL').set("")
browser.text_field(:id => 'gs_SPL').set("i")
browser.send_keys("{ENTER}")
sleep 2

if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "3.999"
print "Edit and Verify Record - Passed", "\n"
else
print "Edit and Verify Record - Failed", "\n"
end
sleep 2

browser.close