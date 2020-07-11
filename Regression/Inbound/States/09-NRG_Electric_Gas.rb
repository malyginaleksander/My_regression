require 'rubygems'
require 'watir-webdriver'
require 'win32ole' 
require 'csv'

rows = 2
while    
rows <= 2	#2		

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\Inbound\\States\\State_Data.xlsx")
worksheet = workbook.worksheets(9)

first_name=worksheet.cells(rows,"A").value
last_name=worksheet.cells(rows,"B").value
state=worksheet.cells(rows,"C").value
utility=worksheet.cells(rows,"D").value
utility2=worksheet.cells(rows,"E").value
address=worksheet.cells(rows,"F").value
city=worksheet.cells(rows,"G").value
zip=worksheet.cells(rows,"H").value
area_code=worksheet.cells(rows,"I").value
prefix=worksheet.cells(rows,"J").value.to_s
last=worksheet.cells(rows,"K").value.to_s
account_number=worksheet.cells(rows,"L").value.to_s
account_number2=worksheet.cells(rows,"M").value.to_s

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
sleep 2
end

#Get Started
browser.text_field(:id => 'caller-first-name').set first_name
browser.text_field(:id => 'caller-last-name').set last_name
browser.select_list(:xpath => '/html/body/div[2]/div/div[1]/div[6]/div[1]/select').select state
browser.radio(:xpath => '/html/body/div[2]/div/div[1]/div[6]/div[2]/div[1]/label/input').set

if 
browser.radio(:name => 'new-account-name_on_bill', :value => "Yes").exists?
browser.radio(:name => 'new-account-name_on_bill', :value => "Yes").click
end

browser.select_list(:xpath => '/html/body/div[2]/div/div[1]/div[6]/div[3]/select').select utility
browser.radio(:xpath => '/html/body/div[2]/div/div[1]/div[6]/div[4]/label[1]/input').set
browser.button(:xpath => '/html/body/div[2]/div/div[1]/div[6]/div[6]/button[1]').click
sleep 2
browser.button(:value => 'Add Account').click
sleep 2
browser.select_list(:xpath => '/html/body/div[2]/div/div[1]/div[7]/div[1]/select').select state
browser.radio(:xpath => '/html/body/div[2]/div/div[1]/div[7]/div[2]/div[2]/label/input').set
sleep 1

if 
browser.radio(:name => 'new-account-name_on_bill', :value => "Yes").exists?
browser.radio(:name => 'new-account-name_on_bill', :value => "Yes").click
end

browser.select_list(:xpath => '/html/body/div[2]/div/div[1]/div[7]/div[3]/select').select utility2
browser.radio(:xpath => '/html/body/div[2]/div/div[1]/div[7]/div[4]/label[1]/input').set
browser.radio(:xpath => '/html/body/div[2]/div/div[1]/div[7]/div[5]/div[3]/label/input').set
browser.button(:xpath => '/html/body/div[2]/div/div[1]/div[7]/div[7]/button[1]').click
sleep 2
browser.button(:value => 'Save and Continue').click

#Offer
sleep 4
#browser.link(:xpath => '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/div[1]/p/span[1]/a').click
browser.div(:xpath => '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[1]/div/div[4]/div[1]/div[1]/div[2]').click
sleep 2
browser.link(:xpath => '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[2]/div/div[4]/div[1]/p/span[1]/a').click
browser.div(:xpath => '/html/body/div[2]/div/div[1]/div[1]/div/div[4]/div[2]/div/div[4]/div[1]/div[1]/div[2]').click

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
browser.radio(:class => 'copy-to-billing-yes').set
browser.text_field(:class => 'uan required').set account_number
browser.button(:class => 'check-account-number').click
Watir::Wait.until {browser.span(:class => 'account-uan-message').exists?}

browser.button(:class => 'same-as-first').click
browser.radio(:xpath => '/html/body/div[2]/div/div[1]/div[2]/div[2]/div[4]/input[1]').set
browser.text_field(:xpath => '/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/input').set account_number2
browser.button(:xpath => '/html/body/div[2]/div/div[1]/div[2]/div[2]/div[5]/button').click
browser.button(:value => 'Save and Continue').click

#Billing Info
sleep 4
browser.radio(:xpath => '/html/body/div[2]/div/div[1]/div[1]/div[1]/div[2]/input[2]').set
browser.radio(:xpath => '/html/body/div[2]/div/div[1]/div[1]/div[1]/div[2]/div/div/div[1]/p[2]/input[2]').set
sleep 2
browser.radio(:xpath => '/html/body/div[2]/div/div[1]/div[1]/div[2]/div[4]/input[2]').set
browser.radio(:xpath => '/html/body/div[2]/div/div[1]/div[1]/div[2]/div[4]/div/div/div[1]/p[2]/input[2]').set
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
browser.url == 'http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=OH'
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id => 'toggle_4_no').set
browser.radio(:id => 'toggle_5_yes').set
elsif
browser.url == 'http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=NJ'
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id => 'toggle_4_no').set
browser.radio(:id => 'toggle_5_yes').set
elsif
browser.url == 'http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MA'
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
browser.url == 'http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=CT'
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
browser.url == 'http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=IL'
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id => 'toggle_4_no').set
browser.radio(:id => 'toggle_5_yes').set
elsif
browser.url == 'http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=NY'
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id=> 'toggle_4_no').set
browser.radio(:id => 'toggle_5_yes').set
sleep 2
browser.button(:id => 'submit_tpv_button').click
sleep 2
browser.radio(:id => 'toggle_6_no').set
elsif
browser.url == 'http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=PA'
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
browser.url == 'http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=MD'
browser.radio(:id => 'toggle_3_no').set
browser.radio(:id => 'toggle_4_no').set
browser.radio(:id => 'toggle_5_yes').set
elsif
browser.url == 'http://www.pt.energypluscompany.com/myinbound/disclosure_state.php?state_abbrev=DC'
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
CSV.open('C:\\Scripts\\Inbound\\States\\NRG_Electric_Gas_Conf_data.csv', 'ab') do |csv|
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