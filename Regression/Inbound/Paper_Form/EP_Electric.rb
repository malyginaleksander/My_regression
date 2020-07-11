require 'rubygems'
require 'watir-webdriver'
require 'win32ole' 
require 'csv'

rows = 2
while  
rows <= 25		#25

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\Inbound\\Paper_Form\\Form_Data.xlsx")
worksheet = workbook.worksheets(1)

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
account_type=worksheet.cells(rows,"K").value
business_name=worksheet.cells(rows,"L").value
email=worksheet.cells(rows,"M").value
utility=worksheet.cells(rows,"N").value
account_number=worksheet.cells(rows,"O").value.to_s
service_ref=worksheet.cells(rows,"P").value.to_s
greenopt=worksheet.cells(rows,"Q").value
partner=worksheet.cells(rows,"R").value
campaign=worksheet.cells(rows,"S").value
promo=worksheet.cells(rows,"T").value

browser = Watir::Browser.new :firefox
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
browser.select_list(:name => 'account_type').select account_type

if
browser.text_field(:name => 'business_name').visible?
browser.text_field(:name => 'business_name').set business_name
end

#Billing Information
browser.checkbox(:name => 'copyinfo').set
browser.checkbox(:name => 'copyinfo').fire_event 'onclick'
browser.text_field(:name => 'email').set email

#Electric
browser.select_list(:name => 'electric_utility').select utility
browser.text_field(:name => 'electric_account_number').set account_number

if 
browser.text_field(:name => 'electric_extra_account_number').visible?
browser.text_field(:name => 'electric_extra_account_number').set service_ref
end

if 
greenopt=worksheet.cells(rows,"R").value == "yes"
browser.checkbox(:name => 'electric_green').set
else
greenopt_check=worksheet.cells(rows,"R").value == "no"
browser.checkbox(:name => 'electric_green').clear
end

#Order Information
browser.text_field(:name => 'partner_code').set partner
browser.text_field(:name => 'campaign_code').set campaign
if 
browser.text_field(:name => 'promo_code').visible?
browser.text_field(:name => 'promo_code').set promo
else
browser.text_field(:name => 'elec_promo_code').set promo
end
sleep 4

#Vendor ID
browser.select_list(:name => 'vendor_id').select ("EPIB")

CSV.open('C:\\Scripts\\Inbound\\Paper_Form\\EP_electric_Conf_data.csv', 'ab') do |csv|
csv << [browser.div(:class => 'enrollmentheader').text.slice(-7..-1), partner=worksheet.cells(rows,"V").value, campaign=worksheet.cells(rows,"W").value,
promo=worksheet.cells(rows,"X").value]
end
sleep 2

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