require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Operations/SearchEnrollments.aspx'

#Search Customers Enrolled By Last Name
browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').select ('Customers Enrolled')
sleep 5
browser.text_field(:id => 'ctl00_MainContent_txtLastName').set ("Smith")
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "CustNo"}
if
browser.table(:id => 'ctl00_MainContent_gvCustomerResults').text.include? "SMITH"
print "Search Customer Enrolled By Last Name - Passed", "\n"
else
print "Search Customer Enrolled By Last Name - Failed", "\n"
end
browser.button(:id => 'ctl00_MainContent_btnReset').click
Watir::Waiter::wait_until {browser.text_field(:id => 'ctl00_MainContent_txtLastName').text.include? ""}
sleep 2
browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').select('Customers Not Yet Enrolled')
Watir::Waiter::wait_until {browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').option(:text, "Customers Not Yet Enrolled").selected}

#Search Customers Enrolled By Billing ZIP
browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').select ('Customers Enrolled')
sleep 2
browser.text_field(:id => 'ctl00_MainContent_txtLastName').set ('smith')
browser.text_field(:id => 'ctl00_MainContent_txtBillingZip').set ('19067')
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "CustNo"}
if
browser.text.include? "251115"
print "Search Customer Enrolled By Billing ZIP - Passed", "\n"
else
print "Search Customer Enrolled By Billing ZIP - Failed", "\n"
end
browser.button(:value => 'Reset').click
Watir::Waiter::wait_until {browser.text_field(:id => 'ctl00_MainContent_txtLastName').text.include? ""}
sleep 2
browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').select('Customers Not Yet Enrolled')
Watir::Waiter::wait_until {browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').option(:text, "Customers Not Yet Enrolled").selected}

#View an Enrollment Record's Details
#Expand / Collapse
browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').select ('Customers Enrolled')
sleep 2
browser.select_list(:id => 'ctl00_MainContent_ddlStatus').select ('Staging Valid For Enrollment')
browser.text_field(:id => 'ctl00_MainContent_txtFirstName').set ('GREGORY')
browser.text_field(:id => 'ctl00_MainContent_txtLastName').set ('smith')
browser.text_field(:id => 'ctl00_MainContent_txtBillingZip').set ('06902')
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "Expand All"}
sleep 3
browser.link(:text => 'Collapse All').click
sleep 3
if
browser.div(:id => 'Comments').visible?
print "Search Customer Collapse Enrollment Record's Details - Failed", "\n"
else
print "Search Customer Collapse Enrollment Record's Details - Passed", "\n"
end
sleep 3
browser.link(:text => 'Expand All').click
if
browser.div(:id => 'Comments').visible?
print "Search Customer Expand Enrollment Record's Details - Passed", "\n"
else
print "Search Customer Collapse Enrollment Record's Details - Failed", "\n"
end
sleep 3
browser.link(:text => 'Collapse All').click
sleep 3

#Inbound Data
browser.link(:id => 'ctl00_MainContent_lblInbound').click
sleep 3
if
browser.div(:id => 'InboundData').visible?
print "Search Customer Enrollment Record's Inbound Details - Passed", "\n"
else
print "Search Customer Enrollment Record's Inbound Details - Failed", "\n"
end
sleep 3
browser.link(:text => 'Collapse All').click

#Staging Data
browser.link(:id => 'ctl00_MainContent_lblStagingData').click
sleep 3
if
browser.div(:id => 'StagingData').visible?
print "Search Customer Enrollment Record's Staging Details - Passed", "\n"
else
print "Search Customer Enrollment Record's Staging Details - Failed", "\n"
end
sleep 3
browser.link(:text => 'Collapse All').click

#Customer Record
browser.link(:id => 'ctl00_MainContent_lblCustomer').click
sleep 3
if
browser.div(:id => 'CustomerData').visible?
print "Search Customer Enrollment Record's Customer Details - Passed", "\n"
else
print "Search Customer Enrollment Record's Customer Details - Failed", "\n"
end
sleep 3
browser.link(:text => 'Collapse All').click

#Comments
browser.link(:id => 'ctl00_MainContent_lblComments').click
sleep 3
if
browser.div(:id => 'Comments').visible?
print "Search Customer Enrollment Record's Comments Detail - Passed", "\n"
else
print "Search Customer Enrollment Record's Comments Detail - Failed", "\n"
end
sleep 3
browser.link(:text => 'Collapse All').click
browser.link(:id => 'ctl00_MainContent_HyperLink1').click

