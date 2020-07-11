##############################################################
#need admin - manage employee roles - drop admin permissions
#Remove Save Rep from manage employee roles
#update xls with UAN and Customer Names
##############################################################

require 'rubygems'
require 'watir'
require 'win32ole'

rows = 15 #15
while    
rows <= 16 #16

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\EP_NET\\Inside Sales\\epnet_2_Saves_predrop_data.xlsx")
worksheet = workbook.worksheets(1) 

uan=worksheet.cells(rows,"A").value.to_s
num=worksheet.cells(rows,"B").value.to_s
test_case=worksheet.cells(rows,"C").value.to_s

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/member'
sleep 3

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Member Form')
browser.text_field(:id => 'memberFormSearchCriteria').set uan
browser.send_keys("{BACKSPACE}")
Watir::Waiter::wait_until {browser.div(:id => 'jqgh_SearchGrid_UtilityAccountNumber').exists?}
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[4]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').click
Watir::Waiter::wait_until {browser.div(:id => 'memberFormTabs').exists?}
browser.link(:id => 'accountCallsHref').click
Watir::Waiter::wait_until {browser.div(:class => 'ui-jqgrid-bdiv').exists?}
browser.button(:id => 'addACallButton').click
Watir::Waiter::wait_until {browser.div(:id => 'account-calls-form-left-column').exists?}
browser.select_list(:id => 'FormCALLType').select("CUSTOMER SERVICE")
sleep 2
browser.select_list(:id => 'FormCALLReason').select("AWARDS")
browser.select_list(:id => 'FormINOUT').select("INBOUND CALL")
browser.select_list(:id => 'FormDisposition').select("REFERRED TO WINBACK FOR SAVE")
sleep 2
browser.send_keys("{TAB}")
browser.send_keys("{TAB}")
browser.send_keys("{TAB}")
browser.send_keys("{TAB}")
browser.send_keys("{TAB}")
browser.send_keys("{TAB}")
browser.send_keys("{TAB}")
browser.send_keys("{TAB}")
browser.send_keys("{TAB}")
browser.send_keys("{TAB}")
browser.send_keys("{TAB}")
browser.send_keys("{TAB}")
browser.send_keys("{ENTER}")
Watir::Waiter::wait_until {browser.text.include? "Account Calls (All Accounts)"}
sleep 30
browser.table(:id => 'jqGridCompleteReferral').click
Watir::Waiter::wait_until {browser.select_list(:id => 'RWGroup').exists?}
browser.select_list(:id => 'RWGroup').select("mp - Peters, Michael")
browser.send_keys("{TAB}")
browser.send_keys("{ENTER}")

sleep 1
browser.close 
rows=rows+1

$end
workbook.Save
workbook.Close
end

$end
sleep 1