require 'rubygems'
require 'watir-webdriver'
require "win32ole"
require 'csv'

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\Inbound\\FAQ\\Regression\\FAQ_Regression_data.xlsx")
worksheet = workbook.worksheets(2) 

browser = Watir::Browser.new :firefox
browser.goto 'http://www.pt.energypluscompany.com/myinbound/login.php'

#login
browser.text_field(:name => 'email').set ('mpeters@energypluscompany.com')
browser.text_field(:name => 'password').set ('energy')
browser.button(:value => ' Login').click

#Brand
browser.radio(:id => 'brandId_1').click
browser.button(:id => 'btn_continue').click
sleep 2

#Get Started Tab
browser.button(:id => 'sop-button').click
browser.button(:id => 'save-and-continue').click
sleep 2

browser.select_list(:class => 'campaigns').select "6666 - Rate Class RS - Residential Service"
browser.select_list(:class => 'promos').select "000 - PA Standard Offer"
browser.button(:value => 'Save and Continue').click

sleep 5
browser.link(:text => "FAQs").click
sleep 5
###### Main Headers ######
rows = 2
while    
rows <= 11
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