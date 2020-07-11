require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Finance/CreatePayments.aspx'


#Results are populating on the Page Correctly
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_lvTable').exists?}
if
browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_lvTable').exists?
print "Monetary Results are populating on the Page Correctly - Passed", "\n"
else
print "Monetary Results are populating on the Page Correctly - Failed", "\n"
end
browser.link(:id, "ctl00_ucTabNavigation_hlFinanceCreatePayments").click

#Search by Payee Last Name
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_txtLastName').set('bean')
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_lvTable').exists?}
if
browser.table(:xpath => '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div/div/table/tbody/tr[3]/td/div/table/tbody/tr[2]/td[4]').text.include? "Matthew Bean"
print "Monetary Search by Payee Last Name - Passed", "\n"
else
print "Monetary Search by Payee Last Name - Failed", "\n"
end
browser.link(:id, "ctl00_ucTabNavigation_hlFinanceCreatePayments").click

#Filter Date by Range (Date start and Date end)
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_EPCalendar_Two_Inputs1_txtDateTimeStart').set("07/31/2014")
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_EPCalendar_Two_Inputs1_txtDateTimeEnd').set("08/01/2014")
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_lvTable').exists?}

if
browser.text.include? "7/31/2014"
print "Monetary Start Date - Passed", "\n"
else
print "Monetary Start Date - Failed", "\n"
end
if
browser.text.include? "7/30/2014"
print "Monetary Start Date - Failed", "\n"
else
print "Monetary Start Date - Passed", "\n"
end
if
browser.text.include? "8/1/2014"
print "Monetary End Date - Passed", "\n"
else
print "Monetary End Date - Failed", "\n"
end
if
browser.text.include? "8/2/2014"
print "Monetary End Date - Failed", "\n"
else
print "Monetary End Date - Passed", "\n"
end

#Reset button Clears Search Fields
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_btnReset').click
sleep 20
Watir::Waiter::wait_until {browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_EPCalendar_Two_Inputs1_txtDateTimeStart').text.include? ""}
if
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_EPCalendar_Two_Inputs1_txtDateTimeStart').text.include? ""
print "Monetary Reset fields - Passed", "\n"
else
print "Monetary Reset Fields - Failed", "\n"
end
sleep 5
browser.link(:id, "ctl00_ucTabNavigation_hlFinanceCreatePayments").click

#Search By Status
browser.select_list(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_ddlStatus').select ("Pending")
browser.button(:value,"Search").click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_lvTable').exists?}
if
browser.span(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_ctrl0_lblStatus').text.include? "Pending"
print "Monetary Search By Status - Passed", "\n"
else
print "Monetary Search By Status - Failed", "\n"
end
browser.link(:id, "ctl00_ucTabNavigation_hlFinanceCreatePayments").click

#Paging on Grid Functions Correctly
#Next Page
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_lvTable').exists?}
browser.link(:text => '>').click
sleep 10
if
browser.span(:xpath => '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div/div/table[2]/tbody/tr[2]/td/div/span/span').text.include? "2"
print "Monetary Next Page - Passed", "\n"
else
print "Monetary Next Page - Failed", "\n"
end
=begin
#Previous Page
browser.link(:text => '<').click
sleep 10
if
browser.span(:xpath => '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div/div/table[2]/tbody/tr[2]/td/div/span/span').text.include? "1"
print "Monetary Previous Page - Passed", "\n"
else
print "Monetary Previous Page - Failed", "\n"
end

#Select Page
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucDataPager_ctl03_txtPage').set('10')
browser.link(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucDataPager_ctl03_GoButton').click
sleep 10
if
browser.span(:xpath => '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div/div/table[2]/tbody/tr[2]/td/div/span/span').text.include? "10"
print "Monetary Select Page - Passed", "\n"
else
print "Monetary Select Page - Failed", "\n"
end

#First Page
browser.link(:text => '<<').click
sleep 10
if
browser.span(:xpath => '/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div/div/table[2]/tbody/tr[2]/td/div/span/span').text.include? "1"
print "Monetary First Page - Passed", "\n"
else
print "Monetary First Page - Failed", "\n"
end
=end
#Records Per Page
browser.link(:id => 'ctl00_ucTabNavigation_hlFinanceCreatePayments').click
browser.select_list(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucPaginator_ddlRowsPerPage').select ("100")
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_ucCashPaymentFilter_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_lvTable').exists?}
if 
browser.div(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_ctrl99_chkBxSelect').exists?
print "Monetary Records per page - Passed", "\n"
else
print "Monetary Records per page - Failed", "\n"
end

browser.close