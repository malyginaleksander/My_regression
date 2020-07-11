require 'rubygems'
require 'watir'
require 'win32ole'

browser = Watir::Browser.new
browser.goto 'http://epinsl-qa/InsideSales/MissingkWh.html'
browser.link(:text => 'RUN').click
sleep 5

# Missing KHW
Watir::Waiter::wait_until {browser.div(:id => 'divDetails').visible?}
if
browser.div(:id => 'divDetails').visible?
print "Records Returned", "\n"
else 
print "Search Failed", "\n"
end
sleep 10

# View Saves search by Agent, Electric, State = PA, Utility = DUQ
browser.select_list(:id => 'ddlSaveReps').select("Danielle Stauffer")
browser.text_field(:id => 'startDT').set("01/01/2013")
browser.text_field(:id => 'endDT').set("12/13/2013")
browser.select_list(:id => 'ddlCommodity').select("Electric")
browser.select_list(:id => 'ddlDropType').select("Utility")
browser.select_list(:id => 'ddlServiceStates').select("Pennsylvania")
browser.select_list(:id => 'ddlUtilities').select("PECO")
browser.link(:text => 'RUN').click


=begin
# select account number
browser.link(:text => '8000390156004').click
browser = Watir::Browser.attach(:title, 'Member Form - VOIT SYLVESTER E').close
=end

