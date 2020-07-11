require 'rubygems'
require 'watir-webdriver'
require "win32ole"

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\Zookeeper\\pages\\pages.xlsx")
worksheet = workbook.worksheets(1) 

browser = Watir::Browser.new :firefox
#browser.goto "http://www.qa.energypluscompany.com/newadmin/login.php"
browser.goto "http://www.pt.energypluscompany.com/newadmin/login.php"

browser.text_field(:name => 'loginusername').set("mpeters")
browser.text_field(:name => 'loginpassword').set("energy")
browser.button(:value => 'Login').click
sleep 5

rows = 2
while    
rows <= 56	#56

page=worksheet.cells(rows,"A").value
header=worksheet.cells(rows,"B").value

browser.link(:xpath => page).click
sleep 2

if 
browser.div(:class => 'container').exists?
if
browser.text.include? header
print header, " - Passed", "\n"
else
print header, " - Failed", "\n"
end
elsif
browser.div(:class => 'maincontent').exists?
if
browser.text.include? header
print header, " - Passed", "\n"
else
print header, " - Failed", "\n"
end
end

browser.goto "http://www.pt.energypluscompany.com/newadmin/index.php"
sleep 2

rows=rows+1
end

browser.close

$end
workbook.Save
workbook.Close

sleep 2