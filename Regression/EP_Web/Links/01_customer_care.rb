#Remove All instances of Current Page from spreadsheet
require 'rubygems'
require 'watir-webdriver'
require "win32ole"

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\EP_Web\\Links\\Links.xlsx")
worksheet = workbook.worksheets(1) 
browser = Watir::Browser.new :firefox

rows = 2
while    
rows <= 19

customer=worksheet.cells(rows,"A").value
state=worksheet.cells(rows,"B").value
phone=worksheet.cells(rows,"C").value
email=worksheet.cells(rows,"D").value

browser.goto 'http://www.pt.energypluscompany.com/care/care.php'

browser.radio(:value => customer).click
browser.select_list(:id, 'selectState').select state

if
browser.text.include? phone
print "Phone Passed, "
else
print "Phone Failed, "
end

if 
browser.text.include? email
print "Email Passed", "\n" 
else
print "Email Failed", "\n"
end
 
rows=rows+1
end


browser.close

$end
workbook.Save
workbook.Close


sleep 2