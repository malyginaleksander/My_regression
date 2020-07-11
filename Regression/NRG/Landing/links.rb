#Remove All instances of Current Page from spreadsheet
require 'rubygems'
require 'watir-webdriver'
require "win32ole"

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\NRG\\links.xlsx")
worksheet = workbook.worksheets(1)

browser = Watir::Browser.new :firefox

rows = 2		#2
while    
rows <= 31		#31

browser.goto 'http://nrghomepower.qa.nrgpl.us'

page=worksheet.cells(rows,"A").value
xpath=worksheet.cells(rows,"B").value
expected=worksheet.cells(rows,"C").value
result=worksheet.cells(rows,"E").value

string_from_excel = "goto"
browser.send string_from_excel, page
browser.link(:xpath => xpath).click

if
browser.text.include? 'Server Error'
print "Server Error, "
end

if
browser.url == expected
print result, " = good", "\n"
else
print result, " = bad", "\n"
end
rows=rows+1
end

browser.close 

$end
workbook.Save
workbook.Close

$end
sleep 2