require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 5

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Base Costs")
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
Watir::Waiter::wait_until {browser.text.include? "View 901"}
if
browser.text.include? "View 901"
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
#SPL
browser.div(:id => 'jqgh_pricingAdminGrid_SPL').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[11]').text.include? "01"
print "Sort by SPL ASC - Passed", "\n"
else
print "Sort by SPL ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_SPL').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[11]').text.include? "PSG"
print "Sort by SPL DESC - Passed", "\n"
else
print "Sort by SPL DESC - Failed", "\n"
end

#Utility Code
browser.div(:id => 'jqgh_pricingAdminGrid_UtilityCode').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[12]').text.include? "01"                         
print "Sort by Utility Code ASC - Passed", "\n"
else
print "Sort by Utility Code ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_UtilityCode').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[12]').text.include? "53"
print "Sort by Unit DESC - Passed", "\n"
else
print "Sort by Unit DESC - Failed", "\n"
end

#Filter
wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

#Base Supply
browser.text_field(:id => 'gs_BaseSupply').set("0.0388")
browser.send_keys("{ENTER}")
browser.send_keys("{ENTER}")
sleep 5
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "0.03880"
print "Filter by Base Supply - Passed", "\n"
else
print "Filter by Base Supply - Failed", "\n"
end
browser.text_field(:id => 'gs_BaseSupply').set("")

#Effective Date
browser.text_field(:id => 'gs_EffectiveDate').set("04/06/2009")
browser.send_keys("{ENTER}")
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "04/06/2009"
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
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[8]').text.include? "2"
print "Filter by Revenue Class - Passed", "\n"
else
print "Filter by Revenue Class - Failed", "\n"
end
browser.text_field(:id => 'gs_RevenueClass').set("")

#SPL
browser.text_field(:id => 'gs_SPL').set("COMED")
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[11]').text.include? "COMED"
print "Filter by SPL - Passed", "\n"
else
print "Filter by SPL - Failed", "\n"
end
browser.text_field(:id => 'gs_SPL').set("")
browser.send_keys("{ENTER}")

#Utility Code
browser.select_list(:id => 'gs_UtilityCode').option(:value, '48').select
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[12]').text.include? "48"
print "Filter by Utility Code - Passed", "\n"
else
print "Filter by Utility Code - Failed", "\n"
end
browser.select_list(:id => 'gs_UtilityCode').option(:value, '').select

browser.close