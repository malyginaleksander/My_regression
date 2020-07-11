require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 3

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Fixed Prices")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

if
browser.div(:id => 'gbox_pricingAdminGrid').exists?
print "Results populating on page - Passed", "\n"
else
print "Results populating on page - Failed", "\n"
end

#Add and Verify Record
browser.span(:class => 'ui-icon ui-icon-plus').click
browser.text_field(:id => 'FixedPrice').set("0.2299")
browser.text_field(:id => 'EffectiveDate').set("12/15/2014")
browser.select_list(:id => 'UtilityCode').select("15")
sleep 2
browser.span(:class => 'ui-icon ui-icon-disk').click
sleep 2
browser.span(:class => 'ui-icon ui-icon-closethick').click
browser.close

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2
browser.select_list(:id => 'pricingAdminComboBox').select("Fixed Prices")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_FixedPrice').set("0.2299")
browser.text_field(:id => 'gs_FixedPrice').set("")
browser.text_field(:id => 'gs_FixedPrice').set("0.2299")
browser.send_keys("{ENTER}")

sleep 5
if
browser.table(:xpath => '/html/body/div[1]/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "0.2299"
print "Add and Verify Record - Passed", "\n"
else
print "Add and Verify Record - Failed", "\n"
end
browser.close

#Edit Record
browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 3
#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Fixed Prices")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}
if
browser.div(:id => 'gbox_pricingAdminGrid').exists?
print "Results populating on page - Passed", "\n"
else
print "Results populating on page - Failed", "\n"
end

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_RevenueClass').set("2")
browser.text_field(:id => 'gs_EffectiveDate').set("12/15/2010")
browser.text_field(:id => 'gs_SPL').set("i")
browser.text_field(:id => 'gs_SPL').set("")
browser.text_field(:id => 'gs_SPL').set("i")
browser.send_keys("{ENTER}")
sleep 5
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').click
browser.span(:class => 'ui-icon ui-icon-pencil').click
browser.text_field(:id => 'FixedPrice').set("0.99")
browser.span(:class => 'ui-icon ui-icon-disk').click
browser.span(:class => 'ui-icon ui-icon-closethick').click
browser.close

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 3
#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Fixed Prices")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_RevenueClass').set("2")
browser.text_field(:id => 'gs_EffectiveDate').set("12/15/2010")
browser.text_field(:id => 'gs_SPL').set("i")
browser.text_field(:id => 'gs_SPL').set("")
browser.text_field(:id => 'gs_SPL').set("i")
browser.send_keys("{ENTER}")
sleep 5

if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "0.99"
print "Edit and Verify Record - Passed", "\n"
else
print "Edit and Verify Record - Failed", "\n"
end

browser.close