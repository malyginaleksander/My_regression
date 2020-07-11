##############################################################
#need admin - manage employee roles - drop admin permissions
#Remove Save Rep from manage employee roles
#update xls with UAN and Customer Names
##############################################################

require 'rubygems'
require 'watir'
require 'win32ole'

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Finance/CreatePayments.aspx'
browser.select_list(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_ddlPayeeType').select("Employee")
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_txtLastName').set("Huning")
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_EPCalendar_Two_Inputs1_txtDateTimeStart').set("06/01/2015")
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_EPCalendar_Two_Inputs1_txtDateTimeEnd').set("09/28/2015")
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_lvTable').exists?}
browser.checkbox(:id, "ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_chkBxHeader").set
sleep 10
browser.button(:value => 'Create Cash Payment').click
Watir::Waiter::wait_until {browser.text.include? "Please verify the information is correct and click [OK] to create a cash payment."}
browser.close


