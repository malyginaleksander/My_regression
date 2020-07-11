require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Finance/InitialOfferPricing.aspx'
sleep 5

#Display a Price Group using Pricing-Group, Pricing Code and State Drop-downs
rows = 2
while    
rows <= 5

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\EP_NET\\EP_NET_1.0\\04 - Finance\\EP_NET_FINANCE_DATA.xlsx")
worksheet = workbook.worksheets(1)

group=worksheet.cells(rows,"A").text
code=worksheet.cells(rows,"B").text
state=worksheet.cells(rows,"C").text

browser.select_list(:id => 'ctl00_MainContent_ddlPricingGroup').select group
sleep 6
browser.select_list(:id => 'ctl00_MainContent_ddlInitialOffer').select code
sleep 4
browser.select_list(:id => 'ctl00_MainContent_ddlState').select state
sleep 6

if
browser.span(:id => 'ctl00_MainContent_lblCalendar').text.include? "View Rates"
print "Display a Price Group - Passed", "\n"
else
print "Display a Price Group - Failed", "\n"
end

sleep 1
rows=rows+1


$end
workbook.Save
workbook.Close
end

sleep 2
browser.close

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Finance/InitialOfferPricing.aspx'
sleep 5
#Add a Pricing Group
#Update Pricing Group Value before each test
browser.link(:id => 'ctl00_MainContent_lbCustGroup').click
browser.text_field(:id => 'ctl00_MainContent_txtCustGroupVal').set ('12price')
browser.text_field(:id => 'ctl00_MainContent_txtCustGroupDesc').set ('test group')
browser.select_list(:id => 'ctl00_MainContent_ddlContractTerm').select ('3')
browser.button(:id => 'ctl00_MainContent_btnAddCustGroup').click
Watir::Waiter::wait_until {browser.text.include? "A new pricing group has been added"}
if
browser.select_list(:id => 'ctl00_MainContent_ddlPricingGroup').text.include? "12price / test group"
print "Add a Pricing Group - Passed", "\n"
else
print "Add a Pricing Group - Failed", "\n"
end

#Add a Pricing Code
#Change Customer Group to reflect Cust Group Value in above Test
browser.link(:id, "ctl00_MainContent_lbPricingCode").click
browser.text_field(:id, "ctl00_MainContent_txtInternalName").set("test")
browser.select_list(:id, "ctl00_MainContent_ddlCustomerGroup").select("12price / test group")
sleep 2
browser.button(:id => 'ctl00_MainContent_btnPricingCode').click
Watir::Waiter::wait_until {browser.text.include? "A New pricing code has been added"}
if
browser.text.include? "A New pricing code has been added"
print "Add a Pricing Code - Passed", "\n"
else
print "Add a Pricing Code - Failed", "\n"
end

browser.close