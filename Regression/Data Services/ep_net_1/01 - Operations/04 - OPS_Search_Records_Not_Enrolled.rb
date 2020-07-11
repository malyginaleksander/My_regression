require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Operations/SearchEnrollments.aspx'

#Search Customers Not Yet Enrolled By Last Name
browser.text_field(:id => 'ctl00_MainContent_txtLastName').set ('smith')
browser.text_field(:id => 'ctl00_MainContent_txtBillingZip').set ("19067")
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "CustNo"}
if
browser.table(:id => 'ctl00_MainContent_gvResults').text.include? "SMITH"
print "Search Customer Not Yet Enrolled By Last Name - Passed", "\n"
else
print "Search Customer Not Yet Enrolled By Last Name - Failed", "\n"
end
browser.button(:value => 'Reset').click

#Search Customers Not Yet Enrolled By Billing Zip
Watir::Waiter::wait_until {browser.text_field(:id => 'ctl00_MainContent_txtLastName').text.include? ""}
browser.text_field(:id => 'ctl00_MainContent_txtLastName').set ('smith')
browser.text_field(:id => 'ctl00_MainContent_txtBillingZip').set ("19067")
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "CustNo"}
if
browser.table(:id => 'ctl00_MainContent_gvResults').text.include? "19067"
print "Search Customer Not Yet Enrolled By ZIP - Passed", "\n"
else
print "Search Customer Not Yet Enrolled By ZIP - Failed", "\n"
end
browser.button(:value => 'Reset').click
=begin
#Search Customers Not Yet Enrolled By Enroll Type Move In
Watir::Waiter::wait_until {browser.text_field(:id => 'ctl00_MainContent_txtBillingZip').text.include? ""}
browser.select_list(:id => 'ctl00_MainContent_ddlEnrollType').select ('Move In')
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "CustNo"}
browser.link(:text => 'View Record').click
Watir::Waiter::wait_until {browser.text.include? "Expand All"}
browser.link(:text => 'Expand All').click
Watir::Waiter::wait_until {browser.text.include? "Customer Information"}

if
browser.select_list(:id => 'ctl00_MainContent_ValidationPanel2_ddlEnrollType').option(:text, 'Move In').selected
print "Search Customer Not Yet Enrolled By Enroll Type - Passed", "\n"
else
print "Search Customer Not Yet Enrolled By Enroll Type - Failed", "\n"
end
browser.link(:id => 'ctl00_MainContent_HyperLink1').click
sleep 2

#Search Customers Not Yet Enrolled By Enroll Type On Cycle
Watir::Waiter::wait_until {browser.text_field(:id => 'ctl00_MainContent_txtBillingZip').text.include? ""}
browser.select_list(:id => 'ctl00_MainContent_ddlEnrollType').select ('On Cycle')
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "CustNo"}
browser.link(:text => 'View Record').click
Watir::Waiter::wait_until {browser.text.include? "Expand All"}
browser.link(:text => 'Expand All').click
Watir::Waiter::wait_until {browser.text.include? "Customer Information"}

if
browser.select_list(:id => 'ctl00_MainContent_ValidationPanel2_ddlEnrollType').option(:text, 'On Cycle').selected
print "Search Customer Not Yet Enrolled By Enroll Type - Passed", "\n"
else
print "Search Customer Not Yet Enrolled By Enroll Type - Failed", "\n"
end
browser.link(:id => 'ctl00_MainContent_HyperLink1').click
sleep 2
=end
browser.close