require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Missing Utility Codes, Zones, or Revenue Classes")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

if
browser.div(:id => 'gbox_pricingAdminGrid').exists?
print "Results populating on page - Passed", "\n"
else
print "Results populating on page - Failed", "\n"
end

#Paging on the Detail grid functions correctly
#Next Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-next').click
Watir::Waiter::wait_until {browser.text.include? "View 101"}
if
browser.text.include? "View 101"
print "Admin Base Cost Next Page - Passed", "\n"
else
print "Admin Base Cost Next Page - Failed", "\n"
end

#Previous Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-prev').click
Watir::Waiter::wait_until {browser.text.include? "View 1 - 100"}
if
browser.text.include? "View 1 - 100"
print "Admin Base Cost Previous Page - Passed", "\n"
else
print "Admin Base Cost Previous Page - Failed", "\n"
end

#Last Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-end').click
Watir::Waiter::wait_until {browser.text.include? "View 2 301 - "}
if
browser.text.include? "View 2 301 - "
print "Admin Base Cost Last Page - Passed", "\n"
else
print "Admin Base Cost Last Page - Failed", "\n"
end

#First Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-first').click
Watir::Waiter::wait_until {browser.text.include? "View 1 - 100"}
if
browser.text.include? "View 1 - 100"
print "Admin Base Cost First Page - Passed", "\n"
else
print "Admin Base Cost First Page - Failed", "\n"
end

#Sort
#Utility Code
browser.div(:id => 'jqgh_pricingAdminGrid_UtilityCode').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[8]').text.include? "02"
print "Sort by Utility Code ASC - Passed", "\n"
else
print "Sort by Utility Code ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_UtilityCode').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[8]').text.include? "41"
print "Sort by Utility Code DESC - Passed", "\n"
else
print "Sort by Utility Code DESC - Failed", "\n"
end

#Utility Billing City
browser.div(:id => 'jqgh_pricingAdminGrid_UtilityBillingCity').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[14]').text.include? "undefined"
print "Sort by Utility Billing City ASC - Passed", "\n"
else
print "Sort by Utility Billing City ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_UtilityBillingCity').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[14]').text.include? "ZION"
print "Sort by Utility Billing City DESC - Passed", "\n"
else
print "Sort by Utility Billing City DESC - Failed", "\n"
end

#Filter
wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 8

#Utility Account Number
browser.text_field(:id => 'gs_UtilityAccountNumber').set("2025753022")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_UtilityAccountNumber').set("")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_UtilityAccountNumber').set("2025753022")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "2025753022"
print "Filter by Utility Account Number - Passed", "\n"
else
print "Filter by Utility Account Number - Failed", "\n"
end
browser.text_field(:id => 'gs_UtilityAccountNumber').set("")
browser.send_keys("{ENTER}")

#Utility Code
browser.select_list(:id => 'gs_UtilityCode').option(:value, '16').select
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[8]').text.include? "16"
print "Filter by Utility Code - Passed", "\n"
else
print "Filter by Utility Code - Failed", "\n"
end
browser.select_list(:id => 'gs_UtilityCode').option(:value, '').select

#Utility Billing City
browser.text_field(:id => 'gs_UtilityBillingCity').set("ZION")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[14]').text.include? "ZION"
print "Filter by Utility Billing City - Passed", "\n"
else
print "Filter by Utility Billing City - Failed", "\n"
end
browser.text_field(:id => 'gs_UtilityBillingCity').set("")
browser.send_keys("{ENTER}")

browser.close