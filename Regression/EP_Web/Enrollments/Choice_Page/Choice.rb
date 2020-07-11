require 'rubygems'
require 'watir-webdriver'
require "win32ole"
require 'csv'

############################################
#  Choice							       #
############################################

browser = Watir::Browser.new :firefox
browser.goto 'http://www.pt.energypluscompany.com/sywr/choice/'
if
browser.select_list(:xpath => '/html/body/div/div/div[3]/form/select/option[11]').exists?
print "too many states"
end
browser.close

rows = 2
while    
rows <= 7

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\EP_Web\\Enrollments\\Choice_Page\\Choice_Data.xlsx") #Edit this to point to your location.
worksheet = workbook.worksheets(1) 

state=worksheet.cells(rows,"A").value
first_name=worksheet.cells(rows,"b").value
middle_initial=worksheet.cells(rows,"C").value
last_name=worksheet.cells(rows,"D").value
email_addr=worksheet.cells(rows,"G").value
confirm_email_addr=worksheet.cells(rows,"H").value
Service_Address1=worksheet.cells(rows,"I").value
city=worksheet.cells(rows,"J").value
zip=worksheet.cells(rows,"K").value
Service_phone_number=worksheet.cells(rows,"L").value.to_s
elect_gas_radio=worksheet.cells(rows,"M").value
LocalUtility=worksheet.cells(rows,"N").value
account_type=worksheet.cells(rows,"O").value
greenopt_check=worksheet.cells(rows,"P").value
gastypesel=worksheet.cells(rows,"Q").value
accountNo=worksheet.cells(rows,"T").value.to_s #value.to_s removes error for limit_to_maxlength when cells have large numbers
sr_num=worksheet.cells(rows,"U").text
rateclassdet=worksheet.cells(rows,"V").value
busnamedet=worksheet.cells(rows,"W").value
memnum=worksheet.cells(rows,"X").value.to_s
pfname=worksheet.cells(rows,"Y").value
plname=worksheet.cells(rows,"Z").value

browser = Watir::Browser.new
browser.goto 'http://www.pt.energypluscompany.com/sywr/choice/'

sleep 2

browser.select_list(:id => 'state').select state
browser.link(:text => 'Enroll').click

if
browser.text.include? "There is a problem"
browser.link(:text => "Continue to this website (not recommended).").click
end

#Personal Information
browser.text_field(:id => 'first_name').set first_name
browser.text_field(:id => 'middle_initial').set middle_initial
browser.text_field(:id => 'last_name').set last_name
browser.text_field(:id => 'email_addr').set email_addr
browser.text_field(:id => 'confirm_email_addr').set confirm_email_addr
browser.text_field(:id => 'Service_Address1').set Service_Address1
browser.text_field(:id => 'Service_City').set city
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
browser.select_list(:class => 'LocalUtility').fire_event 'onClick'
browser.select_list(:class => 'LocalUtility').select LocalUtility
browser.select_list(:class => 'LocalUtility').fire_event 'onClick'
browser.select_list(:class => 'resbus').select ('Please Choose...')
browser.select_list(:class => 'resbus').fire_event 'onClick'
browser.select_list(:class => 'resbus').select account_type
browser.select_list(:class => 'resbus').fire_event 'onClick'
browser.text_field(:class => 'accountNo').set accountNo

if
browser.text_field(:class => 'accountNo2').visible?
browser.text_field(:class => 'accountNo2').set accountNo #account Number
browser.text_field(:class => 'accountNo').set sr_num #Service Reference Number
browser.text_field(:class => 'NameKeyValue').set ('Test')
browser.radio(:class => 'NameKeyValidator radiobutton', :value => '1').click
else
browser.text_field(:class => 'accountNo').set accountNo
end

if 
browser.select_list(:class => 'rateclassdet').visible?
browser.select_list(:class => 'rateclassdet').select ('Please Choose...')
browser.select_list(:class => 'rateclassdet').fire_event 'onClick'
browser.select_list(:class => 'rateclassdet').select rateclassdet
browser.select_list(:class => 'rateclassdet').fire_event 'onClick'
end

