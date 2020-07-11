require 'rubygems'
require 'watir-webdriver'
require "win32ole"

### FOOTER ###
excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\NRG\\Landing\\nrg_links.xlsx")
worksheet = workbook.worksheets(1)

browser = Watir::Browser.new :firefox

rows = 2		#2
while    
rows <= 5		#5

browser.goto 'http://enroll.pt.nrghomepower.com/combined/cashbackres/il/'

page=worksheet.cells(rows,"A").value
xpath=worksheet.cells(rows,"B").value
expected=worksheet.cells(rows,"C").value
result=worksheet.cells(rows,"E").value

string_from_excel = "goto"
browser.send string_from_excel, page
browser.link(:xpath => xpath).click

if
browser.alert.exists?
browser.alert.ok
end

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

$end
workbook.Save
workbook.Close

$end
sleep 2

### LOGO ###
excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\NRG\\Landing\\nrg_links.xlsx")
worksheet = workbook.worksheets(1)

rows = 6		#6
while    
rows <= 6		#6

browser.goto 'http://enroll.pt.nrghomepower.com/combined/cashbackres/il/'

page=worksheet.cells(rows,"A").value
xpath=worksheet.cells(rows,"B").value
expected=worksheet.cells(rows,"C").value
result=worksheet.cells(rows,"E").value

string_from_excel = "goto"
browser.send string_from_excel, page
browser.image(:xpath => xpath).click

if
browser.alert.exists?
browser.alert.ok
end

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

$end
workbook.Save
workbook.Close

$end
sleep 2

browser.close