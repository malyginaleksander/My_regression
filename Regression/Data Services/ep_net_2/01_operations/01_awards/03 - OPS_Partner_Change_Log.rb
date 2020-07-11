require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/awards#partner_change_log'
Watir::Waiter::wait_until {browser.div(:id => 'gbox_partnerChangelogGrid').exists?}
sleep 5

#Paging on the Detail grid functions correctly
#Next Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-next').click
Watir::Waiter::wait_until {browser.text.include? "View 101 - 200"}
if
browser.text.include? "View 101 - 200"
print "Partner Change Log Next Page - Passed", "\n"
else
print "Partner Change Log Next Page - Failed", "\n"
end

#Previous Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-prev').click
Watir::Waiter::wait_until {browser.text.include? "View 1 - 100"}
if
browser.text.include? "View 1 - 100"
print "Partner Change Log Previous Page - Passed", "\n"
else
print "Partner Change Log Previous Page - Failed", "\n"
end

#Last Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-end').click
Watir::Waiter::wait_until {browser.text.include? "View 9 901"}
if
browser.text.include? "View 9 901"
print "Partner Change Log Last Page - Passed", "\n"
else
print "Partner Change Log Last Page - Failed", "\n"
end

#First Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-first').click
Watir::Waiter::wait_until {browser.text.include? "View 1 - 100"}
if
browser.text.include? "View 1 - 100"
print "Partner Change Log First Page - Passed", "\n"
else
print "Partner Change Log First Page - Failed", "\n"
end
sleep 2

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Awards')
sleep 5

#Select Page
browser.text_field(:class => 'ui-pg-input').set("10")
browser.send_keys("{ENTER}")
browser.send_keys("{ENTER}")
Watir::Waiter::wait_until {browser.text.include? "View 901 - 1 000"}
if
browser.text.include? "View 901 - 1 000"
print "Partner Change Log Select Page - Passed", "\n"
else
print "Partner Change Log Select Page - Failed", "\n"
end
sleep 2

#Sorting
#Sort Problem
browser.div(:id => 'jqgh_partnerChangelogGrid_Problem').click
sleep 5
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "Corrected Member Name"
print "Sort by Problem ASC - Passed", "\n"
else
print "Sort by Problem ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_partnerChangelogGrid_Problem').click
sleep 5
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "Renumbered Account-Name Mismatch"
print "Sort by Problem DESC - Passed", "\n"
else
print "Sort by Problem Code - Failed", "\n"
end
sleep 2

#Member Last Name
browser.div(:id => 'jqgh_partnerChangelogGrid_MemberLastName').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? ""
print "Sort by Member Last Name ASC - Passed", "\n"
else
print "Sort by Member Last Name ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_partnerChangelogGrid_MemberLastName').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "ZURITA"
print "Sort by Member Last Name DESC - Passed", "\n"
else
print "Sort by Member Last Name DESC - Failed", "\n"
end

#Member First Name
browser.div(:id => 'jqgh_partnerChangelogGrid_MemberFirstName').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[8]').text.include? "undefined"
print "Sort by Member First ASC - Passed", "\n"
else
print "Sort by Member First ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_partnerChangelogGrid_MemberFirstName').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[8]').text.include? "Yoel"
print "Sort by Member First DESC - Passed", "\n"
else
print "Sort by Member First Code - Failed", "\n"
end

#Partner Last Name
browser.div(:id => 'jqgh_partnerChangelogGrid_PartnerLastName').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]').text.include? ""
print "Sort by Partner Last Name ASC - Passed", "\n"
else
print "Sort by Partner Last Name ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_partnerChangelogGrid_PartnerLastName').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]').text.include? "ZYLINSKI"
print "Sort by Partner Last Name DESC - Passed", "\n"
else
print "Sort by Partner Last Name DESC - Failed", "\n"
end

#Partner First Name
browser.div(:id => 'jqgh_partnerChangelogGrid_PartnerFirstName').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[11]').text.include? "undefined"
print "Sort by Partner First Name ASC - Passed", "\n"
else
print "Sort by Partner First Name ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_partnerChangelogGrid_PartnerFirstName').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[11]').text.include? "ZVI"
print "Sort by Partner First Name DESC - Passed", "\n"
else
print "Sort by Partner First Name DESC - Failed", "\n"
end

