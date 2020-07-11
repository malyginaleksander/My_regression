require 'rubygems'
require 'watir-webdriver'
require "win32ole"

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\Zookeeper\\checksum\\checksum.xlsx")
worksheet = workbook.worksheets(1) 

browser = Watir::Browser.new :firefox
#browser.goto "http://www.qa.energypluscompany.com/newadmin/login.php"
browser.goto "http://www.pt.energypluscompany.com/newadmin/login.php"

browser.text_field(:name => 'loginusername').set("mpeters")
browser.text_field(:name => 'loginpassword').set("energy")
browser.button(:value => 'Login').click
browser.link(:xpath => '/html/body/div[4]/div[2]/div[2]/ul/li[10]/a').click
sleep 4

rows = 30
while    
rows <= 60	#60

partner=worksheet.cells(rows,"A").value
number=worksheet.cells(rows,"B").value

browser.table.td(:id => partner).click
sleep 2
browser.text_field(:id => 'partner_member_number').set number
browser.link(:id => 'checkNumber').click
Watir::Wait.until {browser.div(:id => 'checksum_message').visible?}
if 
browser.text.include? "Not Valid!"
print "Not Valid!", "\n"
else
print "Valid!", "\n"
end

rows=rows+1
end

browser.close

$end
workbook.Save
workbook.Close

sleep 2