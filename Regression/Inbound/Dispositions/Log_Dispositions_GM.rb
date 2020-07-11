require 'rubygems'
require 'watir-webdriver'
require 'win32ole'
require 'csv'

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\INBOUND\\Dispositions\\Dispositions_data.xlsx")
worksheet = workbook.worksheets(5) 

rows = 2
while    
rows <= 12	#12
disposition=worksheet.cells(rows,"A").value

browser = Watir::Browser.new :firefox
browser.goto 'http://www.pt.energypluscompany.com/myinbound/login.php'

if
browser.text.include? "There is a problem with this website's security certificate."
browser.link(:text => 'Continue to this website (not recommended).').click
end

#login
browser.text_field(:name => 'email').set ('mpeters@energypluscompany.com')
browser.text_field(:name => 'password').set ('energy')
browser.button(:value => ' Login').click

if
browser.text.include? "Start a manual call"
browser.link(:text => 'Start a manual call').click
browser.text_field(:id => 'phoneNumber').set("2154935444")
browser.text_field(:id => 'reason').set("this is a test")
browser.select_list(:id => 'brand_id').select("Green Mountain Energy")
browser.button(:value => 'Start Call').click_no_wait
browser.javascript_dialog.button('OK').click
sleep 2
else
browser.radio(:id => 'brandId_5').visible?
browser.radio(:id => 'brandId_5').click
browser.button(:id => 'btn_continue').click
end
sleep 2

browser.button(:id => 'log-dispo').click
sleep 5
browser.select_list(:id => 'dispo-list').select disposition
sleep 2

if
browser.text_field(:name => 'dispo-comments').visible?
sleep 2
browser.text_field(:name => 'dispo-comments').set "test"
end
browser.button(:id => 'dispo-start-new').click
sleep 3


browser.close

rows=rows+1
end

$end
workbook.Save
workbook.Close