require 'rubygems'
require 'watir-webdriver'
require "win32ole"
require 'csv'
require "watir-webdriver/wait"

browser = Watir::Browser.new :firefox
browser.goto 'http://www.pt.energypluscompany.com/resetsession.php'
browser.goto 'http://www.pt.energypluscompany.com/myinbound/login.php'
if
browser.text.include? "Continue to this website (not recommended)."
browser.link(:text => 'Continue to this website (not recommended).').click
end

#login
browser.text_field(:name => 'email').set ('mpeters@energypluscompany.com')
browser.text_field(:name => 'password').set ('energy')
browser.button(:value => ' Login').click

excel= WIN32OLE::new("excel.Application")
workbook=excel.Workbooks.Open("C:\\Scripts\\INBOUND\\800_Enrollment\\800_Enrollment_data.xlsx")
worksheet = workbook.worksheets(2) 

#EP
rows = 2	#2
while    
rows <= 8	#8

state=worksheet.cells(rows,"A").value
customer_id=worksheet.cells(rows,"B").value
phone=worksheet.cells(rows,"C").value

browser.goto 'http://www.pt.energypluscompany.com/ajax/services/rdi/testcall.php'
browser.text_field(:id => 'customer_id').set customer_id 
browser.text_field(:id => 'source_phone').set phone
browser.button(:value => 'Submit - S4 way').click
sleep 4

if
browser.select_list(:name => 'state-list').selected? state
print "EP Brand - Passed", "\n"
else
print "EP Brand - Failed", "\n"
end

if
browser.text.include? "Thank you for calling Energy Plus"
print "EP State - Passed", "\n"
else
print "EP State - Failed", "\n"
end

rows=rows+1
end

#EP
rows = 9	#9
while    
rows <= 15	#15

state=worksheet.cells(rows,"A").value
customer_id=worksheet.cells(rows,"B").value
phone=worksheet.cells(rows,"C").value

browser.goto 'http://www.pt.energypluscompany.com/ajax/services/rdi/testcall.php'
browser.text_field(:id => 'customer_id').set customer_id 
browser.text_field(:id => 'source_phone').set phone
browser.button(:value => 'Submit - S4 way').click
sleep 4

if
browser.select_list(:name => 'state-list').selected? state
print "EP Phone and State - Passed", "\n"
else
print "EP Phone and State - Failed", "\n"
end

rows=rows+1
end

#Duquesne Standard Offer Program 
rows = 16		#16
while    
rows <= 16		#16

state=worksheet.cells(rows,"A").value
customer_id=worksheet.cells(rows,"B").value
phone=worksheet.cells(rows,"C").value

browser.goto 'http://www.pt.energypluscompany.com/ajax/services/rdi/testcall.php'
browser.text_field(:id => 'customer_id').set customer_id
browser.text_field(:id => 'source_phone').set phone
browser.button(:value => 'Submit - S4 way').click
sleep 2

Watir::Wait.until {browser.text.include? "Hello! My name is"}
if
#browser.text.include? "Did you start service with Duquesne yet?"
browser.button(:class => 'btn-danger').visible?
print "EP SOP - Passed", "\n"
else
print "EP SOP - Failed", "\n"
end

rows=rows+1
end


#NRG
rows = 17		#17
while    
rows <= 26		#26

state=worksheet.cells(rows,"A").value
customer_id=worksheet.cells(rows,"B").value
phone=worksheet.cells(rows,"C").value

browser.goto 'http://www.pt.energypluscompany.com/ajax/services/rdi/testcall.php'

browser.text_field(:id => 'customer_id').set customer_id
browser.text_field(:id => 'source_phone').set phone
browser.button(:value => 'Submit - S4 way').click
sleep 2

if
browser.select_list(:name => 'state-list').selected? state
print "NRG Phone and State - Passed", "\n"
else
print "NRG Phone and State - Failed", "\n"
end

if
browser.text.include? "Thank you for calling NRG Home"
print "NRG - Passed", "\n"
else
print "NRG - Failed", "\n"
end

