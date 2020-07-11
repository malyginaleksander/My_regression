require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Fixed Prices")
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
Watir::Waiter::wait_until {browser.text.include? "View 101 - 200"}
if
browser.text.include? "View 101 - 200"
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
Watir::Waiter::wait_until {browser.text.include? "View 201"}
if
browser.text.include? "View 201"
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
#Revenue Class
browser.div(:id => 'jqgh_pricingAdminGrid_RevenueClass').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "1"
print "Sort by Revenue Class ASC - Passed", "\n"
else
print "Sort by Revenue Class ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_RevenueClass').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "3"
print "Sort by Revenue Class DESC - Passed", "\n"
else
print "Sort by Revenue Class DESC - Failed", "\n"
end

#SPL
browser.div(:id => 'jqgh_pricingAdminGrid_SPL').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "01"
print "Sort by SPL ASC - Passed", "\n"
else
print "Sort by SPL ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_SPL').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "PSG"
print "Sort by SPL DESC - Passed", "\n"
else
print "Sort by SPL DESC - Failed", "\n"
end

#Utility Code
browser.div(:id => 'jqgh_pricingAdminGrid_UtilityCode').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "01"                         
print "Sort by Utility Code ASC - Passed", "\n"
else
print "Sort by Utility Code ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_UtilityCode').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "53"
print "Sort by Unit DESC - Passed", "\n"
else
print "Sort by Unit DESC - Failed", "\n"
end

#Filter
wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 8

#Fixed Price
browser.text_field(:id => 'gs_FixedPrice').set("4.37")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "4.37100"
print "Filter by Fixed Price - Passed", "\n"
else
print "Filter by Fixed Price - Failed", "\n"
end
browser.text_field(:id => 'gs_FixedPrice').set("")
browser.send_keys("{ENTER}")

#Effective Date
browser.text_field(:id => 'gs_EffectiveDate').set("10/11/2011")
browser.send_keys("{ENTER}")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "10/11/2011"
print "Filter by Effective Date - Passed", "\n"
else
print "Filter by Effective Date - Failed", "\n"
end
browser.text_field(:id => 'gs_EffectiveDate').set("")
browser.send_keys("{ENTER}")

#Revenue Class
browser.text_field(:id => 'gs_RevenueClass').set("2")
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "2"
print "Filter by Revenue Class - Passed", "\n"
else
print "Filter by Revenue Class - Failed", "\n"
end
browser.text_field(:id => 'gs_RevenueClass').set("")

#SPL
browser.text_field(:id => 'gs_SPL').set("COMED")
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "COMED"
print "Filter by SPL - Passed", "\n"
else
print "Filter by SPL - Failed", "\n"
end
browser.text_field(:id => 'gs_SPL').set("")
browser.send_keys("{ENTER}")

#Utility Code
browser.select_list(:id => 'gs_UtilityCode').option(:value, '48').select
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "48"
print "Filter by Utility Code - Passed", "\n"
else
print "Filter by Utility Code - Failed", "\n"
end
browser.select_list(:id => 'gs_UtilityCode').option(:value, '').select

browser.close