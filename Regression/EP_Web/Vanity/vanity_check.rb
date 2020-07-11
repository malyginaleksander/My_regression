require 'rubygems'
require 'watir-webdriver'
require 'win32ole' 
require 'csv'

browser = Watir::Browser.new :firefox
browser.goto 'http://www.pt.energypluscompany.com/17save'

if
browser.text.include? 'Not Found'
print "Vanity Landing Page - Failed", "\n"
else
print "Vanity Landing Page - Passed", "\n"
end

browser.goto 'http://www.pt.energypluscompany.com/02402'
if
browser.text.include? 'Not Found'
print "Not Found - Passed", "\n"
else
print "Not Found - Failed", "\n"
end

browser.close