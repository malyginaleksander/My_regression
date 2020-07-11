require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/awards#reconciliation'
sleep 2
browser.select_list(:id => 'awardsReconciliationPartnerCodeComboBox').select("BBY - Best Buy")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_milesListingGrid').exists?}
sleep 5

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Awards')
sleep 5

#Records are editable and saved
browser.text_field(:id => 'gs_Miles').set("35000")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_Miles').set("")
browser.text_field(:id => 'gs_Miles').set("35000")
browser.send_keys("{ENTER}") 
browser.send_keys("{ENTER}") 
sleep 2
Watir::Waiter::wait_until {browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "35000"}
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').click
browser.span(:class => 'ui-icon ui-icon-pencil').click
browser.text_field(:id => 'Notes').set("this is a test")
browser.span(:class => 'ui-icon ui-icon-disk').click
browser.span(:class => 'ui-icon ui-icon-closethick').click
browser.select_list(:id => 'awardsReconciliationPartnerCodeComboBox').select("AAL - American Airlines")
sleep 5
browser.select_list(:id => 'awardsReconciliationPartnerCodeComboBox').select("BBY - Best Buy")
sleep 5
browser.text_field(:id => 'gs_Miles').set("35000")
browser.send_keys("{ENTER}")
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[3]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[16]').text.include? "this is a test"
print "Records are editable and saved - Passed", "\n"
else
print "Records are editable and saved - Failed", "\n"
end

browser.close