#Filter
wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Awards')
sleep 5

#ID
browser.text_field(:id => 'gs_Id').set("14897")
browser.text_field(:id => 'gs_Id').set("")
browser.text_field(:id => 'gs_Id').set("14897")
browser.send_keys("{ENTER}") 
sleep 10
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "14897"
print "Filter by ID - Passed", "\n"
else
print "Filter by ID - Failed", "\n"
end
browser.text_field(:id => 'gs_Id').set("")

#Problem
browser.text_field(:id => 'gs_Problem').set("MERGED MEMBERSHIP NUMBER")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "MERGED MEMBERSHIP NUMBER"
print "Filter by Problem - Passed", "\n"
else
print "Filter by Problem - Failed", "\n"
end
browser.text_field(:id => 'gs_Problem').set("")

#Ben Id
browser.text_field(:id => 'gs_BenID').set("4202860")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "4202860"
print "Filter by BEN ID - Passed", "\n"
else
print "Filter by BEN ID - Failed", "\n"
end
browser.text_field(:id => 'gs_BenID').set("")

#Utility Account
browser.text_field(:id => 'gs_UtilityAccountNumber').set("8175056021")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "8175056021"
print "Filter by Utility Account - Passed", "\n"
else
print "Filter by Utility Account - Failed", "\n"
end
browser.text_field(:id => 'gs_UtilityAccountNumber').set("")

#Member ID
browser.text_field(:id => 'gs_MemberID').set("BVH68753")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "BVH68753"
print "Filter by Member Id - Passed", "\n"
else
print "Filter by Member Id - Failed", "\n"
end
browser.text_field(:id => 'gs_MemberID').set("")

#Member Last Name
browser.text_field(:id => 'gs_MemberLastName').set("ORATZ")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "ORATZ"
print "Filter by Member Last Name - Passed", "\n"
else
print "Filter by Member Last Name - Failed", "\n"
end
browser.text_field(:id => 'gs_MemberLastName').set("")

#Member First Name
browser.text_field(:id => 'gs_MemberFirstName').set("Yoel")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[8]').text.include? "Yoel"
print "Filter by Member First Name - Passed", "\n"
else
print "Filter by Member First Name - Failed", "\n"
end
browser.text_field(:id => 'gs_MemberFirstName').set("")

#Partner Member Number
browser.text_field(:id => 'gs_PartnerMemberNumber').set("9055430202")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[9]').text.include? "9055430202"
print "Filter by Partner Member Number - Passed", "\n"
else
print "Filter by Partner Member Number - Failed", "\n"
end
browser.text_field(:id => 'gs_PartnerMemberNumber').set("")

#Partner Last Name
browser.text_field(:id => 'gs_PartnerLastName').set("ASANO")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]').text.include? "ASANO"
print "Filter by Partner Last Name - Passed", "\n"
else
print "Filter by Partner Last Name - Failed", "\n"
end
browser.text_field(:id => 'gs_PartnerLastName').set("")

#Partner First Name
browser.text_field(:id => 'gs_PartnerFirstName').set("YEHUDA")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[11]').text.include? "YEHUDA"
print "Filter by Partner First Name - Passed", "\n"
else
print "Filter by Partner First Name - Failed", "\n"
end
browser.text_field(:id => 'gs_PartnerFirstName').set("")

#NY
browser.text_field(:id => 'gs_AwardID').set("1590702")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[12]').text.include? "1590702"
print "Filter by NY - Passed", "\n"
else
print "Filter by NY - Failed", "\n"
end
browser.text_field(:id => 'gs_AwardID').set("")

#Marked as Resolved
######### Update with every test run ##############
browser.text_field(:id => 'gs_BenID').set("4202860")
browser.send_keys("{ENTER}") 
browser.checkbox(:id => 'jqg_partnerChangelogGrid_148970').set
sleep 2
browser.span(:class => 'ui-icon ui-icon-circle-check').click
sleep 5
browser.text_field(:id => 'gs_BenID').set("4202860")
browser.send_keys("{ENTER}") 
sleep 3
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[2]/div[2]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').exists?
print "Marked as Resolved - Failed", "\n"
else
print "Marked as Resolved - Passed", "\n"
end

browser.close