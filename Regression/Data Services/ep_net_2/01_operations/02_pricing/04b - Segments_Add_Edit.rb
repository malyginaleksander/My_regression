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

#Add and Verify Record
############## Update Records ####################
browser.span(:class => 'ui-icon ui-icon-plus').click
browser.text_field(:id, "PriceSegment").set("0436D2D")
browser.text_field(:id, "Adder").set("0.1140")
browser.text_field(:id, "DemandAdder").set("0.1140")
browser.text_field(:id, "RoundingMethod").set("NONE")
browser.text_field(:id, "Description").set("Test")
browser.span(:class => 'ui-icon ui-icon-disk').click
browser.span(:class => 'ui-icon ui-icon-closethick').click
browser.close

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#segments'

Watir::Waiter::wait_until(240,5) do
browser.span(:id => 'gbox_priceSegmentsGrid').exists?
end

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_PriceSegment').set("0436D2D")
browser.send_keys("{ENTER}")
sleep 2
browser.text_field(:id => 'gs_PriceSegment').set("0411D2DMO3")
browser.send_keys("{ENTER}")
sleep 2
browser.text_field(:id => 'gs_PriceSegment').set("0436D2D")
browser.send_keys("{ENTER}")
sleep 5
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td').text.include? "0436D2D"
print "Add and Verify Record - Passed", "\n"
else
print "Add and Verify Record - Failed", "\n"
end
browser.text_field(:id => 'gs_PriceSegment').set("")

#Edit Record
browser.text_field(:id => 'gs_PriceSegment').set("0411D2DMO3")
browser.send_keys("{ENTER}")
sleep 10
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td').click
browser.span(:class => 'ui-icon ui-icon-pencil').click
browser.text_field(:id => 'Description').set("Test")
browser.span(:class => 'ui-icon ui-icon-disk').click
browser.span(:class => 'ui-icon ui-icon-closethick').click
browser.close

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#segments'

Watir::Waiter::wait_until(240,5) do
browser.span(:id => 'gbox_priceSegmentsGrid').exists?
end

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_PriceSegment').set("0411D2DMO3")
browser.send_keys("{ENTER}")
sleep 2
browser.text_field(:id => 'gs_PriceSegment').set("0436D2D")
browser.send_keys("{ENTER}")
sleep 2
browser.text_field(:id => 'gs_PriceSegment').set("0411D2DMO3")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[4]/div/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "Test"
print "Edit and Verify Record - Passed", "\n"
else
print "Edit and Verify Record - Failed", "\n"
end
browser.close