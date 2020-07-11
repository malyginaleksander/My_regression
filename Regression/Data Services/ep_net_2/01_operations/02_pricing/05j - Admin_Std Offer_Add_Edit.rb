require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Std Off")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

#Add and Verify Record
browser.span(:class => 'ui-icon ui-icon-plus').click
browser.text_field(:id => 'DemandAdder').set("0.051")
browser.text_field(:id => 'NonDemandAdder').set("0.051")
browser.text_field(:id => 'EffectiveDate').set("11/03/2009")
sleep 2
browser.span(:class => 'ui-icon ui-icon-disk').click
sleep 2
browser.span(:class => 'ui-icon ui-icon-closethick').click
browser.close

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Std Off")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_DemandAdder').set("0.051")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_DemandAdder').set("")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_DemandAdder').set("0.051")
browser.send_keys("{ENTER}")

sleep 5
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "0.05100"
print "Add and Verify Record - Passed", "\n"
else
print "Add and Verify Record - Failed", "\n"
end
browser.text_field(:id => 'gs_DemandAdder').set("")
browser.close

#Edit Record
browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Std Off")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_DemandAdder').set("0.051")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_DemandAdder').set("")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_DemandAdder').set("0.051")
browser.send_keys("{ENTER}")
sleep 5
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').click
browser.span(:class => 'ui-icon ui-icon-pencil').click
browser.text_field(:id => 'DemandAdder').set("0.052")
browser.span(:class => 'ui-icon ui-icon-disk').click
browser.span(:class => 'ui-icon ui-icon-closethick').click
browser.close

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Std Off")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5
browser.text_field(:id => 'gs_DemandAdder').set("0.052")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_DemandAdder').set("")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_DemandAdder').set("0.052")
browser.send_keys("{ENTER}")
sleep 2

if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "0.052"
print "Edit and Verify Record - Passed", "\n"
else
print "Edit and Verify Record - Failed", "\n"
end
sleep 2
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').click
browser.span(:class => 'ui-icon ui-icon-pencil').click
browser.text_field(:id => 'DemandAdder').set("0.051")
browser.span(:class => 'ui-icon ui-icon-disk').click
browser.span(:class => 'ui-icon ui-icon-closethick').click

browser.close
