require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/awards'
Watir::Waiter::wait_until {browser.button(:id => 'awardsSearchButton').exists?}
browser.button(:id => 'awardsSearchButton').click
Watir::Waiter::wait_until {browser.div(:id => 'gbox_awardsGrid').exists?}
sleep 5

#Sort All Data
#Partner Code
browser.div(:id => 'jqgh_awardsGrid_PartnerCode').click
sleep 5
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "AAL"
print "Sort by Partner Code ASC - Passed", "\n"
else
print "Sort by Partner Code ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_awardsGrid_PartnerCode').click
sleep 5
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "USA"
print "Sort by Partner Code DESC - Passed", "\n"
else
print "Sort by Partner Code DESC - Failed", "\n"
end
sleep 5

#Promo Code
browser.div(:id => 'jqgh_awardsGrid_PromoCode').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "001"
print "Sort by Promo Code ASC - Passed", "\n"
else
print "Sort by Promo Code ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_awardsGrid_PromoCode').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "021"
print "Sort by Promo Code DESC - Passed", "\n"
else
print "Sort by Promo Code DESC - Failed", "\n"
end

#Benfit
browser.div(:id => 'jqgh_awardsGrid_TypeofBenefit').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]').text.include? "CASH"
print "Sort by Benfit ASC - Passed", "\n"
else
print "Sort by Benfit ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_awardsGrid_TypeofBenefit').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]').text.include? "REWARD"
print "Sort by Benfit DESC - Passed", "\n"
else
print "Sort by Benfit DESC - Failed", "\n"
end

#Status
browser.div(:id => 'jqgh_awardsGrid_Status').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[24]').text.include? "ACCEPT"
print "Sort by Status ASC - Passed", "\n"
else
print "Sort by Status ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_awardsGrid_Status').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[24]').text.include? "VOID"
print "Sort by Status DESC - Passed", "\n"
else
print "Sort by Status DESC - Failed", "\n"
end

#Filter
wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Awards')
sleep 5

#Ben ID
browser.text_field(:id => 'gs_Id').set("11040")
browser.text_field(:id => 'gs_Id').set("")
browser.text_field(:id => 'gs_Id').set("11040")
browser.send_keys("{ENTER}") 
sleep 20
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td').text.include? "11040"
print "Filter by BEN ID - Passed", "\n"
else
print "Filter by BEN ID - Failed", "\n"
end
browser.text_field(:id => 'gs_Id').set("")

#Trans Date
browser.text_field(:id => 'gs_TransDate').set("01/10/2008")
browser.send_keys("{ENTER}")
sleep 2
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "01/10/2008"
print "Filter by Trans Date - Passed", "\n"
else
print "Filter by Trans Date - Failed", "\n"
end
browser.text_field(:id => 'gs_TransDate').set("")

#Utility Account
browser.text_field(:id => 'gs_Acct').set("211577342500164")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "211577342500164"
print "Filter by Utility Account - Passed", "\n"
else
print "Filter by Utility Account - Failed", "\n"
end
browser.text_field(:id => 'gs_Acct').set("")

#Account
browser.text_field(:id => 'gs_AccountId').set("5166")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "5166"
print "Filter by Account - Passed", "\n"
else
print "Filter by Account - Failed", "\n"
end
browser.text_field(:id => 'gs_AccountId').set("")

#Partner
browser.text_field(:id => 'gs_PartnerCode').set("USA")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "USA"
print "Filter by Partner - Passed", "\n"
else
print "Filter by Partner - Failed", "\n"
end
browser.text_field(:id => 'gs_PartnerCode').set("")

#Promo
browser.text_field(:id => 'gs_PromoCode').set("004")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "004"
print "Filter by Promo - Passed", "\n"
else
print "Filter by Promo - Failed", "\n"
end
browser.text_field(:id => 'gs_PromoCode').set("")

#Member Number
browser.text_field(:id => 'gs_MemNum').set("DF896628")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[8]').text.include? "DF896628"
print "Filter by Member Number - Passed", "\n"
else
print "Filter by Member Number - Failed", "\n"
end
browser.text_field(:id => 'gs_MemNum').set("")

#Partner Indicator
browser.text_field(:id => 'gs_PartnerIndicator').set("MTH")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[9]').text.include? "MTH"
print "Filter by Partner Indicator - Passed", "\n"
else
print "Filter by Partner Indicator - Failed", "\n"
end
browser.text_field(:id => 'gs_PartnerIndicator').set("")

#Benefit
browser.text_field(:id => 'gs_TypeofBenefit').set("DISCOUNT")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[10]').text.include? "DISCOUNT"
print "Filter by Benefit - Passed", "\n"
else
print "Filter by Benefit - Failed", "\n"
end
browser.text_field(:id => 'gs_TypeofBenefit').set("")

#Award
browser.text_field(:id => 'gs_Award').set("CHANGE RATE CLASS")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[11]').text.include? "CHANGE RATE CLASS"
print "Filter by Award - Passed", "\n"
else
print "Filter by Award - Failed", "\n"
end
browser.text_field(:id => 'gs_Award').set("")

