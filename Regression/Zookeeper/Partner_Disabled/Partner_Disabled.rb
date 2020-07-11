require 'rubygems'
require 'watir-webdriver'
require 'win32ole' 
require 'csv'

browser = Watir::Browser.new :firefox
browser.goto "http://www.pt.energypluscompany.com/newadmin/login.php"

browser.text_field(:name => 'loginusername').set("mpeters")
browser.text_field(:name => 'loginpassword').set("energy")
browser.button(:value => 'Login').click
sleep 2

browser.link(:xpath => '/html/body/div[4]/div[2]/div[2]/ul/li[2]/a').click
sleep 2
browser.button(:value => 'PA').click
sleep 2
browser.table.td(:id => 'pid_9440').click
sleep 2
browser.button(:value => 'Disabled').click
sleep 2

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Partners')
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :enter
sleep 5

browser.close

browser = Watir::Browser.new :firefox

browser.goto 'http://www.pt.energypluscompany.com/virginamerica/pa/'
if
browser.text.include? "The offer you are looking for is no longer available."
print "Offer Expired - Passed", "\n"
else 
print "Offer Expired - Failed", "\n"
end
sleep 2
browser.goto 'http://staging.devepc.com/combined/virginamerica/pa'
if
browser.text.include? "The offer you are looking for is no longer available."
print "Offer Expired - Passed"
else 
print "Offer Expired - Failed"
end

browser.close

browser = Watir::Browser.new :firefox
browser.goto "http://www.pt.energypluscompany.com/newadmin/login.php"

browser.text_field(:name => 'loginusername').set("mpeters")
browser.text_field(:name => 'loginpassword').set("energy")
browser.button(:value => 'Login').click
sleep 4

browser.link(:xpath => '/html/body/div[4]/div[2]/div[2]/ul/li[2]/a').click
sleep 5
browser.button(:value => 'PA').click
sleep 2
browser.table.td(:id => 'pid_9440').click
sleep 2
browser.button(:value => 'Active').click
sleep 5

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Partners')
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :tab
browser.send_keys :enter
sleep 1

browser.close