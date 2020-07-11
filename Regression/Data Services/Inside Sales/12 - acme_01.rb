require 'rubygems'
require 'watir-webdriver'
require 'win32ole'

browser = Watir::Browser.new :firefox
browser.goto 'http://acme.pt.nrgpl.us/'
sleep 2
if
browser.text_field(:id => 'username').exists?
browser.text_field(:id => 'username').set("acmeprodadminnrg")#("acmeprodadminnrg")
browser.text_field(:id => 'password').set("Green123")#("Green123")
browser.button(:value => 'Log On').click
end

wsh = WIN32OLE.new('Wscript.Shell')
wsh.AppActivate('NRG Retail Campaign Management')


browser.goto 'http://acme.pt.nrgpl.us/#/addCampaign'
sleep 2
browser.text_field(:id => 'campaignName').set("test")
browser.text_field(:id => 'startDateText').set("07-28-2015")
browser.text_field(:id => 'endDateText').set("12-30-2015")
browser.button(:id => 'visualRuleEditButton').click
sleep 2
browser.select_list(:id => 'ruleSelectField').select("Account Name")
sleep 1
browser.select_list(:id => 'ruleSelectOperator').select("Contains")
browser.text_field(:id => 'ruleTextValue').set("davis")
sleep 1
browser.button(:id => 'ruleAddButton').click
sleep 1
browser.button(:id => 'ruleCalcButton').click
sleep 20
browser.button(:id => 'ruleSaveButton').click

sleep 2
browser.checkbox(:id => 'checkbox-1').set
sleep 2
browser.button(:id => 'saveCampaignButton').click

browser.close