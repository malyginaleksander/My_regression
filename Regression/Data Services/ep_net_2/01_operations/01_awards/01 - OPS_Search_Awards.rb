require 'rubygems'
require 'watir-webdriver'
require "win32ole"

browser = Watir::Browser.new :firefox
browser.goto 'http://epnet2.pt.nrgpl.us/awards'
Watir::Wait.until {browser.div(:class => 'ui-widget ui-helper-clearfix').exists?}

#All Search Criteria can be used to conduct searches
#Search by Account ID
browser.text_field(:id => 'AccountID').set("136")
browser.button(:id => 'awardsSearchButton').click
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "136"
print "Search by Account ID - Passed", "\n"
else
print "Search by Account ID - Failed", "\n"
end
browser.button(:id => 'awardsSeachClearButton').click
Watir::Wait.until {browser.text_field(:id => 'AccountID').text.include? ""}

#Search by Utility Account
browser.text_field(:id => 'Acct').set("9067494114")
browser.button(:id => 'awardsSearchButton').click
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "9067494114"
print "Search by Utility Account - Passed", "\n"
else
print "Search by Utility Account - Failed", "\n"
end
browser.button(:id => 'awardsSeachClearButton').click
Watir::Wait.until {browser.text_field(:id => 'Acct').text.include? ""}

#Search by Ben ID
browser.text_field(:id => 'Id').set("276099")
browser.button(:id => 'awardsSearchButton').click
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[1]').text.include? "276099"
print "Search by Ben ID - Passed", "\n"
else
print "Search by Ben ID - Failed", "\n"
end
browser.button(:id => 'awardsSeachClearButton').click
Watir::Wait.until {browser.text_field(:id => 'Id').text.include? ""}

#Search by Partner Code
browser.select_list(:id => 'PartnerCode').select("BRD")
browser.button(:id => 'awardsSearchButton').click
sleep 15
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "BRD"
print "Search by Partner Code - Passed", "\n"
else
print "Search by Partner Code - Failed", "\n"
end
browser.button(:id => 'awardsSeachClearButton').click
Watir::Wait.until {browser.select_list(:id => 'PartnerCode').text.include? ""}

#Search by Promo Code
browser.select_list(:id => 'PromoCode').select("100")
browser.button(:id => 'awardsSearchButton').click
sleep 15
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "100"
print "Search by Promo Code - Passed", "\n"
else
print "Search by Promo Code - Failed", "\n"
end
browser.button(:id => 'awardsSeachClearButton').click
Watir::Wait.until {browser.select_list(:id => 'PromoCode').text.include? ""}

#Search by Status
browser.select_list(:id => 'Status').select("PENDING")
browser.button(:id => 'awardsSearchButton').click
sleep 10
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[24]').text.include? "PENDING"
print "Search by Status - Passed", "\n"
else
print "Search by Status - Failed", "\n"
end
browser.button(:id => 'awardsSeachClearButton').click
Watir::Wait.until {browser.select_list(:id => 'Status').text.include? ""}

#Search by Account ID and Utility Account
browser.text_field(:id => 'AccountID').set("26707")
browser.text_field(:id => 'Acct').set("655714199000054")
browser.button(:id => 'awardsSearchButton').click
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "26707"
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "655714199000054"
print "Search by Account ID and Utility Account - Passed", "\n"
else
print "Search by Account ID and Utility Account - Failed", "\n"
end
end
browser.button(:id => 'awardsSeachClearButton').click
Watir::Wait.until {browser.text_field(:id => 'AccountID').text.include? ""}

#Search by Account ID and Ben ID
browser.text_field(:id => 'AccountID').set("24829")
browser.text_field(:id => 'Id').set("35")
browser.button(:id => 'awardsSearchButton').click
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "24829"
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[1]').text.include? "35"
print "Search by Account ID and Ben ID - Passed", "\n"
else
print "Search by Account ID and Ben ID - Failed", "\n"
end
end
browser.button(:id => 'awardsSeachClearButton').click
Watir::Wait.until {browser.text_field(:id => 'AccountID').text.include? ""}

#Search by Account ID and Partner Code
browser.text_field(:id => 'AccountID').set("30552")
browser.select_list(:id => 'PartnerCode').select("CON")
browser.button(:id => 'awardsSearchButton').click
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "30552"
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "CON"
print "Search by Account ID and Partner Code - Passed", "\n"
else
print "Search by Account ID and Partner Code - Failed", "\n"
end
end
browser.button(:id => 'awardsSeachClearButton').click
Watir::Wait.until {browser.text_field(:id => 'AccountID').text.include? ""}

#Search by Account ID and Promo Code
browser.text_field(:id => 'AccountID').set("6248")
browser.select_list(:id => 'PromoCode').select("015")
browser.button(:id => 'awardsSearchButton').click
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "6248"
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "015"
print "Search by Account ID and Promo Code - Passed", "\n"
else
print "Search by Account ID and Promo Code - Failed", "\n"
end
end
browser.button(:id => 'awardsSeachClearButton').click
Watir::Wait.until {browser.text_field(:id => 'AccountID').text.include? ""}

#Search by Account ID and Status
browser.text_field(:id => 'AccountID').set("38632")
browser.select_list(:id => 'Status').select("HOLD")
browser.button(:id => 'awardsSearchButton').click
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "38632"
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[24]').text.include? "HOLD"
print "Search by Account ID and Status - Passed", "\n"
else
print "Search by Account ID and Status - Failed", "\n"
end
end
browser.button(:id => 'awardsSeachClearButton').click
Watir::Wait.until {browser.text_field(:id => 'AccountID').text.include? ""}

#Search by ALL Criteria
browser.text_field(:id => 'AccountID').set("7472")
browser.text_field(:id => 'Acct').set("2781070006")
browser.text_field(:id => 'Id').set("3")
browser.select_list(:id => 'PartnerCode').select("BRD")
browser.select_list(:id => 'PromoCode').select("001")
browser.select_list(:id => 'Status').select("ACCEPT")
browser.button(:id => 'awardsSearchButton').click
sleep 2
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[4]').text.include? "7472"
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[3]').text.include? "2781070006"
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[1]').text.include? "3"
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[6]').text.include? "BRD"
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[7]').text.include? "001"
if
browser.table(:xpath => '/html/body/div/div[3]/div/div/div[3]/div[3]/div[3]/div/table/tbody/tr[2]/td[24]').text.include? "ACCEPT"
print "Search by ALL Criteria - Passed", "\n"
else
print "Search by ALL Criteria - Failed", "\n"
end
end
end
end
end
end

browser.button(:id => 'awardsSeachClearButton').click
Watir::Wait.until {browser.text_field(:id => 'AccountID').text.include? ""}

browser.close