#Cash
browser.text_field(:id => 'gs_BenefitCash').set("50")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[12]').text.include? "50.00"
print "Filter by Cash - Passed", "\n"
else
print "Filter by Cash - Failed", "\n"
end
browser.text_field(:id => 'gs_BenefitCash').set("")

#Miles
browser.text_field(:id => 'gs_BenefitMiles').set("99")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[13]').text.include? "99"
print "Filter by Miles - Passed", "\n"
else
print "Filter by Miles - Failed", "\n"
end
browser.text_field(:id => 'gs_BenefitMiles').set("")

#Invoice
browser.text_field(:id => 'gs_InvoiceNumber').set("0016538735")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[14]').text.include? "0016538735"
print "Filter by Invoice - Passed", "\n"
else
print "Filter by Invoice - Failed", "\n"
end
browser.text_field(:id => 'gs_InvoiceNumber').set("")

#Invoice Total
browser.text_field(:id => 'gs_InvoiceTotal').set("49.21")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[15]').text.include? "49.21"
print "Filter by Invoice Total - Passed", "\n"
else
print "Filter by Invoice Total - Failed", "\n"
end
browser.text_field(:id => 'gs_InvoiceTotal').set("")

#Invoice Date
browser.text_field(:id => 'gs_InvoiceDate').set("01/09/2008")
browser.send_keys("{ENTER}")
sleep 2
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[16]').text.include? "01/09/2008"
print "Filter by Invoice Date - Passed", "\n"
else
print "Filter by Invoice Date - Failed", "\n"
end
browser.text_field(:id => 'gs_InvoiceDate').set("")

#Bill Cycle
browser.text_field(:id => 'gs_TriggerBC').set("2")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[17]').text.include? "2"
print "Filter by Bill Cycle - Passed", "\n"
else
print "Filter by Bill Cycle - Failed", "\n"
end
browser.text_field(:id => 'gs_TriggerBC').set("")

#Send Date
browser.text_field(:id => 'gs_SendDate').set("07/08/2008")
browser.send_keys("{ENTER}")
sleep 2
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[18]').text.include? "07/08/2008"
print "Filter by Send Date - Passed", "\n"
else
print "Filter by Send Date - Failed", "\n"
end
browser.text_field(:id => 'gs_SendDate').set("")

#Send File
browser.text_field(:id => 'gs_SendFileName').set("Awards_DISCOUNT 20080611-1819.xls")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[19]').text.include? "Awards_DISCOUNT 20080611-1819.xls"
print "Filter by Send File - Passed", "\n"
else
print "Filter by Send File - Failed", "\n"
end
browser.text_field(:id => 'gs_SendFileName').set("")

#Reply Date
browser.text_field(:id => 'gs_ReplyDate').set("03/01/2010")
browser.send_keys("{ENTER}")
sleep 2
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[20]').text.include? "03/01/2010"
print "Filter by Reply Date - Passed", "\n"
else
print "Filter by Reply Date - Failed", "\n"
end
browser.text_field(:id => 'gs_ReplyDate').set("")

#Reply File
browser.text_field(:id => 'gs_ReplyFileName').set("handback_20090630.txt")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[21]').text.include? "handback_20090630.txt"
print "Filter by Reply File - Passed", "\n"
else
print "Filter by Reply File - Failed", "\n"
end
browser.text_field(:id => 'gs_ReplyFileName').set("")

#Reply Status
browser.text_field(:id => 'gs_ReplyStatus').set("0000")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[22]').text.include? "0000"
print "Filter by Reply Status - Passed", "\n"
else
print "Filter by Reply Status - Failed", "\n"
end
browser.text_field(:id => 'gs_ReplyStatus').set("")

#Reply Info
browser.text_field(:id => 'gs_ReplyExtraInfo').set("Credited for the first 2 invoices already")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[23]').text.include? "Credited for the first 2 invoices already"
print "Filter by Reply Info - Passed", "\n"
else
print "Filter by Reply Info - Failed", "\n"
end
browser.text_field(:id => 'gs_ReplyExtraInfo').set("")

#Status
browser.select_list(:id => 'gs_Status').fire_event 'onclick'
browser.select_list(:id => 'gs_Status').select("VOID")
browser.select_list(:id => 'gs_Status').fire_event 'onclick'
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[24]').text.include? "VOID"
print "Filter by Status - Passed", "\n"
else
print "Filter by Status - Failed", "\n"
end
browser.select_list(:id => 'gs_Status').fire_event 'onclick'
browser.select_list(:id => 'gs_Status').select("All")
browser.select_list(:id => 'gs_Status').fire_event 'onclick'

#Notes
browser.text_field(:id => 'gs_Notes').set("Invoice canceled")
browser.send_keys("{ENTER}") 
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[25]').text.include? "Invoice canceled"
print "Filter by Notes - Passed", "\n"
else
print "Filter by Notes - Failed", "\n"
end
browser.text_field(:id => 'gs_Notes').set("")

#Date Added
browser.text_field(:id => 'gs_DateAdded').set("01/17/2009")
browser.send_keys("{ENTER}")
sleep 2
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[26]').text.include? "01/17/2009"
print "Filter by Date Added - Passed", "\n"
else
print "Filter by Date Added - Failed", "\n"
end
browser.text_field(:id => 'gs_DateAdded').set("")

browser.close
