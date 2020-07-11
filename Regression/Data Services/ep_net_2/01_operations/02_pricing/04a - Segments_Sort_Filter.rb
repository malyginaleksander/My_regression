require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#segments'

Watir::Waiter::wait_until(240,5) do
browser.span(:id => 'gbox_priceSegmentsGrid').exists?
end

#Results populating on page
if
browser.div(:id => 'gbox_priceSegmentsGrid').exists?
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
print "Segment Next Page - Passed", "\n"
else
print "Segment Next Page - Failed", "\n"
end

#Previous Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-prev').click
Watir::Waiter::wait_until {browser.text.include? "View 1 - 100"}
if
browser.text.include? "View 1 - 100"
print "Segment Previous Page - Passed", "\n"
else
print "Segment Previous Page - Failed", "\n"
end

#Last Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-end').click
Watir::Waiter::wait_until {browser.text.include? "View 201"}
if
browser.text.include? "View 201"
print "Segment Last Page - Passed", "\n"
else
print "Segment Last Page - Failed", "\n"
end

#First Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-first').click
Watir::Waiter::wait_until {browser.text.include? "View 1 - 100"}
if
browser.text.include? "View 1 - 100"
print "Segment First Page - Passed", "\n"
else
print "Segment First Page - Failed", "\n"
end

#Sort
browser.div(:id => 'jqgh_priceSegmentsGrid_PriceSegment').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td').text.include? "WHTINT"
print "Sort by Price Segment DESC - Passed", "\n"
else
print "Sort by Price Segment DESC - Failed", "\n"
end

browser.div(:id => 'jqgh_priceSegmentsGrid_PriceSegment').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td').text.include? "00004"
print "Sort by Price Segment ASC - Passed", "\n"
else
print "Sort by Price Segment ASC - Failed", "\n"
end

#Unit
browser.text_field(:id => 'jqgh_priceSegmentsGrid_Unit').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "A"                         
print "Sort by Unit ASC - Passed", "\n"
else
print "Sort by Unit ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_priceSegmentsGrid_Unit').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "X"
print "Sort by Unit DESC - Passed", "\n"
else
print "Sort by Unit DESC - Failed", "\n"
end

#Rounding Method
browser.div(:id => 'jqgh_priceSegmentsGrid_RoundingMethod').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "undefined"
print "Sort by Rounding Method ASC - Passed", "\n"
else
print "Sort by Rounding Method ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_priceSegmentsGrid_RoundingMethod').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "Round9"
print "Sort by Rounding Method DESC - Passed", "\n"
else
print "Sort by Rounding Method DESC - Failed", "\n"
end

#Filter
wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

#Price Segment
browser.text_field(:id => 'gs_PriceSegment').set("VIP005")
browser.send_keys("{ENTER}")
sleep 5
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td').text.include? "VIP005"
print "Filter by Price Segment - Passed", "\n"
else
print "Filter by Price Segment - Failed", "\n"
end
browser.text_field(:id => 'gs_PriceSegment').set("")

#Unit
browser.select_list(:id => 'gs_Unit').option(:value, 'U').select
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "U"
print "Filter by Unit - Passed", "\n"
else
print "Filter by Unit - Failed", "\n"
end
browser.select_list(:id => 'gs_Unit').option(:value, '').select

#Rounding Method
browser.select_list(:id => 'gs_RoundingMethod').option(:value, 'GasRoundOdd').select
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "GasRoundOdd"
print "Filter by Rounding Method - Passed", "\n"
else
print "Filter by Rounding Method - Failed", "\n"
end
browser.select_list(:id => 'gs_RoundingMethod').option(:value, '').select

#Status
browser.select_list(:id => 'gs_SegmentStatus').option(:value, 'ACTIVE').select
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "ACTIVE"
print "Filter by Status - Passed", "\n"
else
print "Filter by Status - Failed", "\n"
end
browser.select_list(:id => 'gs_SegmentStatus').option(:value, '').select

#Description
browser.text_field(:id => 'gs_Description').set("Upromise Intro")
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "Upromise Intro"
print "Filter by Description - Passed", "\n"
else
print "Filter by Description - Failed", "\n"
end
browser.text_field(:id => 'gs_Description').set("")

#Business Rules Utility Code
browser.text_field(:id => 'gs_BizRule_UtilityCode').set("[UtilityCode]='08'")
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[8]').text.include? "[UtilityCode]='08'"
print "Filter by Business Rules Utility Code - Passed", "\n"
else
print "Filter by Business Rules Utility Code - Failed", "\n"
end
browser.text_field(:id => 'gs_BizRule_UtilityCode').set("")

#Business Rules Reporting Group
browser.text_field(:id => 'gs_BizRule_RptGroup').set("[MKGroup]='D2DRINT'")
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[9]').text.include? "[MKGroup]='D2DRINT'"
print "Filter by Business Rules Reporting Group - Passed", "\n"
else
print "Filter by Business Rules Reporting Group - Failed", "\n"
end
browser.text_field(:id => 'gs_BizRule_RptGroup').set("")

#Business Rules Other
browser.text_field(:id => 'gs_BizRule_Other').set("[UtilityCode]='02'")
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[10]').text.include? "[UtilityCode]='02'"
print "Filter by Business Rules Other - Passed", "\n"
else
print "Filter by Business Rules Other - Failed", "\n"
end
browser.text_field(:id => 'gs_BizRule_Other').set("")
browser.send_keys("{ENTER}")

browser.close