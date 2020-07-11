require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#batch-history'
sleep 5

#Select a Price Batch
browser.select_list(:id, "priceBatchHistorySelector").select("2: 2/24/2009")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_priceBatchHistoryGrid').exists?}
if
browser.div(:id => 'gbox_priceBatchHistoryGrid').exists?
print "Select a Price Batch - Passed", "\n"
else
print "Select a Price Batch - Failed", "\n"
end
=begin
#Paging on the Detail grid functions correctly
#Next Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-next').click
Watir::Waiter::wait_until {browser.text.include? "View 101"}
if
browser.text.include? "View 101"
print "Price Batch Next Page - Passed", "\n"
else
print "Price Batch Next Page - Failed", "\n"
end

#Previous Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-prev').click
Watir::Waiter::wait_until {browser.text.include? "View 1 - 100"}
if
browser.text.include? "View 1 - 100"
print "Price Batch Previous Page - Passed", "\n"
else
print "Price Batch Previous Page - Failed", "\n"
end

#Last Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-end').click
Watir::Waiter::wait_until {browser.text.include? "View 601"}
if
browser.text.include? "View 601"
print "Price Batch Last Page - Passed", "\n"
else
print "Price Batch Last Page - Failed", "\n"
end

#First Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-first').click
Watir::Waiter::wait_until {browser.text.include? "View 1 - 100"}
if
browser.text.include? "View 1 - 100"
print "Price Batch First Page - Passed", "\n"
else
print "Price Batch First Page - Failed", "\n"
end

#Select a Page
####### UPDATE PAGE NUMBERS)#######
wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')

browser.text_field(:class => 'ui-pg-input').set("2")
sleep 2
browser.send_keys("{ENTER}") 
Watir::Waiter::wait_until {browser.text.include? "View 101"}
if
browser.text.include? "View 101"
print "Price Batch Select a Page - Passed", "\n"
else
print "Price Batch Select a Page - Failed", "\n"
end
=end
#Sorting
#Status
browser.text_field(:id => 'jqgh_priceBatchHistoryGrid_PBR_Status').click
sleep 10
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "Pending"
print "Sort by Status ASC - Passed", "\n"
else
print "Sort by Status ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_priceBatchHistoryGrid_PBR_Status').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "Reject"
print "Sort by Status DESC - Passed", "\n"
else
print "Sort by Status DESC - Failed", "\n"
end

#Region
browser.div(:id => 'jqgh_priceBatchHistoryGrid_PBR_SPL').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "01"
print "Sort by Region ASC - Passed", "\n"
else
print "Sort by Region ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_priceBatchHistoryGrid_PBR_SPL').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "NYSEG-GAS"
print "Sort by Region DESC - Passed", "\n"
else
print "Sort by Region DESC - Failed", "\n"
end

#Price Segment
browser.div(:id => 'jqgh_priceBatchHistoryGrid_PriceSegment').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "undefined"
print "Sort by Price Segment ASC - Passed", "\n"
else
print "Sort by Price Segment ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_priceBatchHistoryGrid_PriceSegment').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "STDOFF"
print "Sort by Price Segment DESC - Passed", "\n"
else
print "Sort by Price Segment DESC - Failed", "\n"
end

#Filter
wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

#Status
browser.select_list(:id => 'gs_PBR_Status').option(:value, 'reject').select
browser.select_list(:id => 'gs_PBR_Status').option(:value, '').select
browser.select_list(:id => 'gs_PBR_Status').option(:value, 'reject').select
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "Reject"
print "Filter by Status - Passed", "\n"
else
print "Filter by Status - Failed", "\n"
end
browser.select_list(:id => 'gs_PBR_Status').option(:value, '').select

#Utility Code
browser.text_field(:id => 'gs_PBR_UtilityCode').set("45")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "45"
print "Filter by Utility Code - Passed", "\n"
else
print "Filter by Utility Code - Failed", "\n"
end
browser.text_field(:id => 'gs_PBR_UtilityCode').set("")

#Region
browser.text_field(:id => 'gs_PBR_SPL').set("BECO")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "BECO"
print "Filter by Region - Passed", "\n"
else
print "Filter by Region - Failed", "\n"
end
browser.text_field(:id => 'gs_PBR_SPL').set("")

browser.close