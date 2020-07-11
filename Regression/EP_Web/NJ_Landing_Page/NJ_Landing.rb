require 'rubygems'
require 'watir-webdriver'
require "win32ole"
require 'csv'

###################
#  New Jersey     #
###################

browser = Watir::Browser.new :firefox
browser.goto 'http://www.pt.energypluscompany.com/resetsession.php'
browser.goto 'http://www.pt.energypluscompany.com/combined/cashback/nj/?apptype=WE&cellcode=01&campaign=0000&pc=015&pcb=015'

if
browser.text.include? "We're sorry, this offer has expired."
browser.link(:text => "click here").click
end

if
browser.text.include? "There is a problem"
browser.link(:text => "Continue to this website (not recommended).").click
end

rows = 2	
while    
rows <= 9	

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\EP_Web\\NJ_Landing_Page\\NJ_Data.xlsx")
worksheet = workbook.worksheets(1) 

xpath=worksheet.cells(rows,"A").value
utility=worksheet.cells(rows,"B").value
price=worksheet.cells(rows,"C").value.to_s

#Landing Page
browser.span(:id => 'show_price_table').click
sleep 2
if
browser.td(:xpath => xpath).text.include? price
print utility, " pass", "\n"
else
print utility, " failed", "\n"
end

sleep 1
rows=rows+1

$end
workbook.Save
workbook.Close
end

browser.close

$end
sleep 1