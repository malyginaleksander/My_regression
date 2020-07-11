require 'rubygems'
require 'watir-webdriver'
require "win32ole"
require 'csv'

###################
#  Illinois       #
###################

rows = 2		#2
while    
rows <= 5		#5

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\EP_Web\\Enrollments\\IL\\IL_Data.xlsx")
worksheet = workbook.worksheets(1) 

site_one=worksheet.cells(rows,"A").value
first_name=worksheet.cells(rows,"B").value
middle_initial=worksheet.cells(rows,"C").value
last_name=worksheet.cells(rows,"D").value
email_addr=worksheet.cells(rows,"G").value
confirm_email_addr=worksheet.cells(rows,"H").value
Service_Address1=worksheet.cells(rows,"I").value

zip=worksheet.cells(rows,"J").value.to_s
Service_phone_number=worksheet.cells(rows,"K").value.to_s
elect_gas_radio=worksheet.cells(rows,"L").value
LocalUtility=worksheet.cells(rows,"M").value
account_type=worksheet.cells(rows,"N").value
greenopt_check=worksheet.cells(rows,"O").value
gastypesel=worksheet.cells(rows,"P").value
accountNo=worksheet.cells(rows,"S").value.to_s 
servicereference=worksheet.cells(rows,"T").value.to_s
busnamedet=worksheet.cells(rows,"U").value
pfname=worksheet.cells(rows,"V").value
plname=worksheet.cells(rows,"W").value
price=worksheet.cells(rows,"X").value
con1=worksheet.cells(rows,"Z").value
con2=worksheet.cells(rows,"AA").value
con3=worksheet.cells(rows,"AB").value

browser = Watir::Browser.new :firefox
browser.goto 'http://www.pt.energypluscompany.com/resetsession.php'

string_from_excel = "goto"
browser.send string_from_excel, site_one
browser.link(:text => 'Enroll').click

#Personal Information
browser.text_field(:id => 'first_name').set first_name
browser.text_field(:id => 'middle_initial').set middle_initial
browser.text_field(:id => 'last_name').set last_name
browser.text_field(:id => 'email_addr').set email_addr
browser.text_field(:id => 'confirm_email_addr').set confirm_email_addr
browser.text_field(:id => 'Service_Address1').set Service_Address1
browser.text_field(:id => 'Service_Address2').set("apt 2a")
browser.text_field(:id => 'Service_City').set('Antioch')
browser.text_field(:id => 'Service_Zip5').set zip
browser.text_field(:name => 'Service_phone_number').set Service_phone_number
browser.checkbox(:id => 'billing').set
browser.image(:alt, 'Continue').click

#Utility Information
if
browser.radio(:id => 'chkGasNo').exists?
browser.radio(:id => elect_gas_radio).set 
browser.radio(:id => elect_gas_radio).fire_event 'onclick'
end

#Electric
if
browser.div(:id => 'AccountMainElectric').visible?
browser.div(:id => 'AccountMainElectric').select_list(:class => 'LocalUtility').fire_event 'onClick'
browser.div(:id => 'AccountMainElectric').select_list(:class => 'LocalUtility').select LocalUtility
browser.div(:id => 'AccountMainElectric').select_list(:class => 'LocalUtility').fire_event 'onClick'
browser.div(:id => 'AccountMainElectric').select_list(:class => 'resbus').select ('Please Choose...')
browser.div(:id => 'AccountMainElectric').select_list(:class => 'resbus').fire_event 'onClick'
browser.div(:id => 'AccountMainElectric').select_list(:class => 'resbus').select account_type
browser.div(:id => 'AccountMainElectric').select_list(:class => 'resbus').fire_event 'onClick'
browser.div(:id => 'AccountMainElectric').text_field(:class => 'accountNo').set accountNo

if
browser.text_field(:class => 'busnamedet').visible?
browser.text_field(:class => 'busnamedet').set busnamedet
browser.select_list(:class => 'drpTaxYes').select ('Please Choose...')
browser.select_list(:class => 'drpTaxYes').select ("No, I'm non-exempt")
end

if 
greenopt_check=worksheet.cells(rows,"O").value == "yes"
browser.checkbox(:class => 'greenopt').set 
browser.img(:id => 'btnUtilSubmit').click
else
greenopt_check=worksheet.cells(rows,"O").value == "no"
browser.img(:id => 'btnUtilSubmit').click
end
end

=begin
#Gas
if
browser.div(:id => 'AccountMainGas').visible?
browser.div(:id => 'AccountMainGas',).select_list(:class => 'LocalUtility').select ('Please Choose...')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'LocalUtility').fire_event 'onClick'
browser.div(:id => 'AccountMainGas',).select_list(:class => 'LocalUtility').select LocalUtility
browser.div(:id => 'AccountMainGas',).select_list(:class => 'LocalUtility').fire_event 'onClick'
browser.div(:id => 'AccountMainGas',).select_list(:class => 'resbus').select ('Please Choose...')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'resbus').fire_event 'onClick'
browser.div(:id => 'AccountMainGas',).select_list(:class => 'resbus').select account_type
browser.div(:id => 'AccountMainGas',).select_list(:class => 'resbus').fire_event 'onClick'
if
browser.select_list(:class => 'gastypesel').visible?
browser.select_list(:class => 'gastypesel').select ('Please Choose...')
browser.select_list(:class => 'gastypesel').fire_event 'onClick'
browser.select_list(:class => 'gastypesel').select gastypesel
browser.select_list(:class => 'gastypesel').fire_event 'onClick'
end
browser.div(:id => 'AccountMainGas',).text_field(:class => 'accountNo').set accountNo
if
browser.div(:id => 'AccountMainGas',).text_field(:class => 'usage_units').visible?
browser.div(:id => 'AccountMainGas',).text_field(:class => 'usage_units').set ('223')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'usage_month').select ('Please Choose...')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'usage_month').fire_event 'onClick'
browser.div(:id => 'AccountMainGas',).select_list(:class => 'usage_month').select ('July')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'usage_month').fire_event 'onClick'
end
if
browser.div(:id => 'AccountMainGas',).text_field(:class => 'busnamedet').visible?
browser.div(:id => 'AccountMainGas',).text_field(:class => 'busnamedet').set busnamedet
end
browser.img(:id => 'btnUtilSubmit').click
end
=end

#Rewards Information
if
browser.text_field(:id => 'partner_memnum').exists?
browser.text_field(:id => 'partner_memnum').set("2198765432")
browser.text_field(:id => 'pfname').set pfname
browser.text_field(:id => 'plname').set plname
browser.img(:id => 'partnerSubmitbtn').click
end


#Submit
browser.radio(:id => 'authorizeYes').fire_event 'onclick'
browser.radio(:id => 'authorizeYes').click
browser.button(:id => 'submitbutton').click

CSV.open('C:\\Scripts\\EP_Web\\Enrollments\\IL\\IL_Conf_data.csv', 'ab') do |csv|
csv << [browser.span(:id => 'confirmationCode').text, price=worksheet.cells(rows,"X").value, con1=worksheet.cells(rows,"Z").value,
con2=worksheet.cells(rows,"AA").value, con3=worksheet.cells(rows,"AB").value]
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