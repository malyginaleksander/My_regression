require 'rubygems'
require 'watir-webdriver'
require "win32ole"
require 'csv'

rows = 2	#2
while    
rows <= 3		#26

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\NRG\\Enrollments\\NRG_Data.xlsx")
worksheet = workbook.worksheets(3)

url=worksheet.cells(rows,"A").value.to_s
first_name=worksheet.cells(rows,"B").value.to_s
last_name=worksheet.cells(rows,"C").value
email_addr=worksheet.cells(rows,"F").value
confirm_email_addr=worksheet.cells(rows,"G").value
Service_Address1=worksheet.cells(rows,"H").value
city=worksheet.cells(rows,"I").value.to_s
zip=worksheet.cells(rows,"J").value.to_s
Service_phone_number=worksheet.cells(rows,"K").value.to_s
accountNo=worksheet.cells(rows,"L").value.to_s
gas_util=worksheet.cells(rows,"M").value.to_s
gasNo=worksheet.cells(rows,"N").value.to_s

browser = Watir::Browser.new :firefox
string_from_excel = "goto"
browser.send string_from_excel, url
sleep 2

browser.img(:xpath => "/html/body/div/div[2]/center[2]/font/span/a/img").click

browser.text_field(:id => 'id_first_name').set first_name
browser.text_field(:id => 'id_last_name').set last_name
browser.text_field(:id => 'id_email').set email_addr
browser.text_field(:id => 'id_ver_email').set confirm_email_addr
browser.text_field(:id => 'id_phone').set Service_phone_number
browser.text_field(:id => 'id_service_address_1').set Service_Address1
browser.text_field(:id => 'id_service_address_city').set city
browser.text_field(:id => 'id_service_address_zip').set zip
browser.checkbox(:id =>  'id_billing_same').clear
browser.checkbox(:id => 'id_billing_same').set
browser.text_field(:id => 'id_electric-uan').set accountNo
sleep 2
browser.select_list(:id => "id_gas-utility_slug").select gas_util
sleep 2
if
browser.text_field(:id => 'id_gas-uan').exists?
browser.text_field(:id => 'id_gas-uan').set gasNo
sleep 2
end
browser.button(:id => 'continue-submit').click
sleep 4

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('NRG Home Power')
browser.div(:class => "tos-section").send_keys [:control, :end]

browser.checkbox(:id, "id_order_authorization").set

if
browser.checkbox(:id, "id_affiliate_consent").exists?
browser.checkbox(:id, "id_affiliate_consent").set
end

browser.button(:value,"Submit").click

CSV.open('C:\\Scripts\\NRG\\Enrollments\\dual_enroll_Conf_data.csv', 'ab') do |csv|
csv << [browser.div(:id => 'confirmation').text]
end

sleep 1
browser.close 
rows=rows+1

$end
workbook.Save
workbook.Close

end
$end
sleep 1