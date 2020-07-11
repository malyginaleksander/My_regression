require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/CustomerService/CustomerServiceQueue.aspx'
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_updCSRejects').exists?}

##################################################
#Copy account numbers from a NJ, NY, MA State into script before running#
##################################################

#Reprocess an Enrollment Record
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set("54143886059")
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
sleep 10
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 1 of 1"}
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_btnReprocess').click
Watir::Waiter::wait_until {browser.text.include? "Your record has been resubmitted for processing."}
browser.goto 'http://epnet1.pt.nrgpl.us/Operations/SearchEnrollments.aspx'

sleep 2
browser.text_field(:id => 'ctl00_MainContent_txtUtilAccountNumber').set("54143886059")
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "Return to Search form"}
if
browser.text.include? "Collapse All"
browser.link(:id => 'ctl00_MainContent_lblInbound').click
end

if
browser.text.include? "Ready To Reprocess"
print "Reprocess an Enrollment Record - Passed", "\n"
else
print "Reprocess an Enrollment Record - Failed", "\n"
end
browser.link(:text => 'Collapse All').click
sleep 2
#browser.goto 'http://epnet1.pt.nrgpl.us/CustomerService/CustomerServiceQueue.aspx'
browser.goto 'http://epnet1.pt.nrgpl.us/CustomerService/CustomerServiceQueue.aspx'
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_updCSRejects').exists?}

#Change Enrollment Record's status to Dead
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set("54873076079")
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
sleep 10
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 1 of 1"}
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlStatus').select("Dead")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_btnChangeStatus').click
Watir::Waiter::wait_until {browser.text.include? "The status has been changed for Utility Account Number 54873076079"}
browser.goto 'http://epnet1.pt.nrgpl.us/Operations/SearchEnrollments.aspx'
sleep 2
browser.text_field(:id => 'ctl00_MainContent_txtUtilAccountNumber').set("54873076079")
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "Return to Search form"}
if
browser.text.include? "Collapse All"
browser.link(:id => 'ctl00_MainContent_lblInbound').click
end

if
browser.text.include? "Ready To Reprocess"
print "Change Enrollment Record's status to Dead - Passed", "\n"
else
print "Change Enrollment Record's status to Dead - Failed", "\n"
end
browser.link(:text => 'Collapse All').click
sleep 2
browser.goto 'http://epnet1.pt.nrgpl.us/CustomerService/CustomerServiceQueue.aspx'
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_updCSRejects').exists?}

#Change Records Status to Cancelled per Enrollee Request
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set("54774981070")
sleep 10
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
sleep 10
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 1 of 1"}
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlStatus').select("Canceled per Enrollee Request")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_btnChangeStatus').click
Watir::Waiter::wait_until {browser.text.include? "The status has been changed for Utility Account Number 54774981070"}
browser.goto 'http://epnet1.pt.nrgpl.us/Operations/SearchEnrollments.aspx'
sleep 2
browser.text_field(:id => 'ctl00_MainContent_txtUtilAccountNumber').set("54774981070")
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "Return to Search form"}
if
browser.text.include? "Collapse All"
browser.link(:id => 'ctl00_MainContent_lblInbound').click
end

if
browser.text.include? "Canceled per Enrollee Request"
print "Change Records Status to Cancelled per Enrollee Request - Passed", "\n"
else
print "Change Records Status to Cancelled per Enrollee Request - Failed", "\n"
end
browser.link(:text => 'Collapse All').click
sleep 2
browser.goto 'http://epnet1.pt.nrgpl.us/CustomerService/CustomerServiceQueue.aspx'
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_updCSRejects').exists?}

#Change Records Status to Customer Service Follow-up
browser.text_field(:id => 'ctl00_MainContent_DropDownFilter1_txtUtilityAccountNumber').set("54924416019")
sleep 10
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnSearch').click
sleep 10
Watir::Waiter::wait_until {browser.text.include? "Total Records:1 - Showing Page: 1 of 1"}
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlStatus').select("Customer Service Follow-Up")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_btnChangeStatus').click
Watir::Waiter::wait_until {browser.text.include? "The status has been changed for Utility Account Number 54924416019"}
browser.goto 'http://epnet1.pt.nrgpl.us/Operations/SearchEnrollments.aspx'
sleep 2
browser.text_field(:id => 'ctl00_MainContent_txtUtilAccountNumber').set("54924416019")
browser.button(:value => 'Search').click
if
browser.text.include? "Collapse All"
browser.link(:id => 'ctl00_MainContent_lblInbound').click
end

if
browser.text.include? "Customer Service Follow-Up"
print "Change Records Status to Customer Service Follow-up - Passed", "\n"
else
print "Change Records Status to Customer Service Follow-up - Failed", "\n"
end
browser.link(:text => 'Collapse All').click
sleep 2

browser.close
