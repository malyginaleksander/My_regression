require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Operations/OpsEnrollmentQueue.aspx'

#Search Enrollment Queue by Last Name
browser.text_field(:id, "ctl00_MainContent_DropDownFilter1_txtLastName").set("RONG")
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
sleep 10
if
browser.span(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_Label3').text.include? "RONG"
print "Search Enrollment Queue by Last Name - Passed", "\n"
else
print "Search Enrollment Queue by Last Name - Failed", "\n"
end
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnReset').click
sleep 10

#Search Enrollment Queue by Service Phone Number
browser.text_field(:id, "ctl00_MainContent_DropDownFilter1_txtSvcPhone").set("9722612025")
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
sleep 10
if
browser.text.include? "339225199993"
print "Search Enrollment Queue by Service Phone Number - Passed", "\n"
else
print "Search Enrollment Queue by Service Phone Number - Failed", "\n"
end
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnReset').click
sleep 10

#Search Enrollment Queue by Utility Account Number
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set("412223343500039")
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
sleep 10
if
browser.text.include? "412223343500039"
print "Search Enrollment Queue by Utility Account Number - Passed", "\n"
else
print "Search Enrollment Queue by Utility Account Number - Failed", "\n"
end
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnReset').click
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnReset').when_present.click

#Search Enrollment Queue by Energy Plus ID
##############   UPDATE EP ID #####################
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtEnergyPlusId').set("1438816") #UPDATE
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
sleep 10
if
browser.text.include? "412223343500039"
print "Search Enrollment Queue by Energy Plus ID - Passed", "\n"
else
print "Search Enrollment Queue by Energy Plus ID - Failed", "\n"
end
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnReset').click
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnReset').when_present.click
sleep 7

browser.close
