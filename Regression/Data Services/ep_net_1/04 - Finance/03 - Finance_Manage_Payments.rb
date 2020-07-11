require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet1.pt.nrgpl.us/Finance/ManagePayments.aspx'

#Results are populating on the Page Correctly
browser.button(:id => 'ctl00_MainContent_CashPayment2_CashPaymentFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_CashPayment2_lvPendingPayments_itemPlaceholderContainer').exists?}
if
browser.table(:id => 'ctl00_MainContent_CashPayment2_lvPendingPayments_itemPlaceholderContainer').exists?
print "Results are populating on the Page Correctly - Passed", "\n"
else
print "Results are populating on the Page Correctly - Failed", "\n"
end
browser.link(:id, "ctl00_ucTabNavigation_hlFinanceManagePayments").click

#Search by Payee Last Name
browser.text_field(:id => 'ctl00_MainContent_CashPayment2_CashPaymentFilter1_txtLastName').set('lile')
browser.button(:id => 'ctl00_MainContent_CashPayment2_CashPaymentFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_CashPayment2_lvPendingPayments_itemPlaceholderContainer').exists?}
if
browser.table(:xpath => '/html/body/form/div[3]/div[2]/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td[2]').text.include? "Stuart Lile"
print "Search by Payee Last Name - Passed", "\n"
else
print "Search by Payee Last Name - Failed", "\n"
end
browser.link(:id, "ctl00_ucTabNavigation_hlFinanceManagePayments").click

#Reset button Clears Search Fields
browser.button(:id => 'ctl00_MainContent_CashPayment2_CashPaymentFilter1_btnReset').click
Watir::Waiter::wait_until {browser.text_field(:id => 'ctl00_MainContent_CashPayment2_CashPaymentFilter1_txtLastName').text.include? ""}
if
browser.text_field(:id => 'ctl00_MainContent_CashPayment2_CashPaymentFilter1_txtLastName').text.include? ""
print "Reset fields - Passed", "\n"
else
print "Reset Fields - Failed", "\n"
end
sleep 5
browser.link(:id, "ctl00_ucTabNavigation_hlFinanceManagePayments").click

#Search By Status
browser.select_list(:id => 'ctl00_MainContent_CashPayment2_CashPaymentFilter1_ddlStatus').select ("Confirmed")
browser.button(:value,"Search").click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_CashPayment2_lvPendingPayments_itemPlaceholderContainer').exists?}
if
browser.table(:xpath => '/html/body/form/div[3]/div[2]/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[2]/td[5]').text.include? "Confirmed"
print "Search By Status - Passed", "\n"
else
print "Search By Status - Failed", "\n"
end
browser.link(:id, "ctl00_ucTabNavigation_hlFinanceManagePayments").click

#Paging on Grid Functions Correctly
#Next Page
browser.button(:id => 'ctl00_MainContent_CashPayment2_CashPaymentFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_CashPayment2_lvPendingPayments_itemPlaceholderContainer').exists?}
browser.link(:text => '>').click
sleep 5
if
browser.span(:xpath => '/html/body/form/div[3]/div[2]/div[2]/table[2]/tbody/tr[2]/td/div/span/span').text.include? "2"
print "Next Page - Passed", "\n"
else
print "Next Page - Failed", "\n"
end

#Previous Page
browser.link(:text => '<').click
sleep 5
if
browser.span(:xpath => '/html/body/form/div[3]/div[2]/div[2]/table[2]/tbody/tr[2]/td/div/span/span').text.include? "1"
print "Previous Page - Passed", "\n"
else
print "Previous Page - Failed", "\n"
end

#Select Page
browser.text_field(:id => 'ctl00_MainContent_CashPayment2_ucDataPager_ctl03_txtPage').set('4')
browser.link(:id => 'ctl00_MainContent_CashPayment2_ucDataPager_ctl03_GoButton').click
sleep 5
if
browser.span(:xpath => '/html/body/form/div[3]/div[2]/div[2]/table[2]/tbody/tr[2]/td/div/span/span').text.include? "4"
print "Select Page - Passed", "\n"
else
print "Select Page - Failed", "\n"
end

#First Page
browser.link(:text => '<<').click
sleep 5
if
browser.span(:xpath => '/html/body/form/div[3]/div[2]/div[2]/table[2]/tbody/tr[2]/td/div/span/span').text.include? "1"
print "First Page - Passed", "\n"
else
print "First Page - Failed", "\n"
end

#Records Per Page
browser.link(:id => 'ctl00_ucTabNavigation_hlFinanceManagePayments').click
browser.select_list(:id => 'ctl00_MainContent_CashPayment2_ucPaginator_ddlRowsPerPage').select ("100")
browser.button(:id => 'ctl00_MainContent_CashPayment2_CashPaymentFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_CashPayment2_lvPendingPayments_itemPlaceholderContainer').exists?}
if 
browser.div(:id => 'ctl00_MainContent_CashPayment2_lvPendingPayments_ctrl80_Tr1').exists?
print "Records per page - Passed", "\n"
else
print "Records per page - Failed", "\n"
end
=begin
#Generate a Report for Payment
browser.button(:id => 'ctl00_MainContent_CashPayment2_CashPaymentFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_CashPayment2_lvPendingPayments_itemPlaceholderContainer').exists?}
browser.link(:id => 'ctl00_MainContent_CashPayment2_lvPendingPayments_ctrl1_hplEdit').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_ucCompensation_tbContainer_body').exists?}
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_btnGenerateReport').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_lvTable').exists?}
if
browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_lvTable').exists?
print "Generate a Report for Payment - Passed", "\n"
else
print "Generate a Report for Payment - Failed", "\n"
end

#Edit a Payment
browser.link(:id => 'ctl00_ucTabNavigation_hlFinanceManagePayments').click
browser.button(:id => 'ctl00_MainContent_CashPayment2_CashPaymentFilter1_btnSearch').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_CashPayment2_lvPendingPayments_itemPlaceholderContainer').exists?}
browser.link(:id => 'ctl00_MainContent_CashPayment2_lvPendingPayments_ctrl1_hplEdit').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_ucCompensation_tbContainer_body').exists?}
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_btnGenerateReport').click
Watir::Waiter::wait_until {browser.table(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_lvTable').exists?}
browser.link(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_ctrl0_LinkButton1').click
Watir::Waiter::wait_until {browser.div(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_ctrl0_divComment').exists?}
browser.text_field(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_ctrl0_ucCompensationItemEdit_txtComment').set ("Test")
browser.button(:id => 'ctl00_MainContent_ucCompensation_tbContainer_tbPanelMonetary_ucCompensationPayment_lvPendingPayments_ctrl0_ucCompensationItemEdit_btnSave').click
Watir::Waiter::wait_until {browser.text.include? "Test"}
if 
browser.text.include? "Test"
print "Edit a Payment - Passed", "\n"
else
print "Edit a Payment - Failed", "\n"
end
=end
browser.close