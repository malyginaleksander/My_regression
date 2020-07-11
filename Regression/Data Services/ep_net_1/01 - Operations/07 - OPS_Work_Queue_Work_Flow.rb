require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Operations/OpsEnrollmentQueue.aspx'

#Reprocess a Record
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set ('339225199222')
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 1 of 1"}
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_divValidationPanel').exists?}
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_btnReprocess').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been reprocessed."}
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsSearchRecords').click
browser.text_field(:id => 'ctl00_MainContent_txtUtilAccountNumber').set("339225199222")
browser.button(:value => 'Search').click
browser.link(:text => 'Collapse All').click
browser.link(:id => 'ctl00_MainContent_lblInbound').click
if
browser.text.include? "Ready To Reprocess"
print "Reprocess a Record - Passed", "\n"
else
print "Reprocess a Record - Failed", "\n"
end
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsWorkQueue').click
sleep 2

#Change Records Status to Dead
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set ('339225199333')
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 1 of 1"}
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_divValidationPanel').exists?}
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlStatus').select ('Dead')
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_btnChangeStatus').click
Watir::Waiter::wait_until {browser.text.include? "The status has been changed for Utility Account Number 339225199333"}
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsSearchRecords').click
sleep 2
browser.text_field(:id => 'ctl00_MainContent_txtUtilAccountNumber').set("339225199333")
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "Collapse All"}
browser.link(:text => 'Collapse All').click
browser.link(:id => 'ctl00_MainContent_lblInbound').click
if
browser.text.include? "Dead"
print "Change Records Status to Dead - Passed", "\n"
else
print "Change Records Status to Dead - Failed", "\n"
end
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsWorkQueue').click
sleep 2

#Change Records Status to Canceled per Enrollee Request
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set ('339225199444')
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 1 of 1"}
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_divValidationPanel').exists?}
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlStatus').select ('Canceled per Enrollee Request')
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_btnChangeStatus').click
Watir::Waiter::wait_until {browser.text.include? "The status has been changed for Utility Account Number 339225199444"}
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsSearchRecords').click
browser.text_field(:id => 'ctl00_MainContent_txtUtilAccountNumber').set('339225199444')
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "Collapse All"}
browser.link(:text => 'Collapse All').click
browser.link(:id => 'ctl00_MainContent_lblInbound').click
if
browser.text.include? "Canceled per Enrollee Request"
print "Change Records Status to Cancelled per Enrollee Request - Passed", "\n"
else
print "Change Records Status to Cancelled per Enrollee Request - Failed", "\n"
end
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsWorkQueue').click
sleep 2

#Change Records Status to Customer Service Follow-up
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set ('339225199555')
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 1 of 1"}
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_divValidationPanel').exists?}
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlStatus').select ('Customer Service Follow-Up')
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_btnChangeStatus').click
Watir::Waiter::wait_until {browser.text.include? "The status has been changed for Utility Account Number 339225199555"}
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsSearchRecords').click
browser.text_field(:id => 'ctl00_MainContent_txtUtilAccountNumber').set('339225199555')
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "Collapse All"}
browser.link(:text => 'Collapse All').click
browser.link(:id => 'ctl00_MainContent_lblInbound').click
if
browser.text.include? "Customer Service Follow-Up"
print "Change Records Status to Customer Service Follow-up - Passed", "\n"
else
print "Change Records Status to Customer Service Follow-up - Failed", "\n"
end
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsWorkQueue').click
sleep 2

#Confirm an Enrollment as a Duplicate
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set ('10443720002070654')
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 1 of 1"}
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_divValidationPanel').exists?}
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_DuplicatePanel1_btnSelectMatch').click
Watir::Waiter::wait_until {browser.text.include? "This record with Utility Acct #10443720002070654 has been confirmed as a duplicate."}
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsSearchRecords').click
browser.text_field(:id => 'ctl00_MainContent_txtUtilAccountNumber').set('10443720002070654')
browser.button(:value => 'Search').click
if
browser.text.include? "Thomas"
print "Confirm an Enrollment as a Duplicate - Passed", "\n"
else
print "Confirm an Enrollment as a Duplicate - Failed", "\n"
end
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsWorkQueue').click
sleep 2

#Confirm an Enrollment is not a Duplicate
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set ('10443720002070654')
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 1 of 1"}
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_divValidationPanel').exists?}
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_DuplicatePanel1_btnNoMatch').click
Watir::Waiter::wait_until {browser.text.include? "This reject has been marked as Not a Duplicate"}
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set ('10443720002070654')
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
browser.button(:value => 'Search').click
if
browser.text.include? "Duplicate Within File"
print "Confirm an Enrollment Is not a Duplicate - Passed", "\n"
else
print "Confirm an Enrollment Is not a Duplicate - Failed", "\n"
end
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsWorkQueue').click
sleep 2

#Send a Record to Customer Service
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set ('10443720006690670')
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 1 of 1"}
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_divValidationPanel').exists?}
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_DuplicatePanel1_btnCS').click
Watir::Waiter::wait_until {browser.text.include? "This record with Utility Acct #10443720006690670 has been sent to Customer Service for Follow-Up."}
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsSearchRecords').click
browser.text_field(:id => 'ctl00_MainContent_txtUtilAccountNumber').set('10443720006690670')
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "Customer Service Follow-Up"}
if
browser.text.include? "Customer Service Follow-Up"
print "Send a Record to Customer Service - Passed", "\n"
else
print "Send a Record to Customer Service - Failed", "\n"
end
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsWorkQueue').click
sleep 2
=begin
#Select Possible Match Record as a Match
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set ('10443720003174406')
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 1 of 1"}
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_divValidationPanel').exists?}
browser.checkbox(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_AccountMatchingPanel1_gvMatches_ctl02_chk1').set
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_AccountMatchingPanel1_btnSelectMatch').click
Watir::Waiter::wait_until {browser.text.include? "This record with Utility Acct #10443720003174406 has been marked as a match."}
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsSearchRecords').click
browser.text_field(:id => 'ctl00_MainContent_txtUtilAccountNumber').set('10443720003174406')
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "Collapse All"}
if
browser.text.include? "Assigned Master"
print "Possible Match Record as a Match - Passed", "\n"
else
print "Possible Match Record as a Match - Failed", "\n"
end
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsWorkQueue').click
sleep 2

#Select Possible Match Record as Not a Match
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set ('1008901017631574489100')
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.text.include? "Total Records:1 - Showing Page: 1 of 1"}
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_divValidationPanel').exists?}
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_AccountMatchingPanel1_btnNoMatch').click
Watir::Waiter::wait_until {browser.text.include? "This record with Utility Acct #1008901017631574489100 has been marked as Not a Match."}
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsSearchRecords').click
browser.text_field(:id => 'ctl00_MainContent_txtUtilAccountNumber').set('1008901017631574489100')
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "Collapse All"}
if
browser.text.include? "Ready To Reprocess"
print "Possible Match Record as a Match - Passed", "\n"
else
print "Send a Record to Customer Service - Failed", "\n"
end
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsWorkQueue').click
sleep 2
=end

browser.close