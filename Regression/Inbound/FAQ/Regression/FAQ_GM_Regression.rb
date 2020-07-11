require 'rubygems'
require 'watir-webdriver'
require "win32ole"
require 'csv'

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\Inbound\\FAQ\\Regression\\FAQ_Regression_data.xlsx")
worksheet = workbook.worksheets(3) 

browser = Watir::Browser.new :firefox
browser.goto 'http://www.pt.energypluscompany.com/myinbound/login.php'

#login
browser.text_field(:name => 'email').set ('mpeters@energypluscompany.com')
browser.text_field(:name => 'password').set ('energy')
browser.button(:value => ' Login').click

#Brand
browser.radio(:id => 'brandId_5').click
browser.button(:id => 'btn_continue').click
sleep 2

browser.link(:text => 'FAQs').click
sleep 2

###### Main Headers ######
rows = 2
while    
rows <= 17
index=worksheet.cells(rows,"A").value
header=worksheet.cells(rows,"B").value
pass=worksheet.cells(rows,"C").value
fail=worksheet.cells(rows,"D").value

if
browser.text.include? header
puts pass
else
puts fail
end

rows=rows+1
end

$end
workbook.Save
workbook.Close

browser.close 