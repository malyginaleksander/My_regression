require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/awards#reconciliation'
sleep 5
browser.select_list(:id => 'awardsReconciliationPartnerCodeComboBox').select("BBY - Best Buy")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_milesListingGrid').exists?}
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
Watir::Waiter::wait_until {browser.text.include? "View 401"}
if
browser.text.include? "View 401"
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

#Sorting
#Reply File Name
browser.text_field(:id => 'jqgh_milesListingGrid_ReplyFileName').click
sleep 10
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "BBY_Reply"
print "Sort by Reply File Name ASC - Passed", "\n"
else
print "Sort by Reply File Name ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_milesListingGrid_ReplyFileName').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "R00000006"
print "Sort by Reply File Name DESC - Passed", "\n"
else
print "Sort by Reply File Name Code - Failed", "\n"
end

#Partner Indicator
browser.div(:id => 'jqgh_milesListingGrid_PartnerIncicator').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "3964"
print "Sort by Partner Indicator ASC - Passed", "\n"
else
print "Sort by Partner Indicator ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_milesListingGrid_PartnerIncicator').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "5263"
print "Sort by Partner Indicator DESC - Passed", "\n"
else
print "Sort by Partner Indicator DESC - Failed", "\n"
end

#Partner Billing Period
browser.div(:id => 'jqgh_milesListingGrid_PartnerBillingPeriod').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[9]').text.include? "undefined"
print "Sort by Partner Billing Period ASC - Passed", "\n"
else
print "Sort by Partner Billing Period ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_milesListingGrid_PartnerBillingPeriod').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[9]').text.include? "September 2012"
print "Sort by Partner Billing Period DESC - Passed", "\n"
else
print "Sort by Partner Billing Period Code - Failed", "\n"
end

#Partner Invoice
browser.div(:id => 'jqgh_milesListingGrid_PartnerInvoice').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]').text.include? "undefined"
print "Sort by Partner Invoice ASC - Passed", "\n"
else
print "Sort by Partner Invoice ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_milesListingGrid_PartnerInvoice').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]').text.include? "RZ-EP-08"
print "Sort by Partner Invoice DESC - Passed", "\n"
else
print "Sort by Partner Invoice DESC - Failed", "\n"
end

#Notes
browser.div(:id => 'jqgh_milesListingGrid_PDF').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[16]').text.include? "undefined"
print "Sort by Notes ASC - Passed", "\n"
else
print "Sort by Notes ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_milesListingGrid_PDF').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[16]').text.include? "Balanced"
print "Sort by Notes DESC - Passed", "\n"
else
print "Sort by Notes DESC - Failed", "\n"
end

#Filter
wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Awards')
sleep 5

#Reply File Name
browser.text_field(:id => 'gs_ReplyFileName').set("R00000006_08052010122216_Response.txt")
browser.text_field(:id => 'gs_ReplyFileName').set("")
browser.text_field(:id => 'gs_ReplyFileName').set("R00000006_08052010122216_Response.txt")
browser.send_keys("{ENTER}") 
sleep 10
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "R00000006_08052010122216_Response.txt"
print "Filter by Reply File Name - Passed", "\n"
else
print "Filter by Reply File Name - Failed", "\n"
end
browser.text_field(:id => 'gs_ReplyFileName').set("")

#Reply Date
browser.text_field(:id => 'gs_ReplyDate').set("09/09/2010")
browser.send_keys("{ENTER}") 
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "09/09/2010"
print "Filter by Reply Date - Passed", "\n"
else
print "Filter by Reply Date - Failed", "\n"
end
browser.text_field(:id => 'gs_ReplyDate').set("")

#Partner Indicator
browser.text_field(:id => 'gs_PartnerIncicator').set("3965")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "3965"
print "Filter by Partner Indicator - Passed", "\n"
else
print "Filter by Partner Indicator - Failed", "\n"
end
browser.text_field(:id => 'gs_PartnerIncicator').set("")

#Miles
browser.text_field(:id => 'gs_Miles').set("35000")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "35000"
print "Filter by Miles - Passed", "\n"
else
print "Filter by Miles - Failed", "\n"
end
browser.text_field(:id => 'gs_Miles').set("")

#Partner Billing Period
browser.text_field(:id => 'gs_PartnerBillingPeriod').set("December 2011")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[9]').text.include? "December 2011"
print "Filter by Partner Billing Period - Passed", "\n"
else
print "Filter by Partner Billing Period - Failed", "\n"
end
browser.text_field(:id => 'gs_PartnerBillingPeriod').set("")

#Partner Invoice
browser.text_field(:id => 'gs_PartnerInvoice').set("4002762")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]').text.include? "4002762"
print "Filter by Partner Invoice - Passed", "\n"
else
print "Filter by Partner Invoice - Failed", "\n"
end
browser.text_field(:id => 'gs_PartnerInvoice').set("")

#Partner Invoice Data
browser.text_field(:id => 'gs_PartnerInvoiceDate').set("02/15/2011")
browser.send_keys("{ENTER}") 
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[12]').text.include? "02/15/2011"
print "Filter by Invoice Data - Passed", "\n"
else
print "Filter by Invoice Data - Failed", "\n"
end
browser.text_field(:id => 'gs_PartnerInvoiceDate').set("")

#Reconciled Date
browser.text_field(:id => 'gs_Reconcilled').set("06/15/2012")
browser.send_keys("{ENTER}") 
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[13]').text.include? "06/15/2012"
print "Filter by Reconciled Date - Passed", "\n"
else
print "Filter by Reconciled Date - Failed", "\n"
end
browser.text_field(:id => 'gs_Reconcilled').set("")

#PDF Name
browser.text_field(:id => 'gs_PDF').set("BBY 201107")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[15]').text.include? "BBY 201107"
print "Filter by PDF Name - Passed", "\n"
else
print "Filter by PDF Name - Failed", "\n"
end
browser.text_field(:id => 'gs_PDF').set("")

browser.close