require 'rubygems'
require 'watir-webdriver'
require 'win32ole' 
require 'csv'


rows = 2			#2
while    
rows <= 2			#2

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\Inbound\\Save_Enrollment\\Save_Enrollment_Data.xlsx")
worksheet = workbook.worksheets(3)

first_name=worksheet.cells(rows,"A").value
last_name=worksheet.cells(rows,"B").value
state=worksheet.cells(rows,"C").value
utility=worksheet.cells(rows,"D").value
plan=worksheet.cells(rows,"E").value.to_s
address=worksheet.cells(rows,"F").value
city=worksheet.cells(rows,"G").value
zip=worksheet.cells(rows,"H").value
area_code=worksheet.cells(rows,"I").value
prefix=worksheet.cells(rows,"J").value.to_s
last=worksheet.cells(rows,"K").value.to_s
account_number=worksheet.cells(rows,"L").value.to_s

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

#Brand
browser.radio(:id => 'brandId_2').exists?
browser.radio(:id => 'brandId_2').click
browser.button(:id => 'btn_continue').click
end
sleep 2

#Get Started
browser.text_field(:id => 'caller-first-name').set first_name
browser.text_field(:id => 'caller-last-name').set last_name
browser.select_list(:name => 'state-list').select state

if 
browser.radio(:class => 'commodity-choice-electric').visible?
browser.radio(:class => 'commodity-choice-electric').set
browser.select_list(:name => 'utility-list').select utility
browser.radio(:class => 'account-type-residential').set
end

if
browser.select_list(:name => 'utility-list').select utility
browser.radio(:class => 'account-type-residential').set
end

browser.button(:value => 'Save and Continue').click

#Offer Tab
sleep 4
#browser.link(:name => '*Primary Plans').click
browser.div(:id => plan).click
browser.button(:value => 'Save and Continue').click
sleep 3

#Customer Info Tab
browser.text_field(:name => 'First Name').set first_name
browser.text_field(:name => 'Last Name').set last_name
browser.text_field(:name => 'Service Address 1').set address
browser.text_field(:name => 'City').set city
browser.text_field(:name => 'Zip').set zip
browser.text_field(:name => 'Phone Area Code').set area_code
browser.text_field(:name => 'Phone Prefix').set prefix
browser.text_field(:name => 'Phone Last Digits').set last
browser.text_field(:class => 'uan required').set account_number
browser.button(:class => 'check-account-number').click
sleep 2
browser.button(:value => 'Save and Continue').click
sleep 2

#Dispo
browser.button(:id => 'log-dispo').click
sleep 3
browser.select_list(:id => 'dispo-list').select "509 : Test Call"
sleep 2
browser.button(:id => 'dispo-start-new').click
sleep 3

#login
if
browser.text_field(:name => 'email').exists?
browser.text_field(:name => 'email').set ('mpeters@energypluscompany.com')
browser.text_field(:name => 'password').set ('energy')
browser.button(:value => ' Login').click
end
sleep 2

#Brand
browser.radio(:id => 'brandId_2').click
browser.button(:id => 'btn_continue').click
sleep 2

#Load Saved Call
browser.link(:text => 'Load Saved Enrollment').click
browser.text_field(:id => 'caller-first-name').set first_name
browser.text_field(:id => 'account-first-name').set first_name
sleep 2
browser.button(:class => 'btn btn-primary').click
sleep 2

browser.table.tr(:xpath => '/html/body/div[2]/div/div[1]/div[1]/div[3]/table/tbody/tr').click
sleep 2
browser.button(:value => 'Load Saved Call').click
sleep 8

if
browser.link(:id => 'to-disclosures',:class => 'disabled').exists?
print "Passed"
else 
print "Failed"
end

#Billing Info
sleep 4
browser.link(:text => 'Billing Info').click
browser.text_field(:name => ' Billing Address').set address
browser.text_field(:name => ' City').set city
browser.select_list(:class => 'state-dropdown').select state
browser.text_field(:name => ' Zip Code').set zip
browser.text_field(:name => ' Phone Area Code').set area_code
browser.text_field(:name => ' Phone Prefix').set prefix
browser.text_field(:name => ' Phone Last Digits').set last
browser.radio(:class => 'email-no').set
browser.radio(:class => 'email-no-no').set
browser.button(:value => 'Save and Continue').click
sleep 2

#Summary
browser.link(:id => 'to-disclosures').click

browser.radio(:id, "toggle_1_no").set
browser.radio(:id, "toggle_2_no").set
browser.radio(:id, "toggle_3_no").set
browser.radio(:id, "toggle_4_no").set
browser.radio(:id, "toggle_5_no").set
browser.radio(:id, "toggle_6_no").set
browser.button(:value,"Submit TPV").click
browser.radio(:id, "toggle_7_no").set
browser.radio(:id, "toggle_8_yes").set

sleep 2

if 
browser.span(:id => 'confcode').visible?
CSV.open('C:\\Scripts\\Inbound\\Save_Enrollment\\NRG_Save_Enrollment_Conf_data.csv', 'ab') do |csv|
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