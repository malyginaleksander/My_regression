require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Holidays")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

if
browser.div(:id => 'gbox_pricingAdminGrid').exists?
print "Results populating on page - Passed", "\n"
else
print "Results populating on page - Failed", "\n"
end

#Sort
#Description
browser.div(:id => 'jqgh_pricingAdminGrid_HolidayDescription').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "Christmas Day"
print "Sort by Description ASC - Passed", "\n"
else
print "Sort by Description ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_HolidayDescription').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "Thanksgiving Day"
print "Sort by Description DESC - Passed", "\n"
else
print "Sort by Description DESC - Failed", "\n"
end

#Date
browser.div(:id => 'jqgh_pricingAdminGrid_Holiday').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "05/25"
print "Sort by Date ASC - Passed", "\n"
else
print "Sort by Date ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_Holiday').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "12/25"
print "Sort by Date DESC - Passed", "\n"
else
print "Sort by Date DESC - Failed", "\n"
end

#Filter
wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 8

#Date
browser.text_field(:id => 'gs_Holiday').set("07/05/2010")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_Holiday').set("")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_Holiday').set("07/05/2010")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "07/05/2010"
print "Filter by Date - Passed", "\n"
else
print "Filter by Date - Failed", "\n"
end
browser.text_field(:id => 'gs_Holiday').set("")
browser.send_keys("{ENTER}")

#Description
browser.text_field(:id => 'gs_HolidayDescription').set("Labor Day")
browser.send_keys("{ENTER}")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "Labor Day"
print "Filter by Description - Passed", "\n"
else
print "Filter by Description - Failed", "\n"
end
browser.text_field(:id => 'gs_HolidayDescription').set("")
browser.send_keys("{ENTER}")

browser.close