require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epweb-pt/Pricing#reject-queue'

Watir::Waiter::wait_until(240,5) do
browser.span(:id => 'gbox_rejectQueueGrid').exists?
end
=begin
#Results populating on page
if
browser.div(:id => 'gbox_rejectQueueGrid').exists?
print "Results populating on page - Passed", "\n"
else
print "Results populating on page - Failed", "\n"
end

#Paging on the Detail grid functions correctly
#Next Page
####### UPDATE PAGE NUMBERS)#######
browser.table(:id => 'next_rejectQueuePager').span(:class => 'ui-icon ui-icon-seek-next').click
Watir::Waiter::wait_until {browser.text.include? "View 101 - 200"}
if
browser.text.include? "View 101 - 200"
print "Price Batch Next Page - Passed", "\n"
else
print "Price Batch Next Page - Failed", "\n"
end

#Previous Page
####### UPDATE PAGE NUMBERS)#######
browser.table(:id => 'prev_rejectQueuePager').span(:class => 'ui-icon ui-icon-seek-prev').click
Watir::Waiter::wait_until {browser.text.include? "View 1 - 100"}
if
browser.text.include? "View 1 - 100"
print "Price Batch Previous Page - Passed", "\n"
else
print "Price Batch Previous Page - Failed", "\n"
end

#Last Page
####### UPDATE PAGE NUMBERS)#######
browser.table(:id => 'last_rejectQueuePager').span(:class => 'ui-icon ui-icon-seek-end').click
Watir::Waiter::wait_until {browser.text.include? "View 301"}
if
browser.text.include? "View 301"
print "Price Batch Last Page - Passed", "\n"
else
print "Price Batch Last Page - Failed", "\n"
end

#First Page
####### UPDATE PAGE NUMBERS)#######
browser.table(:id => 'first_rejectQueuePager').span(:class => 'ui-icon ui-icon-seek-first').click
Watir::Waiter::wait_until {browser.text.include? "View 1 - 100"}
if
browser.text.include? "View 1 - 100"
print "Price Batch First Page - Passed", "\n"
else
print "Price Batch First Page - Failed", "\n"
end

#Sorting
#Utility Code
browser.text_field(:id => 'jqgh_rejectQueueGrid_UtilityCode').click
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div/div/div[3]/div[3]/div/table/tbody/tr[2]/td[12]').text.include? "01"
print "Sort by Utility Code ASC - Passed", "\n"
else
print "Sort by Utility Code ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_rejectQueueGrid_UtilityCode').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div/div/div[3]/div[3]/div/table/tbody/tr[2]/td[12]').text.include? "57"
print "Sort by Utility Code DESC - Passed", "\n"
else
print "Sort by Utility Code DESC - Failed", "\n"
end

#State
browser.text_field(:id => 'jqgh_rejectQueueGrid_State').click
sleep 10
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div/div/div[3]/div[3]/div/table/tbody/tr[2]/td[13]').text.include? "CT"                         
print "Sort by State ASC - Passed", "\n"
else
print "Sort by State ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_rejectQueueGrid_State').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div/div/div[3]/div[3]/div/table/tbody/tr[2]/td[13]').text.include? "PA"
print "Sort by State DESC - Passed", "\n"
else
print "Sort by State DESC - Failed", "\n"
end
=end
#Filter
#wsh = WIN32OLE.new('Wscript.Shell')
#wsh.AppActivate('Pricing Home Page')
#sleep 5

#Price Batch ID
browser.text_field(:id => 'gs_PriceBatchId').set("1478")
browser.send_keys("{ENTER}")
browser.send_keys("{ENTER}")
Watir::Waiter::wait_until(180,5) do
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div/div/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "1478"
end
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div/div/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "1478"
print "Filter by Price Batch ID - Passed", "\n"
else
print "Filter by Price Batch ID - Failed", "\n"
end
browser.text_field(:id => 'gs_PriceBatchId').set("")


#browser.close