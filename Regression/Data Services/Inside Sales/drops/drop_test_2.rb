
require 'rubygems'
require 'watir'

class Action
  def initialize(action)
    @a = Action
  end
end

browser=Watir::Browser.new
browser.goto("http://devfiles.myopera.com/articles/735/example.html")

my_element=browser.li(:text,'Art Brut')
target=browser.ul(:id,'Rej').li(:text,'None')

my_element.fire_event("onmousedown")

driver=browser.driver
driver.action.click_and_hold(my_element.wd).perform

sleep 2
driver.action.move_to(target.wd).perform

sleep 2
target.fire_event("onmouseup")



=begin
<MyElement>
    <Data1>123</Data1>
    <Data2>234</Data2>
</MyElement>

my_element=browser.li(:text,'Art Brut')
target=browser.ul(:id,'Rej').li(:text,'None')
my_element.fire_event("onmousedown")
driver=browser.driver
driver.action.click_and_hold(my_element.wd).perform
sleep 2
driver.action.move_to(target.wd).perform
sleep 2
target.fire_event("onmouseup")
=end