#Remove All instances of Current Page from spreadsheet
require 'rubygems'
require 'watir-webdriver'
require "win32ole"

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\EP_Web\\Links\\Links.xlsx")
worksheet = workbook.worksheets(2) 
browser = Watir::Browser.new :firefox

rows = 2		#2
while    
rows <= 64		#63

page=worksheet.cells(rows,"A").value
xpath=worksheet.cells(rows,"B").value
expected=worksheet.cells(rows,"C").value

string_from_excel = "goto"
browser.send string_from_excel, page
browser.link(:xpath => xpath).click
sleep 1

if
browser.text.include? 'Server Error'
print "Server Error, "
end

if
browser.url == expected
puts "good"
else
puts "bad"
end
rows=rows+1
end

browser.close 

$end
workbook.Save
workbook.Close

$end
sleep 2