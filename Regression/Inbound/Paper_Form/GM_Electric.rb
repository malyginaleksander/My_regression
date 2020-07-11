require 'rubygems'
require 'watir-webdriver'
require 'win32ole' 
require 'csv'

rows = 2	#2
while  
rows <= 15	#23	

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\Inbound\\Paper_Form\\Form_Data.xlsx")
worksheet = workbook.worksheets(3)

brand=worksheet.cells(rows,"A").value
first_name=worksheet.cells(rows,"B").value
last_name=worksheet.cells(rows,"C").value
address=worksheet.cells(rows,"D").value
city=worksheet.cells(rows,"E").value
state=worksheet.cells(rows,"F").value
zip=worksheet.cells(rows,"G").value
area_code=worksheet.cells(rows,"H").value
prefix=worksheet.cells(rows,"I").value.to_s
last=worksheet.cells(rows,"J").value.to_s
email=worksheet.cells(rows,"K").value
spanish=worksheet.cells(rows,"L").value
utility=worksheet.cells(rows,"M").value
account_number=worksheet.cells(rows,"P").value.to_s
srn=worksheet.cells(rows,"Q").value.to_s
rate_class=worksheet.cells(rows,"R").value
zone=worksheet.cells(rows,"S").value
product=worksheet.cells(rows,"T").value

browser = Watir::Browser.new
browser.goto 'http://www.pt.energypluscompany.com/myinbound/login.php'

#login
browser.text_field(:name => 'email').set ('mpeters@energypluscompany.com')
browser.text_field(:name => 'password').set ('energy')
browser.button(:value => ' Login').click

browser.goto 'http://www.pt.energypluscompany.com/myinbound/paper.php'
sleep 2

browser.button(:id => brand).click
Watir::Wait.until {browser.text.include? "Confirmation Code"}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Inbound - Paper Application')

#Customer Information
browser.text_field(:name => 'customer_first_name').set first_name
browser.text_field(:name => 'customer_last_name').set last_name
browser.text_field(:name => 'customer_address1').set address
browser.text_field(:name => 'customer_city').set city
browser.select_list(:name => 'customer_state').select state
browser.text_field(:name => 'customer_zip5').set zip
browser.text_field(:name => 'customer_area_code').set area_code
browser.text_field(:name => 'customer_prefix').set prefix
browser.text_field(:name => 'customer_line_number').set last
browser.select_list(:name => 'account_type').select("Residential")

#Billing
browser.checkbox(:name => 'copyinfo').set
browser.checkbox(:name => 'copyinfo').fire_event 'onclick'
browser.text_field(:name => 'email').set email

#Utility
browser.select_list(:name => 'electric_utility').select utility
if
browser.text_field(:name => 'electric_account_number').visible?
browser.text_field(:name => 'electric_account_number').set account_number
end

if
browser.text_field(:name => 'electric_extra_account_number').visible?
browser.text_field(:name => 'electric_extra_account_number').set srn
end


if
browser.radio(:name => 'coned_zone', :value => 'NYC').visible?
browser.radio(:name => 'coned_zone', :value => zone).click
end

if
spanish=worksheet.cells(rows,"L").value == "yes"
browser.checkbox(:name => 'spanishbill').set
end



#Product
sleep 2
browser.select_list(:name => 'electric_products_gme').select product
sleep 2

#Vendor ID
browser.select_list(:name => 'vendor_id').select ("EPIB")

CSV.open('C:\\Scripts\\Inbound\\Paper_Form\\GM_Electric_Conf_data.csv', 'ab') do |csv|
csv << [browser.div(:class => 'enrollmentheader').text.slice(-7..-1)]
end
sleep 3

browser.button(:name => 'submit').click

sleep 1
browser.close 

rows=rows+1

$end
workbook.Save
workbook.Close
end

$end
sleep 2