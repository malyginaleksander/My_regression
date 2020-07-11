require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epnet2.pt.nrgpl.us/awards'
Watir::Waiter::wait_until {browser.button(:id => 'awardsSearchButton').exists?}
browser.button(:id => 'awardsSearchButton').click
Watir::Waiter::wait_until {browser.div(:id => 'gbox_awardsGrid').exists?}
sleep 5

#Paging on the Detail grid functions correctly
#Next Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-next').click
Watir::Waiter::wait_until {browser.text.include? "View 51 - 100"}
if
browser.text.include? "View 51 - 100"
print "Awards Next Page - Passed", "\n"
else
print "Awards Next Page - Failed", "\n"
end

#Previous Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-prev').click
Watir::Waiter::wait_until {browser.text.include? "View 1 - 50"}
if
browser.text.include? "View 1 - 50"
print "Awards Previous Page - Passed", "\n"
else
print "Awards Previous Page - Failed", "\n"
end

#Last Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-end').click
Watir::Waiter::wait_until {browser.text.include? "View 9 951"}
if
browser.text.include? "View 9 951"
print "Awards Last Page - Passed", "\n"
else
print "Awards Last Page - Failed", "\n"
end

#First Page
####### UPDATE PAGE NUMBERS)#######
browser.span(:class => 'ui-icon ui-icon-seek-first').click
Watir::Waiter::wait_until {browser.text.include? "View 1 - 50"}
if
browser.text.include? "View 1 - 50"
print "Awards First Page - Passed", "\n"
else
print "Awards First Page - Failed", "\n"
end
sleep 2

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Awards')
sleep 5

#Select Page
browser.text_field(:class => 'ui-pg-input').set("10")
browser.send_keys("{ENTER}")
browser.send_keys("{ENTER}")
Watir::Waiter::wait_until {browser.text.include? "View 451 - 500"}
if
browser.text.include? "View 451 - 500"
print "Awards Select Page - Passed", "\n"
else
print "Awards Select Page - Failed", "\n"
end
sleep 2

#Records are editable and saved
browser.text_field(:id => 'Id').set("4405")
browser.button(:id => 'awardsSearchButton').click
sleep 2
Watir::Waiter::wait_until {browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[1]').text.include? "4405"}
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td').click
browser.span(:class => 'ui-icon ui-icon-pencil').click
browser.text_field(:id => 'Notes').set("this is a test")
browser.span(:class => 'ui-icon ui-icon-disk').click
browser.span(:class => 'ui-icon ui-icon-closethick').click
browser.goto 'http://epnet2.pt.nrgpl.us/awards'
Watir::Waiter::wait_until {browser.button(:id => 'awardsSearchButton').exists?}
browser.button(:id => 'awardsSearchButton').click
Watir::Waiter::wait_until {browser.div(:id => 'gbox_awardsGrid').exists?}
sleep 5
browser.text_field(:id => 'Id').set("4405")
browser.button(:id => 'awardsSearchButton').click
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[25]').text.include? "this is a test"
print "Records are editable and saved - Passed", "\n"
else
print "Records are editable and saved - Failed", "\n"
end
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td').click
browser.span(:class => 'ui-icon ui-icon-pencil').click
browser.text_field(:id => 'Notes').set("")
browser.span(:class => 'ui-icon ui-icon-disk').click
browser.span(:class => 'ui-icon ui-icon-closethick').click

browser.close