require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Rounding Price Limits")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

#Edit Record
wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').click
browser.span(:class => 'ui-icon ui-icon-pencil').click
browser.text_field(:id => 'RoundingPriceLimitMax').set("7.50")
browser.span(:class => 'ui-icon ui-icon-disk').click
browser.span(:class => 'ui-icon ui-icon-closethick').click
browser.close

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Rounding Price Limits")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "7.50"
print "Edit and Verify Record - Passed", "\n"
else
print "Edit and Verify Record - Failed", "\n"
end
sleep 2
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').click
browser.span(:class => 'ui-icon ui-icon-pencil').click
browser.text_field(:id => 'RoundingPriceLimitMax').set("5.50")
browser.span(:class => 'ui-icon ui-icon-disk').click
browser.span(:class => 'ui-icon ui-icon-closethick').click

browser.close
