require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/CustomerService/CustomerServiceQueue.aspx'

#Filter Enrollment Rejects By State
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'MA').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 10
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
if
browser.table(:xpath => '//*[@id="ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlServiceState"]').text.include? "MA"
print "Filter Enrollment Rejects by State - Passed", "\n"
else
print "Filter Enrollment Rejects by State - Failed", "\n"
end
browser.button(:value => 'Reset').click
sleep 20

#Filter Enrollment Rejects By User
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("Carder, Dave")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text, "Filter").click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '7').select
sleep 2
browser.button(:value => 'Filter').click
sleep 10
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').option(:text, 'Carder, Dave').selected
print "Filter Enrollment Rejects by User - Passed", "\n"
else
print "Filter Enrollment Rejects by User - Failed", "\n"
end
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter Enrollment Rejects By MID
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').option(:value, '9000').select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 7
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
if
browser.text.include? "9000"
print "Filter Enrollment Rejects by MID - Passed", "\n"
else
print "Filter Enrollment Rejects by MID - Failed", "\n"
end
browser.button(:value => 'Reset').click
sleep 20

#Filter Enrollment Rejects By Reject Type
browser.link(:text => 'Filter').click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').option(:value, /Requires Review*/).select
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 10
if
browser.span(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_Label5').text.include? "Requires Review"
print "Filter Enrollment Rejects by Reject Type - Passed", "\n"
else
print "Filter Enrollment Rejects by Reject Type - Failed", "\n"
end
browser.button(:value => 'Reset').click
sleep 20

#Filter Enrollment Rejects By state and User
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'MA').select
sleep 10
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 10
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("Carder, Dave")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text, "Filter").click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'MA').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '7').select
sleep 2
browser.button(:value => 'Filter').click
sleep 10
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
sleep 10
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').option(:text, 'Carder, Dave').selected
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlServiceState').option(:text, 'MA').selected
print "Filter Enrollment Rejects by State and User - Passed", "\n"
else
print "Filter Enrollment Rejects by State and User - Failed", "\n"
end
end
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter Enrollment Rejects By state and MID
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'MA').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').select(/9000*/)
sleep 10
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 10
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
if
browser.text.include? "9000"
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlServiceState').option(:text, 'MA').selected
print "Filter Enrollment Rejects by State and MID - Passed", "\n"
else
print "Filter Enrollment Rejects by State and MID - Failed", "\n"
end
end
sleep 2
browser.button(:value => 'Reset').click
sleep 20

#Filter Enrollment Rejects By state and Reject
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'MA').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').select(/Requires Review*/)
sleep 10
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 10
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
if
browser.text.include? "Requires Review"
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlServiceState').option(:text, 'MA').selected
print "Filter Enrollment Rejects by State and Reject - Passed", "\n"
else
print "Filter Enrollment Rejects by State and Reject - Failed", "\n"
end
end
sleep 2
browser.button(:value => 'Reset').click
sleep 20

