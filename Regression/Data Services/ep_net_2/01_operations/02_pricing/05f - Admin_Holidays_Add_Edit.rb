require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Holidays")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}
if
browser.div(:id => 'gbox_pricingAdminGrid').exists?
print "Results populating on page - Passed", "\n"
else
print "Results populating on page - Failed", "\n"
end

#Add and Verify Record
browser.span(:class => 'ui-icon ui-icon-plus').click
browser.text_field(:id => 'Holiday').set("06/14/2010")
browser.text_field(:id => 'HolidayDescription').set("Flag Day2")
sleep 2
browser.span(:class => 'ui-icon ui-icon-disk').click
sleep 2
browser.span(:class => 'ui-icon ui-icon-closethick').click
browser.close

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Holidays")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_HolidayDescription').set("Flag Day2")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_HolidayDescription').set("")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_HolidayDescription').set("Flag Day2")
browser.send_keys("{ENTER}")

sleep 5
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "Flag Day"
print "Add and Verify Record - Passed", "\n"
else
print "Add and Verify Record - Failed", "\n"
end
browser.text_field(:id => 'gs_HolidayDescription').set("")
browser.close

#Edit Record
browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Holidays")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

browser.text_field(:id => 'gs_Holiday').set("01/01/2010")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_Holiday').set("")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_Holiday').set("01/01/2010")
browser.send_keys("{ENTER}")
sleep 5
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').click
browser.span(:class => 'ui-icon ui-icon-pencil').click
browser.text_field(:id => 'HolidayDescription').set("New Year's Dayxxx")
browser.span(:class => 'ui-icon ui-icon-disk').click
browser.span(:class => 'ui-icon ui-icon-closethick').click
browser.close

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Holidays")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5
browser.text_field(:id => 'gs_Holiday').set("01/01/2010")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_Holiday').set("")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_Holiday').set("01/01/2010")
browser.send_keys("{ENTER}")
sleep 5

if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "New Year's Dayxxx"
print "Edit and Verify Record - Passed", "\n"
else
print "Edit and Verify Record - Failed", "\n"
end
sleep 2
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').click
browser.span(:class => 'ui-icon ui-icon-pencil').click
browser.text_field(:id => 'HolidayDescription').set("New Year's Day")
browser.span(:class => 'ui-icon ui-icon-disk').click
browser.span(:class => 'ui-icon ui-icon-closethick').click

browser.close