rows=rows+1
end


#Duquesne Standard Offer Program 
rows = 27		#27
while    
rows <= 27		#27

state=worksheet.cells(rows,"A").value
customer_id=worksheet.cells(rows,"B").value
phone=worksheet.cells(rows,"C").value

browser.goto 'http://www.pt.energypluscompany.com/ajax/services/rdi/testcall.php'
browser.text_field(:id => 'customer_id').set customer_id
browser.text_field(:id => 'source_phone').set phone
browser.button(:value => 'Submit - S4 way').click
sleep 2

if
browser.button(:class => 'btn-danger').visible?
print "NRG SOP - Passed", "\n"
else
print "NRG SOP - Failed", "\n"
end

rows=rows+1
end


#Green Mountain
rows = 28	#28
while    
rows <= 29	#29

state=worksheet.cells(rows,"A").value
customer_id=worksheet.cells(rows,"B").value
phone=worksheet.cells(rows,"C").value

browser.goto 'http://www.pt.energypluscompany.com/ajax/services/rdi/testcall.php'
browser.text_field(:id => 'customer_id').set customer_id
browser.text_field(:id => 'source_phone').set phone
browser.button(:value => 'Submit - S4 way').click
sleep 2

if
browser.select_list(:name => 'state-list').selected? state
print "GME Phone and State - Passed", "\n"
else
print "GME Phone and State - Failed", "\n"
end

if
browser.text.include? "Thank you for calling Green Mountain Energy"
print "Green Mountain - Passed", "\n"
else
print "Green Mountain - Failed", "\n"
end

rows=rows+1
end


#GME
rows = 30	#30
while    
rows <= 40	#40

state=worksheet.cells(rows,"A").value
customer_id=worksheet.cells(rows,"B").value
phone=worksheet.cells(rows,"C").value

browser.goto 'http://www.pt.energypluscompany.com/ajax/services/rdi/testcall.php'
browser.text_field(:id => 'customer_id').set customer_id 
browser.text_field(:id => 'source_phone').set phone
browser.button(:value => 'Submit - S4 way').click
sleep 2
if
browser.select_list(:name => 'state-list').selected? state
print "GME Phone and State - Passed", "\n"
else
print "GME Phone and State - Failed", "\n"
end

rows=rows+1
end


#GM Duquesne Standard Offer Program 
rows = 41		#41
while    
rows <= 41		#41

state=worksheet.cells(rows,"A").value
customer_id=worksheet.cells(rows,"B").value
phone=worksheet.cells(rows,"C").value

browser.goto 'http://www.pt.energypluscompany.com/ajax/services/rdi/testcall.php'
browser.text_field(:id => 'customer_id').set customer_id
browser.text_field(:id => 'source_phone').set phone
browser.button(:value => 'Submit - S4 way').click
sleep 2

if
#browser.text.include? "Did you start service with Duquesne yet"
browser.button(:class => 'btn-danger').visible?
print "Green Mountain SOP - Passed", "\n"
else
print "Green Mountain SOP - Failed", "\n"
end

rows=rows+1
end


#Cirro
rows = 42	#42
while    
rows <= 42	#42

state=worksheet.cells(rows,"A").value
customer_id=worksheet.cells(rows,"B").value
phone=worksheet.cells(rows,"C").value

browser.goto 'http://www.pt.energypluscompany.com/ajax/services/rdi/testcall.php'
browser.text_field(:id => 'customer_id').set customer_id
browser.text_field(:id => 'source_phone').set phone
browser.button(:value => 'Submit - S4 way').click
sleep 2

if
browser.select_list(:name => 'state-list').selected? state
print "Cirro Phone and State - Passed", "\n"
else
print "Cirro Phone and State - Failed", "\n"
end

if
browser.text.include? "Thank you for calling Cirro"
print "Cirro - Passed", "\n"
else
print "Cirro - Failed", "\n"
end

rows=rows+1
end

$end
workbook.Save
workbook.Close

browser.close
