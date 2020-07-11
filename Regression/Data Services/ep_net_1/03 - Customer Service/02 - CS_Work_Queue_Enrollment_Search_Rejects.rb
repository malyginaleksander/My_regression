require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/CustomerService/CustomerServiceQueue.aspx'

#Search Enrollment Rejects by Customer Last Name
browser.link(:text => 'Search').click
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtLastName').set ('PEREZ')
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
sleep 10
if
browser.span(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_Label3').text.include? "PEREZ"
print "Search Enrollment Rejects by Customer Last Name - Passed", "\n"
else
print "Search Enrollment Rejects by Customer Last Name - Failed", "\n"
end
browser.button(:value => 'Reset').click
sleep 10

#Search Enrollment Rejects by Customer Service Phone Number
browser.link(:text => 'Search').click
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtSvcPhone').set ('4132544554')
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
sleep 10
if
browser.text.include? "54931427058"
print "Search Enrollment Rejects by Customer Phone Number - Passed", "\n"
else
print "Search Enrollment Rejects by Customer Phone Number - Failed", "\n"
end
browser.button(:value => 'Reset').click
sleep 10

#Search Enrollment Rejects by Customer Service Utility Account Number
browser.link(:text => 'Search').click
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set("8893961001")
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
sleep 10
if
browser.text.include? "8893961001"
print "Search Enrollment Rejects by Utility Account Number - Passed", "\n"
else
print "Search Enrollment Rejects by Utility Account Number - Failed", "\n"
end
browser.button(:value => 'Reset').click
sleep 10

#Search Enrollment Rejects by Customer Service Energy Plus Id
browser.link(:text => 'Search').click
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtEnergyPlusId').set("1517887")
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
sleep 10
if
browser.text.include? "8893961001"
print "Search Enrollment Rejects by Energy Plus Id - Passed", "\n"
else
print "Search Enrollment Rejects by Energy Plus Id - Failed", "\n"
end
browser.button(:value => 'Reset').click
sleep 10

#Save Enrollment Record's Meta-Data after Modification
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'MA').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 10
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
browser.text_field(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_txtServiceAddress2').set ("update meta data")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_btnSaveValidationChanges').click
Watir::Waiter::wait_until {browser.text.include? " Your data has been saved"}
if
browser.text.include? "Your data has been saved"
print "Save Enrollment Record's Meta-Data after Modification - Passed", "\n"
else
print "Save Enrollment Record's Meta-Data after Modification - Failed", "\n"
end

browser.close