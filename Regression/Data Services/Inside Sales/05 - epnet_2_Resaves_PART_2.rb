##############################################################
#need admin - manage employee roles - drop admin permissions
#ADD Save Rep from manage employee roles
#update xls with UAN and Customer Names
##############################################################

require 'rubygems'
require 'watir'
require 'win32ole'

rows = 9	#9
while    
rows <= 11	#11

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\EP_NET\\Inside Sales\\epnet_2_Saves_predrop_data.xlsx")
worksheet = workbook.worksheets(1) 

uan=worksheet.cells(rows,"A").value.to_s
num=worksheet.cells(rows,"B").value.to_s
test_case=worksheet.cells(rows,"C").value.to_s

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/login.aspx'
browser.text_field(:id => 'ctl00_MainContent_txtUsername').set ("mpetersqa")
browser.text_field(:id => 'ctl00_MainContent_txtPassword').set ("Welcome13")
browser.button(:id => 'ctl00_MainContent_btnLogin').click
Watir::Waiter::wait_until {browser.text.include? "Total Records"}
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
browser.select_list(:id => 'FormCALLType').select("DROP REWORK")
sleep 2
browser.select_list(:id => 'FormCALLReason').select("RATE")
sleep 2
browser.select_list(:id => 'FormINOUT').select("INBOUND CALL")
sleep 2
browser.select_list(:id => 'FormDisposition').select("SAVE")
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
sleep 2
browser.text.include? "Save was successful"

sleep 1
browser.close 
rows=rows+1

$end
workbook.Save
workbook.Close
end

$end
sleep 1