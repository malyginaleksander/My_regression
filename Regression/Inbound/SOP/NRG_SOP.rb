require 'rubygems'
require 'watir-webdriver'
require 'win32ole' 
require 'csv'

rows = 2			
while    
rows <= 2		

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\Inbound\\SOP\\State_Data.xlsx")
worksheet = workbook.worksheets(3)
first_name=worksheet.cells(rows,"A").value
last_name=worksheet.cells(rows,"B").value
state=worksheet.cells(rows,"C").value
plan=worksheet.cells(rows,"D").value.to_s
address=worksheet.cells(rows,"E").value
city=worksheet.cells(rows,"F").value
zip=worksheet.cells(rows,"G").value
area_code=worksheet.cells(rows,"H").value
prefix=worksheet.cells(rows,"I").value.to_s
last=worksheet.cells(rows,"J").value.to_s
account_number=worksheet.cells(rows,"K").value.to_s

browser = Watir::Browser.new :firefox
browser.goto 'http://www.pt.energypluscompany.com/myinbound/login.php'

#login
browser.text_field(:name => 'email').set ('mpeters@energypluscompany.com')
browser.text_field(:name => 'password').set ('energy')
browser.button(:value => ' Login').click

if
browser.text.include? "Start a manual call"
browser.link(:text => 'Start a manual call').click
browser.text_field(:id => 'phoneNumber').set("2154935444")
browser.text_field(:id => 'reason').set("this is a test")
browser.select_list(:id => 'brand_id').select("NRG Home")
browser.button(:value => 'Start Call').click
sleep 3
browser.alert.exists?
browser.alert.ok

sleep 2
else

browser.radio(:id => 'brandId_2').visible?
browser.radio(:id => 'brandId_2').click
browser.button(:id => 'btn_continue').click
end
sleep 2

#Get Started
browser.text_field(:id => 'caller-first-name').set first_name
browser.text_field(:id => 'caller-last-name').set last_name
browser.button(:id => 'sop-button').click
browser.button(:id => 'save-and-continue').click
sleep 4

#offer
browser.div(:id => plan).click
sleep 2
browser.button(:name => 'btn_continue').click
sleep 5

#Customer Info
browser.text_field(:name => 'First Name').set first_name
browser.text_field(:name => 'Last Name').set last_name
browser.text_field(:name => 'Service Address 1').set address
browser.text_field(:name => 'City').set city
browser.text_field(:name => 'Zip').set zip
browser.text_field(:name => 'Phone Area Code').set area_code
browser.text_field(:name => 'Phone Prefix').set prefix
browser.text_field(:name => 'Phone Last Digits').set last
browser.radio(:class => 'copy-to-billing-yes').set
browser.text_field(:class => 'uan required').set account_number
browser.button(:class => 'check-account-number').click
Watir::Wait.until {browser.span(:class => 'account-uan-message').visible?}
browser.button(:value => 'Save and Continue').click

#Billing Info
sleep 4
browser.radio(:class => 'email-no').set
browser.radio(:class => 'email-no-no').set
browser.button(:value => 'Save and Continue').click
sleep 2

#Summary
browser.link(:id => 'to-disclosures').click

##Disclosure 
browser.radio(:id => 'toggle_1_no').set
browser.radio(:id => 'toggle_2_no').set
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id => 'toggle_4_no').set
browser.radio(:id => 'toggle_5_yes').set
browser.button(:id => 'submit_tpv_button').click
browser.radio(:id => 'toggle_6_no').set
browser.radio(:id => 'toggle_7_yes').set

if 
browser.span(:id => 'confcode').visible?
CSV.open('C:\\Scripts\\Inbound\\SOP\\NRG_State_Conf_data.csv', 'ab') do |csv|
csv << [browser.span(:id => 'confcode').text]
end
end

browser.button(:id => 'submit_enroll').click

sleep 1

browser.close 
rows=rows+1

$end
workbook.Save
workbook.Close
end

$end
sleep 2