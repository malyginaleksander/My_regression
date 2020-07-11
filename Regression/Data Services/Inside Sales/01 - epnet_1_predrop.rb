##############################################################
#need admin - manage employee roles - drop admin permissions
#update xls with UAN and Customer Names
##############################################################

require 'rubygems'
require 'watir'
require 'win32ole'

rows = 3
while    
rows <= 3

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\EP_NET\\Inside Sales\\epnet_1_predrop_data.xlsx")
worksheet = workbook.worksheets(1) 

uan=worksheet.cells(rows,"A").value.to_s
customer_name=worksheet.cells(rows,"E").value.to_s
test_case=worksheet.cells(rows,"F").value.to_s

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/login.aspx'
browser.text_field(:id => 'ctl00_MainContent_txtUsername').set ("mpetersqa")
browser.text_field(:id => 'ctl00_MainContent_txtPassword').set ("Welcome19")
browser.button(:id => 'ctl00_MainContent_btnLogin').click
Watir::Waiter::wait_until {browser.text.include? "Total Records"}
browser.goto 'http://epnet1.pt.nrgpl.us/DropAssignment.aspx'

Watir::Waiter::wait_until {browser.text_field(:id => 'ctl00_MainContent_ucDropAssignment_txtUtilityID').exists?}
browser.text_field(:id => 'ctl00_MainContent_ucDropAssignment_txtUtilityID').set uan
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.text.include? "Assign To"}
browser.select_list(:id => 'ctl00_MainContent_ucDropAssignment_ddlDropRep').select("Lile, Stuart")
browser.button(:value => 'Set as Pre-Drop').click

print test_case, "\n"
print uan, "\n"
print customer_name, "\n"

Watir::Waiter::wait_until {browser.text.include? "Your Pre Drop has been assigned."}
if 
browser.text.include? "Your Pre Drop has been assigned"
print "Your Pre Drop has been assigned", "\n"
else
print "Your Pre Drop has been assigned - Failed", "\n"
end

browser.goto 'http://epnet1.pt.nrgpl.us/Sales/DropQueue.aspx'
browser.text_field(:id => 'ctl00_MainContent_ucDropOverview_ucDropDownFilter_txtUtilAccountNum').set uan
browser.button(:value => 'Search').click
sleep 5
browser.link(:text => uan).click

sleep 30
browser = Watir::Browser.attach(:title, customer_name)
browser.select_list(:id => 'ctl00_MainContent_ucDropDetails_ddlDropReason').select("Rate")
sleep 5
browser.select_list(:id => 'ctl00_MainContent_ucDropDetails_ddlStatus').select("Saved")
sleep 5
if
browser.select_list(:id => 'ctl00_MainContent_ucDropDetails_ddlNewPricingGroup', :class => 'aspNetDisabled').visible?
print "New Price Group is disabled", "\n"
else 
print "New Price Group is not disabled", "\n"
end
if
browser.select_list(:id => 'ctl00_MainContent_ucDropDetails_ddlNewPartner', :class => 'aspNetDisabled').visible?
print "New Partner is disabled", "\n"
else 
print "New Partner is not disabled", "\n"
end
if
browser.select_list(:id => 'ctl00_MainContent_ucDropDetails_ddlNewPromotion', :class => 'aspNetDisabled').visible?
print "New Promo is disabled", "\n"
else 
print "New Promo is not disabled", "\n"
end
browser.select_list(:id => 'ctl00_MainContent_ucCommunicationLog_ddlAddType').select("Phone")
sleep 5
browser.select_list(:id => 'ctl00_MainContent_ucCommunicationLog_ddlDirection').select("Inbound")
browser.select_list(:id => 'ctl00_MainContent_ucCommunicationLog_ddlAddResult').select("Busy")
browser.text_field(:id => 'ctl00_MainContent_ucCommunicationLog_ucCommunicationLogNoteBox_txtAddNotes').set("regression test")
browser.button(:value => 'Submit Note').click
Watir::Waiter::wait_until {browser.text.include? "Your note has been added."}
if
browser.text.include? "Your note has been added."
print "Your note has been added", "\n"
else
print "Your note has been added - Failed", "\n"
end
browser.button(:value => 'Save').click_no_wait
browser.javascript_dialog.button('OK').click
Watir::Waiter::wait_until {browser.text.include? "Successfully Saved."}
if 
browser.text.include? "Successfully Saved."
print "Successfully Saved.", "\n"
else
print "Save Failed", "\n"
end
browser = Watir::Browser.attach(:title, customer_name).close
browser = Watir::Browser.attach(:title, 'Drop Overview').close

rows=rows+1
end

$end
workbook.Save
workbook.Close

sleep 2