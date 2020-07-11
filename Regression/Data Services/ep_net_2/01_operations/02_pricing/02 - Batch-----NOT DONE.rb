require 'rubygems'
require 'watir'
require "win32ole"

browser = Watir::Browser.new
browser.goto 'http://epweb-pt/Pricing#batch'
wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('Pricing Home Page')
sleep 5

Watir::Waiter::wait_until {browser.div(:id => 'batch').exists?}
sleep 2

#Select Price Batch and Date from Dropdown
########### Update Section before Test Run ################
#browser.select_list(:id => 'priceBatchSelector').select("1114")
browser.text_field(:id => 'specificMeterReadDate').set("09/11/2012")
browser.send_keys("{ENTER}")
browser.send_keys("{ENTER}")
browser.button(:value => 'Run Batch').click

