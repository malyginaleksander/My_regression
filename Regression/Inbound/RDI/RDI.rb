require 'rubygems'
require 'watir-webdriver'
require 'win32ole' 
require 'csv'

browser = Watir::Browser.new :firefox
browser.goto "http://www.pt.energypluscompany.com/newadmin/login.php"

browser.text_field(:name => 'loginusername').set("mpeters")
browser.text_field(:name => 'loginpassword').set("energy")
browser.button(:value => 'Login').click
sleep 4

browser.link(:xpath => '/html/body/div[4]/div[4]/div[2]/ul/li[4]/a').click
sleep 10
browser.text_field(:id => 'prependedInput').set("michael peters")
browser.table.tr(:id => '374').click
sleep 2
browser.select_list(:id, "vendor_id").select("RDIN : RDI Inbound")
sleep 2
browser.button(:value,"Save Operator").click
sleep 2
browser.close

rows = 2
while    
rows <= 2	#2		

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\Inbound\\RDI\\RDI_Data.xlsx")
worksheet = workbook.worksheets(1)

first_name=worksheet.cells(rows,"A").value
last_name=worksheet.cells(rows,"B").value
state=worksheet.cells(rows,"C").value
commodity_radio=worksheet.cells(rows,"D").value
utility=worksheet.cells(rows,"E").value
plan=worksheet.cells(rows,"F").value.to_s
address=worksheet.cells(rows,"G").value
city=worksheet.cells(rows,"H").value
zip=worksheet.cells(rows,"I").value
area_code=worksheet.cells(rows,"J").value
prefix=worksheet.cells(rows,"K").value.to_s
last=worksheet.cells(rows,"L").value.to_s
account_number=worksheet.cells(rows,"M").value.to_s
service_reference=worksheet.cells(rows,"N").value.to_s

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
browser.label(:id => 'label_brand_2').exists?
browser.label(:id => 'label_brand_2').click
browser.button(:id => 'btn_continue').click
end

#Get Started
browser.text_field(:id => 'caller-first-name').set first_name
browser.text_field(:id => 'caller-last-name').set last_name
browser.select_list(:name => 'state-list').select state

if 
browser.radio(:name => 'new-account-name_on_bill', :value => "Yes").exists?
browser.radio(:name => 'new-account-name_on_bill', :value => "Yes").click
end

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

#Offer
sleep 4
#browser.link(:name => 'Essentials Plans').click
sleep 1
browser.div(:id => plan).click
browser.button(:value => 'Save and Continue').click
sleep 3

#Customer Info
browser.text_field(:name => 'First Name').set first_name
browser.text_field(:name => 'Last Name').set last_name
browser.text_field(:name => 'Service Address 1').set address
browser.text_field(:name => 'City').set city
browser.text_field(:name => 'Zip').set zip
browser.text_field(:name => 'Phone Area Code').set area_code
browser.text_field(:name => 'Phone Prefix').set prefix
browser.text_field(:name => 'Phone Last Digits').set last
#browser.radio(:class => 'copy-to-billing-yes').set
browser.text_field(:class => 'uan required').set account_number
browser.button(:class => 'check-account-number').click
sleep 5

if
browser.text_field(:class => 'customer-key').exists?
browser.text_field(:class => 'customer-key').set "test"
end

if
browser.text_field(:class => 'extra-uan').exists?
browser.text_field(:class => 'extra-uan').set service_reference
browser.button(:class => 'check-extra-account-number').click
Watir::Wait.until {browser.span(:class => 'account-extra-uan-message').exists?}
end

browser.button(:value => 'Save and Continue').click
sleep 6


#Billing Info
sleep 4
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

#Disclosure
if 
browser.radio(:id => 'date_yes').exists?
browser.radio(:id => 'date_yes').set
browser.radio(:id, "accept_terms_yes").set
end

browser.radio(:id => 'toggle_1_no').set
browser.radio(:id => 'toggle_2_no').set

if
browser.text.include? "Cleveland"
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id => 'toggle_4_no').set
browser.radio(:id => 'toggle_5_yes').set
elsif
browser.text.include? "Chatham" 
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id => 'toggle_4_no').set
browser.radio(:id => 'toggle_5_yes').set
elsif
browser.text.include? "Boston" 
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id => 'toggle_4_no').set
browser.radio(:id => 'toggle_5_no').set
browser.radio(:id => 'toggle_6_no').set
browser.radio(:id => 'toggle_7_no').set
sleep 2
browser.button(:id => 'submit_tpv_button').click
sleep 2
browser.radio(:id => 'toggle_8_no').set
browser.radio(:id => 'toggle_9_yes').set
elsif
browser.text.include? "Bloomburg" 
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id => 'toggle_4_no').set
browser.radio(:id => 'toggle_5_yes').set
browser.radio(:id => 'toggle_6_no').set
sleep 2
browser.button(:id => 'submit_tpv_button').click
sleep 2
browser.radio(:id => 'toggle_7_no').set
browser.radio(:id => 'toggle_8_yes').set
elsif
browser.text.include? "Chicago" 
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id => 'toggle_4_no').set
browser.radio(:id => 'toggle_5_yes').set
elsif
browser.text.include? "Manhatten" 
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id=> 'toggle_4_no').set
browser.radio(:id => 'toggle_5_yes').set
sleep 2
browser.button(:id => 'submit_tpv_button').click
sleep 2
browser.radio(:id => 'toggle_6_no').set
elsif
browser.text.include? "Philadelphia" 
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id => 'toggle_4_no').set
browser.radio(:id => 'toggle_5_no').set
browser.radio(:id => 'toggle_6_no').set
sleep 2
browser.button(:id => 'submit_tpv_button').click
sleep 2
browser.radio(:id => 'toggle_7_no').set
browser.radio(:id => 'toggle_8_yes').set
elsif
browser.text.include? "Baltimore" 
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id => 'toggle_4_no').set
browser.radio(:id => 'toggle_5_yes').set
elsif
browser.text.include? "Washington"
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id => 'toggle_4_no').set
browser.radio(:id => 'toggle_5_no').set
browser.radio(:id => 'toggle_6_no').set
browser.radio(:id => 'toggle_7_yes').set		
else
browser.radio(:id => 'toggle_3_yes').set
end
sleep 2

if 
browser.span(:id => 'confcode').visible?
CSV.open('C:\\Scripts\\Inbound\\RDI\\RDI_data.csv', 'ab') do |csv|
csv << [browser.span(:id => 'confcode').text]
end
end

browser.button(:id => 'submit_enroll').click
sleep 2

if
browser.text.include? "RDI" 
print "Agent username Failed"
else 
print "Agent username Passed"
end

sleep 1

browser.close 
rows=rows+1

$end
workbook.Save
workbook.Close
end

$end
sleep 2

browser = Watir::Browser.new :firefox
browser.goto "http://www.pt.energypluscompany.com/newadmin/login.php"

browser.text_field(:name => 'loginusername').set("mpeters")
browser.text_field(:name => 'loginpassword').set("energy")
browser.button(:value => 'Login').click
sleep 4

browser.link(:xpath => '/html/body/div[4]/div[4]/div[2]/ul/li[4]/a').click
sleep 10
browser.text_field(:id => 'prependedInput').set("michael peters")
browser.table.tr(:id => '374').click
sleep 2
browser.select_list(:id, "vendor_id").select("EPIB : Energy Plus Inbound")
sleep 2
browser.button(:value,"Save Operator").click
sleep 2
browser.close
