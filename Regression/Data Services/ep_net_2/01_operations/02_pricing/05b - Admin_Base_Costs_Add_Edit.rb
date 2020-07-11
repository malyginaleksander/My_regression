require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Base Costs")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

if
browser.div(:id => 'gbox_pricingAdminGrid').exists?
print "Results populating on page - Passed", "\n"
else
print "Results populating on page - Failed", "\n"
end

#Add and Verify Record
browser.span(:class => 'ui-icon ui-icon-plus').click
browser.text_field(:id => 'Ancillary').set("0.9991")
browser.text_field(:id => 'BaseSupply').set("0.9991")
browser.text_field(:id => 'Demand').set("0.9991")
browser.text_field(:id => 'EffectiveDate').set("01/31/2012")
browser.text_field(:id => 'Green').set("0.01000")
browser.text_field(:id => 'LineLoss').set("0.00000")
browser.text_field(:id => 'UFE').set("0.00000")
browser.select_list(:id => 'UtilityCode').select("02")
sleep 2
browser.span(:class => 'ui-icon ui-icon-disk').click
sleep 1
browser.span(:class => 'ui-icon ui-icon-closethick').click
sleep 1
browser.close

#browser = Watir::Browser.new
#browser.goto 'http://epnet2.pt.nrgpl.us/Pricing'
#browser.link(:href => '#admin').click
browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Base Costs")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_Ancillary').set("0.9991")
browser.text_field(:id => 'gs_Ancillary').set("")
browser.text_field(:id => 'gs_Ancillary').set("0.9991")
browser.send_keys("{ENTER}")
sleep 5
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "0.9991"
print "Add and Verify Record - Passed", "\n"
else
print "Add and Verify Record - Failed", "\n"
end
browser.text_field(:id => 'gs_Ancillary').set("")
browser.close

#Edit Record
browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Base Costs")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_BaseSupply').set("0.9991")
browser.text_field(:id => 'gs_BaseSupply').set("")
browser.text_field(:id => 'gs_BaseSupply').set("0.9991")
browser.send_keys("{ENTER}")
#browser.text_field(:id => 'gs_RevenueClass').set("1")
#browser.send_keys("{ENTER}")
sleep 5
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').click
browser.span(:class => 'ui-icon ui-icon-pencil').click
sleep 1
browser.text_field(:id => 'Demand').set("0.6969")
browser.span(:class => 'ui-icon ui-icon-disk').click
sleep 1
browser.span(:class => 'ui-icon ui-icon-closethick').click
sleep 1
browser.close

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Base Costs")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5
browser.text_field(:id => 'gs_Demand').set("0.6969")
browser.text_field(:id => 'gs_Demand').set("")
browser.text_field(:id => 'gs_Demand').set("0.6969")
#browser.text_field(:id => 'gs_RevenueClass').set("1")
browser.send_keys("{ENTER}")

if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "0.6969"
print "Edit and Verify Record - Passed", "\n"
else
print "Edit and Verify Record - Failed", "\n"
end
browser.close

#Reload Grid
browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
browser.select_list(:id => 'pricingAdminComboBox').select("Base Costs")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_BaseSupply').set("0.0655")
browser.send_keys("{ENTER}")
sleep 5
browser.span(:class => 'ui-icon ui-icon-refresh').click
if
browser.text.include? "2 of 2"
print "Reload Grid - Failed", "\n"
else
print "Reload Grid - Passed", "\n"
end

browser.close