#Filter Enrollment Rejects By User and MID
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').select(/9000*/)
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 10
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("Carder, Dave")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text, "Filter").click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '7').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').select(/9000*/)
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
if
browser.text.include? "9000"
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').option(:text, 'Carder, Dave').selected
print "Filter Enrollment Rejects by User and MID - Passed", "\n"
else
print "Filter Enrollment Rejects by User and MID - Failed", "\n"
end
end
sleep 2
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter Enrollment Rejects By User and Reject
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').select(/Requires Review*/)
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 10
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("Carder, Dave")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text, "Filter").click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '7').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').select(/Requires Review*/)
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
if
browser.text.include? "Requires Review"
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').option(:text, 'Carder, Dave').selected
print "Filter Enrollment Rejects by User and Reject - Passed", "\n"
else
print "Filter Enrollment Rejects by User and Reject - Failed", "\n"
end
end
sleep 2
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter Enrollment Rejects By MID and Reject
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').select(/9000*/)
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').select(/Requires Review*/)
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 10
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
if
browser.text.include? "Requires Review"
if
browser.text.include? "9000"
print "Filter Enrollment Rejects by MID and Reject - Passed", "\n"
else
print "Filter Enrollment Rejects by MID and Reject - Failed", "\n"
end
end
sleep 2
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter Enrollment Rejects By state, User and MID
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'MA').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').select(/9000*/)
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 10
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("Carder, Dave")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text, "Filter").click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'MA').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').select(/9000*/)
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '7').select
sleep 2
browser.button(:value => 'Filter').click
sleep 10
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
if
browser.text.include? "9000"
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').option(:text, 'Carder, Dave').selected
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlServiceState').option(:text, 'MA').selected
print "Filter Enrollment Rejects by state, User and MID - Passed", "\n"
else
print "Filter Enrollment Rejects by state, User and MID - Failed", "\n"
end
end
end
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter Enrollment Rejects By state, MID and Reject Type
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'MA').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').select(/9000*/)
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').select(/Requires Review*/)
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 10
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
if
browser.text.include? "9000"
if
browser.text.include? "Requires Review"
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlServiceState').option(:text, 'MA').selected
print "Filter Enrollment Rejects by state, MID and Reject Type - Passed", "\n"
else
print "Filter Enrollment Rejects by state, MID and Reject Type - Failed", "\n"
end
end
end
browser.button(:value => 'Reset').click
sleep 20

#Filter Enrollment Rejects By state, User and Reject Type
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'MA').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').select(/Requires Review*/)
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 10
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("Carder, Dave")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text, "Filter").click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'MA').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').select(/Requires Review*/)
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '7').select
sleep 2
browser.button(:value => 'Filter').click
sleep 10
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').option(:text, 'Carder, Dave').selected
if
browser.text.include? "Requires Review"
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlServiceState').option(:text, 'MA').selected
print "Filter Enrollment Rejects by state, User and Reject Type - Passed", "\n"
else
print "Filter Enrollment Rejects by state, User and Reject Type - Failed", "\n"
end
end
end
sleep 2
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter Enrollment Rejects By User, MID and Reject Type
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').select(/Requires Review*/)
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').select(/9000*/)
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 10
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("Carder, Dave")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text, "Filter").click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').select(/Requires Review*/)
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').select(/9000*/)
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '7').select
sleep 2
browser.button(:value => 'Filter').click
sleep 10
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
if
browser.text.include? "9000"
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').option(:text, 'Carder, Dave').selected
if
browser.text.include? "Requires Review"
print "Filter Enrollment Rejects by User, MID and Reject Type - Passed", "\n"
else
print "Filter Enrollment Rejects by User, MID and Reject Type - Failed", "\n"
end
end
end
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

#Filter Enrollment Rejects By State, User, MID and Reject Type
browser.link(:text => 'Filter').click
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'MA').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').select(/Requires Review*/)
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').select(/SOLX*/)
sleep 2
browser.button(:id => 'ctl00_MainContent_DropDownFilter1_btnEnrollmentFilter').click
sleep 10
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("Carder, Dave")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject has been assigned."}
browser.link(:text, "Filter").click
sleep 2
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlState').option(:value, 'MA').select
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlRejectType').select(/Requires Review*/)
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlMID').select(/SOLX*/)
browser.select_list(:id => 'ctl00_MainContent_DropDownFilter1_ddlUser').option(:value, '7').select
sleep 2
browser.button(:value => 'Filter').click
sleep 10
browser.link(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_showCustControls').exists?}
if
browser.text.include? "SOLX"
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').option(:text, 'Carder, Dave').selected
if
browser.text.include? "Requires Review"
if
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ValidationPanel1_ddlServiceState').option(:text, 'MA').selected
print "Filter Enrollment Rejects by state, User, MID, and Reject Type - Passed", "\n"
else
print "Filter Enrollment Rejects by state, User, MID, and Reject Type - Failed", "\n"
end
end
end
end
browser.select_list(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_ddlAssignUser').select ("")
browser.button(:id => 'ctl00_MainContent_dlStagingRecords_ctl01_btnAssign').click
Watir::Waiter::wait_until {browser.text.include? "The reject assignment has been removed."}
browser.button(:value => 'Reset').click
sleep 20

browser.close