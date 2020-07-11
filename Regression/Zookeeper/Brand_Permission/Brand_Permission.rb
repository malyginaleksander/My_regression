require 'rubygems'
require 'watir-webdriver'
require 'win32ole' 
require 'csv'

#Zookeeper Clear Brand
browser = Watir::Browser.new :firefox
browser.goto "http://www.pt.energypluscompany.com/newadmin/login.php"

browser.text_field(:name => 'loginusername').set("mpeters")
browser.text_field(:name => 'loginpassword').set("energy")
browser.button(:value => 'Login').click
sleep 2

browser.link(:xpath => '/html/body/div[4]/div[4]/div[2]/ul/li[4]/a').click
sleep 5
browser.text_field(:id => 'prependedInput').set("michael peters")
browser.table.tr(:id => '374').click
sleep 2
browser.checkbox(:name => 'brand_permissions_green_mountain_energy').clear
browser.button(:value,"Save Operator").click
sleep 2
browser.close

#Inbound Check Brand
browser = Watir::Browser.new :firefox

browser.goto 'http://www.pt.energypluscompany.com/myinbound/login.php'

#login
browser.text_field(:name => 'email').set ('mpeters@energypluscompany.com')
browser.text_field(:name => 'password').set ('energy')
browser.button(:value => ' Login').click
sleep 4

if
browser.radio(:id => 'brandId_5').exists?
print "Brand Permission - Failed", "\n"
else 
print "Brand Permission - Passed", "\n"
end
browser.close

#Zookeeper set Brand
browser = Watir::Browser.new :firefox
browser.goto "http://www.pt.energypluscompany.com/newadmin/login.php"

browser.text_field(:name => 'loginusername').set("mpeters")
browser.text_field(:name => 'loginpassword').set("energy")
browser.button(:value => 'Login').click
sleep 2

browser.link(:xpath => '/html/body/div[4]/div[4]/div[2]/ul/li[4]/a').click
sleep 5
browser.text_field(:id => 'prependedInput').set("michael peters")
browser.table.tr(:id => '374').click
sleep 2
browser.checkbox(:name => 'brand_permissions_green_mountain_energy').set
browser.button(:value,"Save Operator").click
sleep 2
browser.close