if
browser.div(:id => 'AccountMainElectric').select_list(:class => 'average_month_usage').visible?
browser.div(:id => 'AccountMainElectric').select_list(:class => 'average_month_usage').set ('Please Choose...')
browser.div(:id => 'AccountMainElectric').select_list(:class => 'average_month_usage').fire_event 'onClick'
browser.div(:id => 'AccountMainElectric').select_list(:class => 'average_month_usage').set ('Less than 10,000 kWh')
browser.div(:id => 'AccountMainElectric').select_list(:class => 'average_month_usage').fire_event 'onClick'
end

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

#Gas
if
browser.div(:id => 'AccountMainGas').exists? and browser.div(:id => 'AccountMainGas').visible?
browser.div(:id => 'AccountMainGas',).select_list(:class => 'LocalUtility').set ('Please Choose...')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'LocalUtility').fire_event 'onClick'
browser.div(:id => 'AccountMainGas',).select_list(:class => 'LocalUtility').set LocalUtility
browser.div(:id => 'AccountMainGas',).select_list(:class => 'LocalUtility').fire_event 'onClick'
browser.div(:id => 'AccountMainGas',).select_list(:class => 'resbus').set ('Please Choose...')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'resbus').fire_event 'onClick'
browser.div(:id => 'AccountMainGas',).select_list(:class => 'resbus').set account_type
browser.div(:id => 'AccountMainGas',).select_list(:class => 'resbus').fire_event 'onClick'
if
browser.select_list(:class => 'gastypesel').visible?
browser.div(:id => 'AccountMainGas',).select_list(:class => 'gastypesel').set ('Please Choose...')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'gastypesel').fire_event 'onClick'
browser.div(:id => 'AccountMainGas',).select_list(:class => 'gastypesel').set gastypesel
browser.div(:id => 'AccountMainGas',).select_list(:class => 'gastypesel').fire_event 'onClick'
end
browser.div(:id => 'AccountMainGas',).text_field(:class => 'accountNo').set accountNo
if
browser.div(:id => 'AccountMainGas',).text_field(:class => 'usage_units').visible?
browser.div(:id => 'AccountMainGas',).text_field(:class => 'usage_units').set ('223')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'usage_month').set ('Please Choose...')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'usage_month').fire_event 'onClick'
browser.div(:id => 'AccountMainGas',).select_list(:class => 'usage_month').set ('July')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'usage_month').fire_event 'onClick'
end
if
browser.div(:id => 'AccountMainGas',).text_field(:class => 'usage_units').visible?
browser.div(:id => 'AccountMainGas',).text_field(:class => 'usage_units').set ('223')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'usage_month').set ('Please Choose...')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'usage_month').fire_event 'onClick'
browser.div(:id => 'AccountMainGas',).select_list(:class => 'usage_month').set ('July')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'usage_month').fire_event 'onClick'
end
if
browser.div(:id => 'AccountMainGas',).text_field(:class => 'busnamedet').visible?
browser.div(:id => 'AccountMainGas',).text_field(:class => 'busnamedet').set busnamedet
browser.div(:id => 'AccountMainGas',).select_list(:class => 'drpTaxYes').set ('Please Choose...')
browser.div(:id => 'AccountMainGas',).select_list(:class => 'drpTaxYes').set ("No, I'm non-exempt")
end
browser.img(:id => 'btnUtilSubmit').click
end

#Rewards Information
if
browser.text_field(:id => 'partner_memnum').exists?
browser.text_field(:id => 'partner_memnum').set("2198765432")
browser.text_field(:id => 'pfname').set pfname
browser.text_field(:id => 'plname').set plname
end
browser.img(:id => 'partnerSubmitbtn').click

#Submit
browser.radio(:id => 'authorizeYes').fire_event 'onclick'
browser.radio(:id => 'authorizeYes').click
browser.button(:id => 'submitbutton').click

CSV.open('C:\\Scripts\\EP_Web\\Enrollments\\Choice_Page\\Choice_ConfCodes.csv', 'ab') do |csv|
csv << [browser.span(:id => 'confirmationCode').text
]
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