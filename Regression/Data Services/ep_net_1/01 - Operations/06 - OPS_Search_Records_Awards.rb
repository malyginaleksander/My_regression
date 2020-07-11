require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Operations/SearchEnrollments.aspx'
browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').select ('Awards')
sleep 2

#Search Award By Account Last Name
browser.text_field(:id => 'ctl00_MainContent_txtAcctLastName').set ('Smith')
browser.button(:id => 'ctl00_MainContent_btnSearch').click
Watir::Waiter::wait_until {browser.text.include? "Date Due"}
if
browser.span(:id => 'ctl00_MainContent_gvResults_ctl02_lblCustLastName').text.include? "Smith"
print "Search Award By Account Last Name - Passed", "\n"
else
print "Search Award By Account Last Name - Failed", "\n"
end
browser.button(:id => 'ctl00_MainContent_btnReset').click
Watir::Waiter::wait_until {browser.text_field(:id => 'ctl00_MainContent_txtAcctLastName').text.include? ""}

#Search Award By Partner
browser.select_list(:id => 'ctl00_MainContent_ddlPartner').select ('(AAL) American Airlines')
browser.text_field(:id => 'ctl00_MainContent_txtAcctLastName').set ('Smith')
browser.button(:id => 'ctl00_MainContent_btnSearch').click
Watir::Waiter::wait_until {browser.text.include? "Date Due"}
if
browser.span(:id => 'ctl00_MainContent_gvResults_ctl02_lblPartnerCode').text.include? "AAL"
print "Search Award By Partner - Passed", "\n"
else
print "Search Award By Partner - Failed", "\n"
end
browser.button(:id => 'ctl00_MainContent_btnReset').click
Watir::Waiter::wait_until {browser.select_list(:id => 'ctl00_MainContent_ddlPartner').option(:value, "")}

#Add a Comment to an Award Record
browser.select_list(:id => 'ctl00_MainContent_ddlPartner').select ('(AAL) American Airlines')
browser.text_field(:id => 'ctl00_MainContent_txtAcctLastName').set ('Smith')
browser.button(:id => 'ctl00_MainContent_btnSearch').click
Watir::Waiter::wait_until {browser.text.include? "Date Due"}
browser.link(:id => 'ctl00_MainContent_gvResults_ctl02_hlViewDetails').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_CommentPanel1_gvComments').exists?}
browser.text_field(:id => /ctl00_MainContent_CommentPanel1_gvComments_ct*/).set ('adding a comment')
browser.button(:id => 'ctl00_MainContent_CommentPanel1_btnAdd').click
sleep 3
if
browser.text.include? "adding a comment"
print "Add a Comment to an Award Record - Passed", "\n"
else
print "Add a Comment to an Award Record - Failed", "\n"
end
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsSearchRecords').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_searchForm').exists?}
browser.select_list(:id => 'ctl00_MainContent_ddlSearchType').select ('Awards')
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_searchForm').exists?}
sleep 3

#Save Premise Information and Reprocess an Award record
browser.select_list(:id => 'ctl00_MainContent_ddlPartner').select ('(AAL) American Airlines')
browser.text_field(:id => 'ctl00_MainContent_txtAcctFirstName').set("john")
browser.text_field(:id => 'ctl00_MainContent_txtAcctLastName').set("smith")
browser.button(:value => 'Search').click
browser.link(:id => 'ctl00_MainContent_gvResults_ctl02_hlViewDetails').click
browser.select_list(:id => 'ctl00_MainContent_CustomerPremiseInfo1_ddlPromotion').select("1% Back (008)")
browser.button(:value => 'Save Premise Information and Reprocess Pending Awards').click
Watir::Waiter::wait_until {browser.text.include? "The awards have been reprocessed"}
browser.link(:id => 'ctl00_ucTabNavigation_hlOperationsSearchRecords').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_searchForm').exists?}
browser.select_list(:id =>  'ctl00_MainContent_ddlSearchType').select("Awards")
sleep 2
browser.select_list(:id => 'ctl00_MainContent_ddlPartner').select ('(AAL) American Airlines')
browser.text_field(:id => 'ctl00_MainContent_txtAcctFirstName').set("john")
browser.text_field(:id => 'ctl00_MainContent_txtAcctLastName').set("smith")
browser.button(:value => 'Search').click
browser.link(:id => 'ctl00_MainContent_gvResults_ctl02_hlViewDetails').click
if
browser.select_list(:id => 'ctl00_MainContent_CustomerPremiseInfo1_ddlPromotion').option(:text, '1% Back (008)').selected
print "Save Premise Information and Reprocess an Award record - Passed", "\n"
else
print "Save Premise Information and Reprocess an Award record - Failed", "\n"
end

browser.close