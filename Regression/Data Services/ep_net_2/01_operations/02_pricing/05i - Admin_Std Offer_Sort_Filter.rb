require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/Pricing#admin'
sleep 2

#Results populating on page
browser.select_list(:id => 'pricingAdminComboBox').select("Std Off")
Watir::Waiter::wait_until {browser.div(:id => 'gbox_pricingAdminGrid').exists?}

if
browser.div(:id => 'gbox_pricingAdminGrid').exists?
print "Results populating on page - Passed", "\n"
else
print "Results populating on page - Failed", "\n"
end

#Sort
#Non Demand Adder
browser.div(:id => 'jqgh_pricingAdminGrid_NonDemandAdder').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "0.06500"
print "Sort by Non Demand Adder ASC - Passed", "\n"
else
print "Sort by Non Demand Adder ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_NonDemandAdder').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "0.07500"
print "Sort by Non Demand Adder DESC - Passed", "\n"
else
print "Sort by Non Demand Adder DESC - Failed", "\n"
end

#Effective Date
browser.div(:id => 'jqgh_pricingAdminGrid_EffectiveDate').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "10/02/2009"
print "Sort by Effective Date ASC - Passed", "\n"
else
print "Sort by Effective Date ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_EffectiveDate').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "01/13/2010"
print "Sort by Effective Date DESC - Passed", "\n"
else
print "Sort by Effective Date DESC - Failed", "\n"
end

#Demand Adder
browser.div(:id => 'jqgh_pricingAdminGrid_DemandAdder').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "0.04500"
print "Sort by Demand Adder ASC - Passed", "\n"
else
print "Sort by Demand Adder ASC - Failed", "\n"
end

browser.div(:id => 'jqgh_pricingAdminGrid_DemandAdder').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "0.07000"
print "Sort by Demand Adder DESC - Passed", "\n"
else
print "Sort by Demand Adder DESC - Failed", "\n"
end

#Filter
wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 8

#Demand Adder
browser.text_field(:id => 'gs_DemandAdder').set("0.055")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_DemandAdder').set("")
browser.send_keys("{ENTER}")
browser.text_field(:id => 'gs_DemandAdder').set("0.055")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[2]').text.include? "0.05500"
print "Filter by Demand Adder - Passed", "\n"
else
print "Filter by Demand Adder - Failed", "\n"
end
browser.text_field(:id => 'gs_DemandAdder').set("")
browser.send_keys("{ENTER}")

#Non Demand Adder
browser.text_field(:id => 'gs_NonDemandAdder').set("0.075")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "0.075"
print "Filter by Non Demand Adder - Passed", "\n"
else
print "Filter by Non Demand Adder - Failed", "\n"
end
browser.text_field(:id => 'gs_NonDemandAdder').set("")
browser.send_keys("{ENTER}")

#Effective Date
browser.text_field(:id => 'gs_EffectiveDate').set("10/02/2009")
browser.send_keys("{ENTER}")
browser.send_keys("{ENTER}")
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div[5]/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "10/02/2009"
print "Filter by Effective Date - Passed", "\n"
else
print "Filter by Effective Date - Failed", "\n"
end
browser.text_field(:id => 'gs_EffectiveDate').set("")
browser.send_keys("{ENTER}")

browser.close