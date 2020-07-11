require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://ep-qa/Operations/OpsEnrollmentQueue.aspx'

#Filter on Enrollment Rejects By State
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'NY').select
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').when_present.click
sleep 7
if
browser.text.include? "339225199993"
print "Filter Enrollment Rejects by State - Passed", "\n"
else
print "Filter Enrollment Rejects by State - Failed", "\n"
end
sleep 5
browser.button(:value => 'Reset').click
sleep 10

#Filter on Enrollment Rejects By User
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select('Galabinski, Amy')
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').when_present.click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text => 'Filter').when_present.click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '49').select
browser.button(:value => 'Filter').when_present.click
sleep 7
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').option(:text, 'Galabinski, Amy').selected
print "Filter Enrollment Rejects by User - Passed", "\n"
else
print "Filter Enrollment Rejects by User  - Failed", "\n"
end
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select("")
browser.button(:value => 'Assign').when_present.click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click

