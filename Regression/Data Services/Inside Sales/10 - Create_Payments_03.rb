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
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_EPCalendar_Two_Inputs1_txtDateTimeStart').set("02/28/2015")
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_EPCalendar_Two_Inputs1_txtDateTimeEnd').set("09/28/2015")
browser.button(:value => 'Search').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_lvTable').exists?}
browser.link(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_ctrl0_LinkButton1').click
Watir::Waiter::wait_until {browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_ctrl0_ucCompensationItemEdit_txtComment').exists?}
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_ctrl0_ucCompensationItemEdit_txtComment').set("test")
browser.select_list(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_ctrl0_ucCompensationItemEdit_ddlStatus').select("Void")
Watir::Waiter::wait_until {browser.checkbox(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_ctrl0_ucCompensationItemEdit_chkBoxUnqualifiedSale').exists?}
browser.checkbox(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_ctrl0_ucCompensationItemEdit_chkBoxUnqualifiedSale').set
browser.button(:value => 'Save').click
sleep 70
browser.span(:xpath => '//*[@id="__tab_ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh"]').click
browser.select_list(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_ddlPayeeType').select("Employee")
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_txtLastNameKwh').set("Huning")
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_EPCalendar_Two_Inputs1_txtDateTimeStartKWH').set("02/01/2015")
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_EPCalendar_Two_Inputs1_txtDateTimeEndKWH').set("07/28/2015")
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_lvTable').exists?}
browser.link(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_ctrl0_LinkButton1').click
Watir::Waiter::wait_until {browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_ctrl0_ucCompensationItemEdit_txtComment').exists?}
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_ctrl0_ucCompensationItemEdit_txtComment').set("test")
browser.select_list(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_ctrl0_ucCompensationItemEdit_ddlStatus').select("Void")
Watir::Waiter::wait_until {browser.checkbox(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_ctrl0_ucCompensationItemEdit_chkBoxUnqualifiedSale').exists?}
browser.checkbox(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_ctrl0_ucCompensationItemEdit_chkBoxUnqualifiedSale').set
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_ctrl0_ucCompensationItemEdit_btnSave').click
sleep 25
browser.close
