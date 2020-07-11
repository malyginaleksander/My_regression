##############################################################
#need admin - manage employee roles - drop admin permissions
#Remove Save Rep from manage employee roles
#update xls with UAN and Customer Names
##############################################################

require 'rubygems'
require 'watir'
require 'win32ole'

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Finance/AdHocCashPayment.aspx'
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_AdhocCashPayment1_UpdatePanel1').exists?}
browser.select_list(:id, 'ctl00_MainContent_AdhocCashPayment1_ddlEntity').select("Employee")
sleep 1
browser.select_list(:id, 'ctl00_MainContent_AdhocCashPayment1_ddlPayee').select("Mike Boyle")
sleep 2
browser.select_list(:id, 'ctl00_MainContent_AdhocCashPayment1_ddlPaymentType').select("kWh")
browser.text_field(:id, 'ctl00_MainContent_AdhocCashPayment1_txtCashAmount').set("123")
browser.text_field(:id, 'ctl00_MainContent_AdhocCashPayment1_EPCalendar1_txtDatetime').set("01/01/2014")
browser.text_field(:id, 'ctl00_MainContent_AdhocCashPayment1_txtComment').set("test")
browser.button(:value,'Save').click
Watir::Waiter::wait_until {browser.text.include? "A new adhoc item payment has been added for Mike Boyle."}
browser.close

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Finance/AdHocCashPayment.aspx'
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_AdhocCashPayment1_UpdatePanel1').exists?}
browser.select_list(:id, 'ctl00_MainContent_AdhocCashPayment1_ddlEntity').select("Employee")
sleep 1
browser.select_list(:id, 'ctl00_MainContent_AdhocCashPayment1_ddlPayee').select("Mike Boyle")
sleep 1
browser.select_list(:id, 'ctl00_MainContent_AdhocCashPayment1_ddlPaymentType').select("Cash Payment")
browser.text_field(:id, 'ctl00_MainContent_AdhocCashPayment1_txtCashAmount').set("123")
browser.text_field(:id, 'ctl00_MainContent_AdhocCashPayment1_EPCalendar1_txtDatetime').set("01/01/2014")
browser.text_field(:id, 'ctl00_MainContent_AdhocCashPayment1_txtComment').set("test")
browser.button(:value,'Save').click
Watir::Waiter::wait_until {browser.text.include? "A new adhoc item payment has been added for Mike Boyle."}
browser.close