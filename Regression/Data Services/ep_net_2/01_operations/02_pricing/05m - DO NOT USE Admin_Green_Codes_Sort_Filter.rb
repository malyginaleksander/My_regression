require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Mismatched Green Codes")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

if
browser.div(:id => 'gbox_pricingAdminGrid').exists?
print "Results populating on page - Passed", "\n"
else
print "Results populating on page - Failed", "\n"
end

#Paging on the Detail grid functions correctly
#Next Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-next').click
Watir::Waiter::wait_until {browser.text.include? "View 101 - 200"}
if
browser.text.include? "View 101 - 200"
print "Admin Base Cost Next Page - Passed", "\n"
else
print "Admin Base Cost Next Page - Failed", "\n"
end

#Previous Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-prev').click
Watir::Waiter::wait_until {browser.text.include? "View 1 - 100"}
if
browser.text.include? "View 1 - 100"
print "Admin Base Cost Previous Page - Passed", "\n"
else
print "Admin Base Cost Previous Page - Failed", "\n"
end

#Last Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-end').click
Watir::Waiter::wait_until {browser.text.include? "View 144 401"}
if
browser.text.include? "View 144 401"
print "Admin Base Cost Last Page - Passed", "\n"
else
print "Admin Base Cost Last Page - Failed", "\n"
end

#First Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-first').click
Watir::Waiter::wait_until {browser.text.include? "View 1 - 100"}
if
browser.text.include? "View 1 - 100"
print "Admin Base Cost First Page - Passed", "\n"
else
print "Admin Base Cost First Page - Failed", "\n"
end

#Sort
#Last Name
browser.div(:id => 'jqgh_pricingAdminGrid_LastName').click
sleep 5
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "undefined"
print "Sort by Last Name ASC - Passed", "\n"
else
print "Sort by Last Name ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_LastName').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "ZYWIEC"
print "Sort by Last Name DESC - Passed", "\n"
else
print "Sort by Last Name DESC - Failed", "\n"
end

#First Name
browser.div(:id => 'jqgh_pricingAdminGrid_FirstName').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "."
print "Sort by First Name - Passed", "\n"
else
print "Sort by First Name - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_FirstName').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "ZYTWON"
print "Sort by First Name DESC - Passed", "\n"
else
print "Sort by First Name DESC - Failed", "\n"
end

#Green
browser.div(:id => 'jqgh_pricingAdminGrid_Green').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "03"
print "Sort by Green ASC - Passed", "\n"
else
print "Sort by UGreen ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_Green').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "018"
print "Sort by Green DESC - Passed", "\n"
else
print "Sort by Green DESC - Failed", "\n"
end

#VIP
browser.div(:id => 'jqgh_pricingAdminGrid_Vip').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "undefined"
print "Sort by VIP ASC - Passed", "\n"
else
print "Sort by VIP ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_Vip').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "018"
print "Sort by VIP DESC - Passed", "\n"
else
print "Sort by VIP DESC - Failed", "\n"
end

#SLP
browser.div(:id => 'jqgh_pricingAdminGrid_Spl').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[8]').text.include? "undefined"
print "Sort by SLP ASC - Passed", "\n"
else
print "Sort by SLP ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_Spl').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[8]').text.include? "WP01"
print "Sort by SLP DESC - Passed", "\n"
else
print "Sort by SLP DESC - Failed", "\n"
end

#Utility Code
browser.div(:id => 'jqgh_pricingAdminGrid_UtilityCode').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[9]').text.include? "01"
print "Sort by Utility Code ASC - Passed", "\n"
else
print "Sort by Utility Code ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_UtilityCode').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[9]').text.include? "60"
print "Sort by Utility Code DESC - Passed", "\n"
else
print "Sort by Utility Code DESC - Failed", "\n"
end

#Partner Code
browser.div(:id => 'jqgh_pricingAdminGrid_PartnerCode').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]').text.include? "AAL"
print "Sort by Partner Code ASC - Passed", "\n"
else
print "Sort by Partner Code ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_PartnerCode').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]').text.include? "WYN"
print "Sort by Partner Code DESC - Passed", "\n"
else
print "Sort by Partner Code DESC - Failed", "\n"
end

