require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Operations/OpsEnrollmentQueue.aspx'

#Filter on Enrollment Rejects By State
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'NJ').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 15
if
browser.text.include? "339225199993"
print "Filter Enrollment Rejects by State - Passed", "\n"
else
print "Filter Enrollment Rejects by State - Failed", "\n"
end
sleep 5
browser.button(:value => 'Reset').click
sleep 20

#Filter on Enrollment Rejects By User
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select('Stinson, Tom')
sleep 2
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text => 'Filter').click
sleep 1
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '34').select
sleep 2
browser.button(:value => 'Filter').click
sleep 15
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').option(:text, 'Stinson, Tom').selected
print "Filter Enrollment Rejects by User - Passed", "\n"
else
print "Filter Enrollment Rejects by User  - Failed", "\n"
end
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select("")
sleep 2
browser.button(:value => 'Assign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter on Enrollment Rejects By MID
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').option(:value, 'D2D1').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 15
if
browser.text.include? "403235236000001"
print "Filter Enrollment Rejects by MID - Passed", "\n"
else
print "Filter Enrollment Rejects by MID - Failed", "\n"
end
sleep 5
browser.button(:value => 'Reset').click
sleep 20

#Filter on Enrollment Rejects By Reject Type
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').option(:value, 'Requires Review').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 15
if
browser.span(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_Label5').text.include? "Requires Review"
print "Filter Enrollment Rejects by Reject Type - Passed", "\n"
else
print "Filter Enrollment Rejects by Reject Type - Failed", "\n"
end
sleep 5
browser.button(:value => 'Reset').click
sleep 20

#Filter on Enrollment Rejects By State And User
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'NJ').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 15
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select('Stinson, Tom')
sleep 2
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'NJ').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '34').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 15
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
sleep 20
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').option(:text, 'Stinson, Tom').selected
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlServiceState').option(:text, 'NJ').selected
print "Filter Enrollment Rejects by State and User - Passed", "\n"
else
print "Filter Enrollment Rejects by State and User - Failed", "\n"
end
end
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select("")
sleep 2
browser.button(:value => 'Assign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter on Enrollment Rejects By State And MID
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'NJ').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').option(:value, '9000').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 15
if
browser.text.include? "PE000009132720532471"
print "Filter Enrollment Rejects by State and MID - Passed", "\n"
else
print "Filter Enrollment Rejects by State and MID - Failed", "\n"
end
sleep 5
browser.button(:value => 'Reset').click
sleep 20

#Filter on Enrollment Rejects By State and Reject Type
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'NJ').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').option(:value, 'Duplicate Within File').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 15
browser.link(:text, "Sale Date").click
sleep 5
browser.link(:text, "Sale Date").click
sleep 5
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
sleep 15
if
browser.text.include? "PE000009132720532471"
print "Filter Enrollment Rejects by State and Reject Type - Passed", "\n"
else
print "Filter Enrollment Rejects by State and Reject Type - Failed", "\n"
end
sleep 5
browser.button(:value => 'Reset').click
sleep 20

#Filter on Enrollment Rejects By User and MID
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').option(:value, 'D2D1').select
sleep 3
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 15
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select('Stinson, Tom')
sleep 2
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').option(:value, 'D2D1').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '34').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 15
if
browser.text.include? "403235236000001"
print "Filter Enrollment Rejects by User and MID - Passed", "\n"
else
print "Filter Enrollment Rejects by User and MID  - Failed", "\n"
end
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select("")
sleep 2
browser.button(:value => 'Assign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter on Enrollment Rejects By User and Reject Type
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').option(:value, 'Requires Review').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 20
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select('Stinson, Tom')
sleep 2
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '34').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').option(:value, 'Requires Review').select
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
sleep 20
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
sleep 15
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').option(:text, 'Stinson, Tom').selected
if
browser.span(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_Label5').text.include? "Requires Review"
print "Filter Enrollment Rejects by User and Reject Type - Passed", "\n"
else
print "Filter Enrollment Rejects by User and Reject Type  - Failed", "\n"
end
end
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select("")
sleep 2
browser.button(:value => 'Assign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter on Enrollment Rejects By MID and Reject Type
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').option(:value, 'D2D1').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').option(:value, 'Requires Review').select
sleep 2
browser.button(:value => 'Filter').click
sleep 15
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
sleep 15
if
browser.span(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_Label5').text.include? "Requires Review"
if
browser.text.include? "D2D1"
print "Filter Enrollment Rejects by MID and Reject Type - Passed", "\n"
else
print "Filter Enrollment Rejects by MID and Reject Type  - Failed", "\n"
end
end
sleep 5
browser.button(:value => 'Reset').click
sleep 20

#Filter on Enrollment Rejects By State, User And MID
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'NJ').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').option(:value, '9000').select
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 20
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select('Stinson, Tom')
sleep 2
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'NJ').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').option(:value, '9000').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '34').select
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 15
if
browser.text.include? "PE000009132720532471"
print "Filter Enrollment Rejects by State, User and MID - Passed", "\n"
else
print "Filter Enrollment Rejects by State, User and MID  - Failed", "\n"
end
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select("")
sleep 2
browser.button(:value => 'Assign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter on Enrollment Rejects By State, MID And Reject Type
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'NY').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').option(:value, 'D2D1').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').option(:value, 'Requires Review').select
sleep 5
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 15
if
browser.text.include? "403235236000001"
print "Filter Enrollment Rejects by State, MID and Reject Type - Passed", "\n"
else
print "Filter Enrollment Rejects by State, MID and Reject Type  - Failed", "\n"
end
sleep 5
browser.button(:value => 'Reset').click
sleep 20

#Filter on Enrollment Rejects By State, User And Reject Type
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'PA').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').option(:value, 'Requires Review').select
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 20
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select('Stinson, Tom')
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'PA').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').option(:value, 'Requires Review').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '34').select
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 20
if
browser.text.include? "6000668165002"
print "Filter Enrollment Rejects by State, User and Reject Type - Passed", "\n"
else
print "Filter Enrollment Rejects by State, User and Reject Type  - Failed", "\n"
end
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select("")
sleep 2
browser.button(:value => 'Assign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter on Enrollment Rejects By User, MID And Reject Type
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').option(:value, '9000').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').option(:value, 'Duplicate Within File').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 15
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select('Stinson, Tom')
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '34').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').option(:value, '9000').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').option(:value, 'Duplicate Within File').select
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 15
if
browser.text.include? "PE000009132720532471"
print "Filter Enrollment Rejects by User, MID and Reject Type - Passed", "\n"
else
print "Filter Enrollment Rejects by User, MID and Reject Type  - Failed", "\n"
end
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select("")
sleep 2
browser.button(:value => 'Assign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter on Enrollment Rejects By State, User, MID And Reject Type
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'NJ').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').option(:value, '9000').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').option(:value, 'Duplicate Within File').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 20
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select('Stinson, Tom')
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text => 'Reset').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'NJ').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '34').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').option(:value, '9000').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').option(:value, 'Duplicate Within File').select
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 15
if
browser.text.include? "PE000009132720532471"
print "Filter Enrollment Rejects by State, User, MID and Reject Type - Passed", "\n"
else
print "Filter Enrollment Rejects by State, User, MID and Reject Type  - Failed", "\n"
end
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select("")
sleep 2
browser.button(:value => 'Assign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

browser.close