#Save Changes to Enrollment Record's Staging Data
#TEXAS RECORD
# Watir::Waiter::wait_until {browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').option(:text, "Customers Not Yet Enrolled").selected}
# browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').select ('Customers Enrolled')
# sleep 5
# browser.text_field(:id => 'ctl00_MainContent_txtFirstName').set ('HIROMI')
# browser.text_field(:id => 'ctl00_MainContent_txtLastName').set ('Smith')
# browser.text_field(:id => 'ctl00_MainContent_txtBillingZip').set ('77077')
# browser.button(:value => 'Search').click
# Watir::Waiter::wait_until {browser.text.include? "Expand All"}
# sleep 3
# browser.link(:text => 'Collapse All').click
# sleep 3
# browser.link(:id => 'ctl00_MainContent_lblStagingData').click
# Watir::Waiter::wait_until {browser.div(:id => 'StagingData').visible?}
# browser.select_list(:id => 'ctl00_MainContent_ValidationPanel1_ddlStatus').select ('Premise Review Pending')
# browser.button(:id => 'ctl00_MainContent_ValidationPanel1_btnChangeStatus').click
# sleep 5
# if
# browser.text.include? "This record with Utility Acct #1008901023810572260100 has changed status"
# print "Save Changes to Enrollment Record's Staging Data - Passed", "\n"
# else
# print "Save Changes to Enrollment Record's Staging Data - Failed", "\n"
# end
# sleep 3
# browser.select_list(:id => 'ctl00_MainContent_ValidationPanel1_ddlStatus').select ('Premise New')
# browser.button(:id => 'ctl00_MainContent_ValidationPanel1_btnChangeStatus').click
# Watir::Waiter::wait_until {browser.text.include? 'This record with Utility Acct #1008901023810572260100 has changed status'}
# browser.link(:id => 'ctl00_MainContent_HyperLink1').click

#Save Changes to Enrollment Record's Customer Data
# Watir::Waiter::wait_until {browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').option(:text, "Customers Not Yet Enrolled").selected}
# browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').select ('Customers Enrolled')
# sleep 7
# browser.text_field(:id => 'ctl00_MainContent_txtFirstName').set ('HIROMI')
# browser.text_field(:id => 'ctl00_MainContent_txtLastName').set ('Smith')
# browser.text_field(:id => 'ctl00_MainContent_txtBillingZip').set ('77077')
# browser.button(:value => 'Search').click
# Watir::Waiter::wait_until {browser.text.include? "Expand All"}
# sleep 3
# browser.link(:text => 'Collapse All').click
# sleep 3
# browser.link(:id => 'ctl00_MainContent_lblCustomer').click
# Watir::Waiter::wait_until {browser.div(:id => 'CustomerData').visible?}
# browser.select_list(:id => 'ctl00_MainContent_ValidationPanel3_ddlStatus').select ('Canceled per Cust Request')
# browser.button(:id => 'ctl00_MainContent_ValidationPanel3_btnChangeStatus').click
# sleep 5
# if
# browser.text.include? "This record with Utility Acct #1008901023810572260100 has changed status"
# print "Save Changes to Enrollment Record's Customer Data - Passed", "\n"
# else
# print "Save Changes to Enrollment Record's Customer Data - Failed", "\n"
# end
# sleep 3
# browser.select_list(:id => 'ctl00_MainContent_ValidationPanel3_ddlStatus').select ('Under Review')
# browser.button(:id => 'ctl00_MainContent_ValidationPanel3_btnChangeStatus').click
# Watir::Waiter::wait_until {browser.text.include? 'This record with Utility Acct #1008901023810572260100 has changed status'}
# browser.link(:id => 'ctl00_MainContent_HyperLink1').click

#Add a Comment to an Enrollment Record
Watir::Waiter::wait_until {browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').option(:text, "Customers Not Yet Enrolled").selected}
browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').select ('Customers Enrolled')
sleep 7
browser.text_field(:id => 'ctl00_MainContent_txtFirstName').set ('HIROMI')
browser.text_field(:id => 'ctl00_MainContent_txtLastName').set ('smith')
browser.text_field(:id => 'ctl00_MainContent_txtBillingZip').set ('77077')
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "Expand All"}
sleep 3
browser.link(:text => 'Collapse All').click
sleep 3
browser.link(:id => 'ctl00_MainContent_lblComments').click
Watir::Waiter::wait_until {browser.div(:id => 'Comments').visible?}
sleep 2
browser.text_field(:id => /ctl00_MainContent_CommentPanel1_gvComments_ct*/).set("test add a comment")
browser.button(:value,"Add New").click
sleep 5
if
browser.text.include? "test add a comment"
print "Add a Comment to an Enrollment Record - Passed", "\n"
else
print "Add a Comment to an Enrollment Record - Failed", "\n"
end
browser.link(:id => 'ctl00_MainContent_HyperLink1').click

=begin
#Search Customers Enrolled By Enroll Type Move In
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
print "Search Customer Enrolled By Enroll Type - Passed", "\n"
else
print "Search Customer Enrolled By Enroll Type - Failed", "\n"
end
browser.link(:id => 'ctl00_MainContent_HyperLink1').click
sleep 2

#Search Customers Enrolled By Enroll Type On Cycle
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
print "Search Customer Enrolled By Enroll Type - Passed", "\n"
else
print "Search Customer Enrolled By Enroll Type - Failed", "\n"
end
browser.link(:id => 'ctl00_MainContent_HyperLink1').click
sleep 2
=end

browser.close