#Utility Billing City
browser.div(:id => 'jqgh_pricingAdminGrid_UtilityBillingCity').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[14]').text.include? "undefined"
print "Sort by Utility Billing City ASC - Passed", "\n"
else
print "Sort by Utility Billing City ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_UtilityBillingCity').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[14]').text.include? "ZULLINGER"
print "Sort by Utility Billing City DESC - Passed", "\n"
else
print "Sort by Utility Billing City DESC - Failed", "\n"
end

#Utility Billing State
browser.div(:id => 'jqgh_pricingAdminGrid_UtilityBillingSt').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[15]').text.include? "CA"
print "Sort by Utility Billing State ASC - Passed", "\n"
else
print "Sort by Utility Billing State ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_UtilityBillingSt').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[15]').text.include? "WY"
print "Sort by Utility Billing State DESC - Passed", "\n"
else
print "Sort by Utility Billing State DESC - Failed", "\n"
end

#Filter
wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 8

#Utility Account Number

#Last Name
browser.text_field(:id => 'gs_LastName').set("ZOOK")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "ZOOK"
print "Filter by Last Name - Passed", "\n"
else
print "Filter by Last Name - Failed", "\n"
end
browser.text_field(:id => 'gs_LastName').set("")
browser.send_keys("{ENTER}")

#First Name
browser.text_field(:id => 'gs_FirstName').set("CHARLES")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[5]').text.include? "CHARLES"
print "Filter by First Name - Passed", "\n"
else
print "Filter by First Name - Failed", "\n"
end
browser.text_field(:id => 'gs_FirstName').set("")
browser.send_keys("{ENTER}")

#Green
browser.text_field(:id => 'gs_Green').set("003")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "003"
print "Filter by Green - Passed", "\n"
else
print "Filter by Green - Failed", "\n"
end
browser.text_field(:id => 'gs_Green').set("")
browser.send_keys("{ENTER}")

#VIP
browser.text_field(:id => 'gs_Vip').set("006")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "011"
print "Filter by VIP - Passed", "\n"
else
print "Filter by VIP - Failed", "\n"
end
browser.text_field(:id => 'gs_Vip').set("")
browser.send_keys("{ENTER}")

#SPL
browser.text_field(:id => 'gs_Spl').set("undefined")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[8]').text.include? "undefined"
print "Filter by SPL - Passed", "\n"
else
print "Filter by SPL - Failed", "\n"
end
browser.text_field(:id => 'gs_Spl').set("")
browser.send_keys("{ENTER}")

#Utility Code
browser.select_list(:id => 'gs_UtilityCode').option(:value, '27').select
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[9]').text.include? "27"
print "Filter by Utility Code - Passed", "\n"
else
print "Filter by Utility Code - Failed", "\n"
end
browser.select_list(:id => 'gs_UtilityCode').option(:value, '').select

#Partner Code
browser.text_field(:id => 'gs_PartnerCode').set("STD")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]').text.include? "STD"
print "Filter by Partner Code - Passed", "\n"
else
print "Filter by Partner Code - Failed", "\n"
end
browser.text_field(:id => 'gs_PartnerCode').set("")
browser.send_keys("{ENTER}")

#Utility Billing City
browser.text_field(:id => 'gs_UtilityBillingCity').set("NEW YORK")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[14]').text.include? "NEW YORK"
print "Filter by Utility Billing City - Passed", "\n"
else
print "Filter by Utility Billing City - Failed", "\n"
end
browser.text_field(:id => 'gs_UtilityBillingCity').set("")
browser.send_keys("{ENTER}")

#Utility Billing State
browser.text_field(:id => 'gs_UtilityBillingSt').set("PA")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[15]').text.include? "PA"
print "Filter by Utility Billing State - Passed", "\n"
else
print "Filter by Utility Billing State - Failed", "\n"
end
browser.text_field(:id => 'gs_UtilityBillingSt').set("")
browser.send_keys("{ENTER}")

browser.close