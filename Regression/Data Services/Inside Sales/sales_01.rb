require 'rubygems'
require 'watir'
require 'win32ole'

browser = Watir::Browser.new
browser.goto 'http://epinsl-qa/InsideSales/ViewSaves.html'
browser.link(:text => 'RUN').click
sleep 5

#check data returns
Watir::Waiter::wait_until {browser.div(:id => 'divDetails').visible?}
if
browser.div(:id => 'divDetails').exists?
print "Records Returned"
else 
print "Search Failed"
end
sleep 5

# View Saves search by Agent, Electric, State = PA, Utility = DUQ
browser.select_list(:id => 'ddlSaveReps').select("LaTonya Andrews")
browser.text_field(:id => 'startDT').set("01/01/2013")
browser.text_field(:id => 'endDT').set("12/13/2013")
browser.select_list(:id => 'ddlCommodity').select("Electric")
browser.select_list(:id => 'ddlDropType').select("Utility")
browser.select_list(:id => 'ddlServiceStates').select("PA")
browser.select_list(:id => 'ddlUtilities').select("Duquesne")
browser.link(:text => 'RUN').click
sleep 5

if 
browser.text.include? "8000390156004"
print "Search Passes", "\n"
else
print "Search Failed", "\n"
end

begin
# select account number
browser.text(:text => '8000390156004').click
browser = Watir::Browser.attach(:title, 'Member Form - VOIT SYLVESTER E').close
