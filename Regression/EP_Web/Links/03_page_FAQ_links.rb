#Remove All instances of Current Page from spreadsheet
require 'rubygems'
require 'watir-webdriver'
require "win32ole"

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\EP_Web\\Links\\Links.xlsx")
worksheet = workbook.worksheets(3) 
browser = Watir::Browser.new :firefox

rows = 2		#2
while    
rows <= 15		#15

page=worksheet.cells(rows,"A").value
link=worksheet.cells(rows,"B").value
xpath=worksheet.cells(rows,"C").value
expected=worksheet.cells(rows,"D").value

string_from_excel = "goto"
browser.send string_from_excel, page
browser.link(:xpath => link).click
sleep 2
browser.link(:xpath => xpath).click
sleep 2

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

rows = 16		#2
while    
rows <= 17		#56

page=worksheet.cells(rows,"A").value
link=worksheet.cells(rows,"B").value
xpath=worksheet.cells(rows,"C").value
expected=worksheet.cells(rows,"D").value

browser = Watir::Browser.new :firefox

string_from_excel = "goto"
browser.send string_from_excel, page
browser.link(:xpath => link).click
sleep 2
browser.link(:xpath => xpath).click
sleep 2

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

browser.close

rows=rows+1
end


$end
workbook.Save
workbook.Close

$end
sleep 2