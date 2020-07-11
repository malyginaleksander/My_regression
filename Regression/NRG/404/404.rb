require 'rubygems'
require 'watir-webdriver'
require 'win32ole'
require 'watir-webdriver-performance'

browser = Watir::Browser.new :firefox
browser.goto "www.pt.nrghomepower.com/testblah/"
if
browser.text.include? "Not Found"
print "TC 1 passed", "\n" 
else
print "TC 1 failed", "\n" 
end
sleep 1
browser.goto "www.pt.nrghomepower.com/testblah"
if
browser.text.include? "Not Found"
print "TC 2 passed", "\n" 
else
print "TC 2 failed", "\n" 
end
sleep 1
browser.goto "www.pt.nrghomepower.com/testblah/test"
if
browser.text.include? "Not Found"
print "TC 3 passed", "\n" 
else
print "TC 3 failed", "\n" 
end
sleep 1
browser.goto "www.pt.nrghomepower.com/testblah/test/"
if
browser.text.include? "Not Found"
print "TC 4 passed", "\n" 
else
print "TC 4 failed", "\n" 
end
sleep 1
browser.close