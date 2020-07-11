require 'rubygems'
require 'watir-webdriver'
require 'win32ole' 
require 'csv'

#EPWEB-2073

browser = Watir::Browser.new :firefox
browser.goto 'https://pt.energypluscompany.com/company/careers.php'

if
browser.url == 'https://careers.nrgenergy.com/'
print "Careers Page - Passed", "\n"
else
print "Careers Page - Failed", "\n"
end

browser.close