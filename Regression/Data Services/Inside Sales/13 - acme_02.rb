require 'rubygems'
require 'watir-webdriver'
require 'win32ole'

browser = Watir::Browser.new :firefox
browser.goto 'http://acme.pt.nrgpl.us/'
if
browser.text_field(:id => 'username').exists?
browser.text_field(:id => 'username').set("acmeprodadminnrg")
browser.text_field(:id => 'password').set("Green123")
browser.button(:value => 'Log On').click
end
sleep 2

browser.goto 'http://acme.pt.nrgpl.us/#/genpop'
sleep 2
browser.select_list(:id => 'stateSelectBox').select("PA")
browser.button(:id => 'goButton').click
sleep 1
browser.div(:class => 'ngCellText ng-scope col11 colt11', :text => 'PA').click
browser.select_list(:id => 'campaignSelect').select("test")
browser.select_list(:id => 'agentSelect').select("Andrews, LaTonya")
browser.button(:text,"Assign To").click_no_wait
sleep 5

browser.goto 'http://acme.pt.nrgpl.us/#/addCampaign'
