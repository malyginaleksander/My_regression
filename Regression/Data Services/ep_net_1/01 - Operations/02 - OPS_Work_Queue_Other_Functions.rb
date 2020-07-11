require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Operations/OpsEnrollmentQueue.aspx'

#Save Record's Meta-data after Modification
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'NJ').select
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 12
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.span(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_lblValidation').exists?}
browser.text_field(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_txtServiceAddress2').set ('Test Record Update')
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_btnSaveValidationChanges').click
sleep 20
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'NJ').select
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 12
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.span(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_lblValidation').exists?}
if
browser.text.include? "Test Record Update"
print "Meta-data updated - Passed", "\n"
else
print "Meta-data updated - Failed", "\n"
end
browser.text_field(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_txtServiceAddress2').set ('')
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_btnSaveValidationChanges').click
sleep 20

#Create a Follow-up Reminder for a Record
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
sleep 10
browser.text_field(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_CreateFollowUp1_txtFollowUpDate').set("12/31/2112")
sleep 1
browser.button(:value => 'Create Follow Up Reminder').click
Watir::Waiter::wait_until {browser.text.include? "The Follow-Up has been Created."}
if
browser.text.include? "The Follow-Up has been Created."
if
browser.text.include? "12-31-2112"
print "Follow-up Date Created - Passed", "\n"
else
print "Follow-up Date Created - Failed", "\n"
end
end

#Add a Comment to a Record
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'NJ').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').option(:value, '9000').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 12
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
sleep 2
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_CommentPanel1_gvComments').exists?}
browser.text_field(:id => /ctl00_MainContent_dlStagingRecords_ctl01_CommentPanel1_gvComments_ct*/).set("test add a comment")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_CommentPanel1_btnAdd').click
Watir::Waiter::wait_until {browser.text.include? "The comment has been added."}
if
browser.text.include? "test add a comment"
print "Add a Comment to an Enrollment Record - Passed", "\n"
else
print "Add a Comment to an Enrollment Record - Failed", "\n"
end
browser.button(:value => 'Reset').click
sleep 10

#Move to Next Page of Queue
####### UPDATE PAGE NUMBERS TO REFLECT WORK QUEUE)#######
browser.link(:id => 'ctl00_MainContent_next').click
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 2"}
if
browser.text.include? "Showing Page: 2 of"
print "Move to Next Page of Queue - Passed", "\n"
else
print "Move to Next Page of Queue - Failed", "\n"
end

#Move to Previous Page of Queue
####### UPDATE PAGE NUMBERS TO REFLECT WORK QUEUE)#######
browser.link(:id => 'ctl00_MainContent_prev').click
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 1"}
if
browser.text.include? "Showing Page: 1 of"
print "Move to Previous Page of Queue - Passed", "\n"
else
print "Move to Previous Page of Queue - Failed", "\n"
end

#Move to Last Page of Queue
####### UPDATE PAGE NUMBERS TO REFLECT WORK QUEUE)#######
browser.link(:id => 'ctl00_MainContent_last').click
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 28"}
if
browser.text.include? "Showing Page: 28"
print "Move to Last Page of Queue - Passed", "\n"
else
print "Move to Last Page of Queue - Failed", "\n"
end

#Move to First Page of Queue
####### UPDATE PAGE NUMBERS TO REFLECT WORK QUEUE)#######
browser.link(:id => 'ctl00_MainContent_first').click
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 1"}
if
browser.text.include? "Showing Page: 1 of"
print "Move to First Page of Queue - Passed", "\n"
else
print "Move to First Page of Queue - Failed", "\n"
end
sleep 2

browser.close
