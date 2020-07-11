require 'rubygems'
require 'watir-webdriver'
require "win32ole"
require 'csv'

browser = Watir::Browser.new :firefox
browser.goto 'http://www.pt.energypluscompany.com/myinbound/login.php'

if
browser.text.include? "There is a problem with this website's security certificate."
browser.link(:text => 'Continue to this website (not recommended).').click
end

#login
browser.text_field(:name => 'email').set ('mpeters@energypluscompany.com')
browser.text_field(:name => 'password').set ('energy')
browser.button(:value => ' Login').click

if
browser.text.include? "Start a manual call"
browser.link(:text => 'Start a manual call').click
browser.text_field(:id => 'phoneNumber').set("2154935444")
browser.text_field(:id => 'reason').set("this is a test")
browser.select_list(:id => 'brand_id').select("Green Mountain Energy")
browser.button(:value => 'Start Call').click_no_wait
browser.javascript_dialog.button('OK').click
sleep 2
else

browser.radio(:id => 'brandId_5').visible?
browser.radio(:id => 'brandId_5').click
browser.button(:id => 'btn_continue').click
end
sleep 2

browser.button(:id => 'log-dispo').click
sleep 2

browser.select_list(:id => 'dispo-list').select "500 : Do Not Solicit"
sleep 2

browser.text_field(:name => 'First Name').set("GM")
browser.text_field(:name => 'Last Name').set("dns")
browser.text_field(:name => 'Address 1').set("123 main st")
browser.text_field(:name => 'City').set("fairless hills")
browser.select_list(:name => 'State').select("Pennsylvania")
browser.text_field(:name => 'Zip').set("19030")
browser.text_field(:name => 'Email').set("test@test.com")
browser.text_field(:name => 'Area Code').set("234")
browser.text_field(:name => 'Prefix').set("342")
browser.text_field(:name => 'Line Number').set("4342")
browser.select_list(:name => 'Reason').select("Addressee no longer resides at address")
browser.text_field(:name => 'Notes').set("testin")
browser.button(:id => 'dispo-end-call').click

browser.close