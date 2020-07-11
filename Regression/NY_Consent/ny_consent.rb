#Remove All instances of Current Page from spreadsheet
require 'rubygems'
require 'watir-webdriver'
require "win32ole"


browser = Watir::Browser.new :firefox
browser.goto 'www.pt.energypluscompany.com/specialoffer'

#TC 1 - bad code
browser.text_field(:name => 'customer_code').set("bVgo2dxxx")
browser.button(:class => 'btn').click

if 
browser.div(:class => 'alert').exists?
print "TC 1 - Bad promo code - Passed", "\n"
else
print "TC 1 - Bad promo code - Failed", "\n"
end

#TC 2 - already given consent
browser.text_field(:name => 'customer_code').set("ny-y33kvv")
browser.button(:class => 'btn').click

if
browser.h1(:text => 'Thank you for signing up!').exists?
print "TC 2 - Already confirmed - Passed", "\n"
else
print "TC 2 - Already confirmed - Failed", "\n"
end

#TC 3 - give consent - validations
browser.goto 'www.pt.energypluscompany.com/specialoffer'

browser.text_field(:name => 'customer_code').set("ny-mwjzn7")
browser.button(:class => 'btn').click

browser.text_field(:id => 'email').set("")
browser.checkbox(:id => 'disclosure').set
browser.button(:value => 'Submit').click

if
browser.h1(:text => 'Thank you for signing up!').exists?
print "TC 3.1 - Need email - Failed", "\n"
else
print "TC 3.1 - Need email - Passed", "\n"
end
sleep 2

browser.text_field(:id => 'email').set("mpeters@energypluscompany.com")
browser.checkbox(:id => 'disclosure').clear
browser.button(:value => 'Submit').click

if
browser.h1(:text => 'Thank you for signing up!').exists?
print "TC 3.2 - Checkbox - Failed", "\n"
else
print "TC 3.2 - Checkbox - Passed", "\n"
end

browser.close