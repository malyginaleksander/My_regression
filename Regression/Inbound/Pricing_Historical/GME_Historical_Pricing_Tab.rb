require 'rubygems'
require 'watir-webdriver'
require "win32ole"
require 'csv'

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\Inbound\\Pricing_Historical\\Historical_Pricing.xlsx")
worksheet = workbook.worksheets(3) 

rows = 2
while    
rows <= 13	#19

browser = Watir::Browser.new :firefox
browser.goto 'http://www.pt.energypluscompany.com/myinbound/login.php'

#login
browser.text_field(:name => 'email').set ('mpeters@energypluscompany.com')
browser.text_field(:name => 'password').set ('energy')
browser.button(:value => ' Login').click
sleep 2

browser.radio(:id => 'brandId_5').click
browser.button(:id => 'btn_continue').click
sleep 2
browser.link(:text => 'Historical Pricing').click

state=worksheet.cells(rows,"A").value
commodity=worksheet.cells(rows,"B").value
utility=worksheet.cells(rows,"C").value

browser.select_list(:id, "state").select state
browser.select_list(:id, "commodity").select commodity
browser.select_list(:id, "utility").select utility

Watir::Wait.until {browser.table(:id => 'tbl_histpricing').exists?}
if 
browser.table(:id => 'tbl_histpricing').exists?
print "GME - ", state, " ", commodity, " ", utility, " - passed", " \n"
else
print "GME - ", state, " ", commodity, " ", utility, " - failed", " \n"
end

browser.close

sleep 0.5
rows=rows+1
end

$end
workbook.Save
workbook.Close

### Pennsylvania ###
browser = Watir::Browser.new :firefox
browser.goto 'http://www.pt.energypluscompany.com/myinbound/login.php'

#login
browser.text_field(:name => 'email').set ('mpeters@energypluscompany.com')
browser.text_field(:name => 'password').set ('energy')
browser.button(:value => ' Login').click
sleep 2

browser.radio(:id => 'brandId_5').click
browser.button(:id => 'btn_continue').click
sleep 2

browser.link(:text => 'Historical Pricing').click

browser.select_list(:id, "state").select("Pennsylvania")

if 
browser.text.include? "www.greenmountainenergy.com/PAHistoricalPricing"
print "Pennsylvania - passed", " \n"
else
print "Pennsylvania - failed", " \n"
end

if 
browser.table(:id => 'tbl_histpricing').exists?
print "table shows - failed", " \n"
else
print "table does not show - passed", " \n"
end


browser.close