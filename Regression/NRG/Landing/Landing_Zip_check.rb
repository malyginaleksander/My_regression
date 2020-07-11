require 'rubygems'
require 'watir-webdriver'
require 'win32ole' 
require 'csv'

browser = Watir::Browser.new :firefox
browser.goto 'http://enroll.pt.nrghomepower.com/combined/cashbackres/il/'

browser.text_field(:name => 'template_variable_zipcode').set("19030")
browser.button(:value => 'See Plans').click
sleep 3

if
browser.table(:id => 'productchartaddress').exists?
print "pass", "\n"
else
print "failed", "\n"
end

sleep 1

browser.text_field(:name => 'template_variable_zipcode').set("90210")
browser.button(:value => 'See Plans').click
sleep 3

if
browser.div(:class => 'alert alert-danger').exists?
print "pass"
else
print "failed"
end

browser.close