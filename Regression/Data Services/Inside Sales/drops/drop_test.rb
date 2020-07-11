##############################################################
#need admin - manage employee roles - drop admin permissions
#update xls with UAN and Customer Names
##############################################################

require 'rubygems'
require 'watir'
require 'win32ole'


browser = Watir::Browser.new

browser.goto 'http://ep-qa/Admin/UserAndRoleAdmin.aspx?type=feature'
Watir::Waiter::wait_until {browser.select_list(:id => 'ctl00_MainContent_ctl00_ddlFeatures').exists?}
browser.link(:id => 'ctl00_ucTabNavigation_hlManageEmployeeRoles').click
browser.select_list(:id => 'ctl00_MainContent_ctl00_ddlRoles').select("SaveRep")
browser.button(:value => 'P' ).click
sleep 5

browser.li(:text => 'Peters, Michael (mpeters)').drag_and_drop_on(browser.div(:id => 'drop1'))





