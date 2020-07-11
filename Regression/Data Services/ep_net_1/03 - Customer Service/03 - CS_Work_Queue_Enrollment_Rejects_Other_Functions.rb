require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/CustomerService/CustomerServiceQueue.aspx'

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
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 4 of 4"}
if
browser.text.include? "Showing Page: 2 of 2"
print "Move to Last Page of Queue - Passed", "\n"
else
print "Move to Last Page of Queue - Failed", "\n"
end

#Move to First Page of Queue
####### UPDATE PAGE NUMBERS TO REFLECT WORK QUEUE)#######
browser.link(:id => 'ctl00_MainContent_first').click
Watir::Waiter::wait_until {browser.text.include? "Showing Page: 1 of "}
if
browser.text.include? "Showing Page: 1 of"
print "Move to First Page of Queue - Passed", "\n"
else
print "Move to First Page of Queue - Failed", "\n"
end
sleep 2

#Add a Comment to an Enrollment Record
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
browser.text_field(:id => /ctl00_MainContent_dlStagingRecords_ctl01_CommentPanel1_gvComments_ct*/).set ('adding a comment')
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_CommentPanel1_btnAdd').click
Watir::Waiter::wait_until {browser.text.include? "Your comment has been added."}
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
if
browser.text.include? "adding a comment"
print "Add a Comment to an Enrollment Record - Passed", "\n"
else
print "Add a Comment to an Enrollment Record - Failed", "\n"
end
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnReset').click
sleep 10

#Create a Follow-Up Reminder for an Enrollment Record
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
browser.text_field(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_CreateFollowUp1_txtFollowUpDate').set("12/31/2020")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_CreateFollowUp1_btnFollowUp').click
Watir::Waiter::wait_until {browser.text.include? "The Follow-Up has been Created."}
if
browser.text.include? "The Follow-Up has been Created."
if
browser.text.include? "12-31-2020"
print "Followup Date Created - Passed", "\n"
else
print "Followup Date Created - Failed", "\n"
end
end

#browser.close