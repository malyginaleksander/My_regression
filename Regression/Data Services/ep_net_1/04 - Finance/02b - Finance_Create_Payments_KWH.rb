require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Finance/CreatePayments.aspx'

#Results are populating on the Page Correctly
browser.span(:xpath => '//*[@id="__tab_ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh"]').click
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_lvTable').exists?}
if
browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_lvTable').exists?
print "KWH Results are populating on the Page Correctly - Passed", "\n"
else
print "KWH Results are populating on the Page Correctly - Failed", "\n"
end
browser.link(:id, "ctl00_ucTabNavigation_hlFinanceCreatePayments").click

#Search by Payee Last Name
browser.span(:xpath => '//*[@id="__tab_ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh"]').click
browser.select_list(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_ddlPayeeType').select("Employee")
sleep 1
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_txtLastNameKwh').set('bean')
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_lvTable').exists?}
if
browser.table(:xpath => '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/table/tbody/tr[3]/td/div/table/tbody/tr[2]/td[3]').text.include? "Matthew Bean"
print "KWH Search by Payee Last Name - Passed", "\n"
else
print "KWH Search by Payee Last Name - Failed", "\n"
end
browser.link(:id, "ctl00_ucTabNavigation_hlFinanceCreatePayments").click

#Filter Date by Range (Date start and Date end)
browser.span(:xpath => '//*[@id="__tab_ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh"]').click
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_EPCalendar_Two_Inputs1_txtDateTimeStartKWH').set("02/02/2013")
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_EPCalendar_Two_Inputs1_txtDateTimeEndKWH').set("03/01/2013")
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_lvTable').exists?}

if
browser.text.include? "01/02/2013"
print "KWH Start Date - Passed", "\n"
else
print "KWH Start Date - Failed", "\n"
end
if
browser.text.include? "01/10/2013"
print "KWH Start Date - Failed", "\n"
else
print "KWH Start Date - Passed", "\n"
end
if
browser.text.include? "01/11/2013"
print "KWH End Date - Passed", "\n"
else
print "KWH End Date - Failed", "\n"
end
if
browser.text.include? "01/12/2013"
print "KWH End Date - Failed", "\n"
else
print "KWH End Date - Passed", "\n"
end

#Reset button Clears Search Fields
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_btnReset').click
sleep 20
Watir::Waiter::wait_until {browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_EPCalendar_Two_Inputs1_txtDateTimeStartKWH').text.include? ""}
if
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_EPCalendar_Two_Inputs1_txtDateTimeStartKWH').text.include? ""
print "KWH Reset fields - Passed", "\n"
else
print "KWH Reset Fields - Failed", "\n"
end
sleep 5
browser.link(:id, "ctl00_ucTabNavigation_hlFinanceCreatePayments").click

#Search By Status
browser.span(:xpath => '//*[@id="__tab_ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh"]').click
browser.select_list(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_ddlStatus').select ("Ready to Pay")
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_lvTable').exists?}
if
browser.span(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_ctrl0_lblStatus').text.include? "Ready to Pay"
print "KWH Search By Status - Passed", "\n"
else
print "KWH Search By Status - Failed", "\n"
end

#Paging on Grid Functions Correctly
#Next Page
browser.link(:id, "ctl00_ucTabNavigation_hlFinanceCreatePayments").click
browser.span(:xpath => '//*[@id="__tab_ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh"]').click
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_lvTable').exists?}
browser.link(:xpath => '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/table[2]/tbody/tr[2]/td/div/span/a[13]').click
sleep 10
if
browser.span(:xpath => '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/table[2]/tbody/tr[2]/td/div/span/span').text.include? "2"
print "KWH Next Page - Passed", "\n"
else
print "KWH Next Page - Failed", "\n"
end

#Previous Page
browser.link(:xpath => '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/table[2]/tbody/tr[2]/td/div/span/a[2]').click
sleep 10
if
browser.span(:xpath => '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/table[2]/tbody/tr[2]/td/div/span/span').text.include? "1"
print "KWH Previous Page - Passed", "\n"
else
print "KWH Previous Page - Failed", "\n"
end

#Select Page
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucDataPager_ctl03_txtPage').set('10')
browser.link(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucDataPager_ctl03_GoButton').click
sleep 10
if
browser.span(:xpath => '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/table[2]/tbody/tr[2]/td/div/span/span').text.include? "10"
print "KWH Select Page - Passed", "\n"
else
print "KWH Select Page - Failed", "\n"
end

#First Page
browser.link(:text => '<<').click
sleep 10
if
browser.span(:xpath => '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/div/table[2]/tbody/tr[2]/td/div/span/span').text.include? "1"
print "KWH First Page - Passed", "\n"
else
print "KWH First Page - Failed", "\n"
end

#Records Per Page
browser.link(:id => 'ctl00_ucTabNavigation_hlFinanceCreatePayments').click
browser.span(:xpath => '//*[@id="__tab_ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh"]').click
browser.select_list(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucPaginator_ddlRowsPerPage').select ("100")
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_ucCashPaymentFilter_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_lvTable').exists?}
if 
browser.div(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelkWh_CompensationPaymentKWH_lvPendingPayments_ctrl99_hplPremise').exists?
print "KWH Records per page - Passed", "\n"
else
print "KWH Records per page - Failed", "\n"
end
