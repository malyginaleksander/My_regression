###This is NRG's Regression Test Suite for the Web Application Stack.


Quick Instructions
------------------
* Install Firefox.  It may not work but it's the default browser for testing (see below)

* Create a python 3.4 virtual environment

    `mkvirtualenv Regression`

* Install dependencies

    `pip install -r requirements.txt`

* Setup python path for pointing to your homedir 

	`export PYTHONPATH=~/GitHub/Regression/Regression`
	
* Change dir to Regression subdir
  `cd ~/GitHub/Regression/Regression`
	
* Run the Tests


	
    `py.test .  -- to run the tests with succinct output`
    `py.test . -s -vv  -- to run the tests with verbose output`
    `py.test . --html=report.html  --junit-xml=regression.junit.xml -s -vv  -- to run the tests with output reports and verbose output`


Browser selection
-----------------
* the tests default to the Selenium Firefox driver.  as of 2016-09-29, this is working fairly well on Windows, but for Mikey at least even with up-to-date Firefox and selenium library version it won't connect.
* Jenkins uses phantomjs, so you can use phantomjs locally
	* `npm install -g phantomjs`  (or other ways for phantom to be installed, cf <link tbd>)
	* export USE_PHANTOM=use_phantom
	* run tests as above


We are still waiting on a successful reference automated run.  Not all tests are executable from the jenkins CI server due to network or unknown restrictions.


n.b.  for mikey, the full test suite takes a very long time (>1hr) and does not pass using phantomjs:

```
(regression) gmnygrios-l1:Regression mreppy.lh$ py.test -s -vv
================================================= test session starts ==================================================
platform darwin -- Python 3.4.3, pytest-2.9.2, py-1.4.31, pluggy-0.3.1 -- /Users/mreppy.lh/.virtualenvs/regression/bin/python3.4
cachedir: .cache
rootdir: /Users/mreppy.lh/Dropbox/mikeyshare/Regression, inifile:
plugins: html-1.10.0
collected 390 items

EP_Web/Enrollments/Choice_Page/test_Choice.py::test_state[tc-01] driver_setup()
making PhantomJS driver
tc-01 EP Web Page Choice Page Enrollment -  Massachusetts  -  National Grid
Confirmation =  fbacf17
PASSED

<... tons of output>

        elem = driver.find_element_by_link_text("FAQs").click()
        time.sleep(5)

>       assert payload.header in driver.page_source
E       assert 'XVIII. NRG Home Football Fan Plans' in '<!DOCTYPE html><html><head>\n\t\t<meta charset="UTF-8">\n\t\t<meta http-equiv="X-UA-Compatible" content="IE=Edge">\n\...end main content row!-->\n\n</div>\n    <div style="color:#AAA;float:right">\n\t10.200.178.116</div>\n\n</body></html>'
E        +  where 'XVIII. NRG Home Football Fan Plans' = payload(tc='tc-12', header='XVIII. NRG Home Football Fan Plans').header
E        +  and   '<!DOCTYPE html><html><head>\n\t\t<meta charset="UTF-8">\n\t\t<meta http-equiv="X-UA-Compatible" content="IE=Edge">\n\...end main content row!-->\n\n</div>\n    <div style="color:#AAA;float:right">\n\t10.200.178.116</div>\n\n</body></html>' = <selenium.webdriver.phantomjs.webdriver.WebDriver (session="74f37100-866c-11e6-b2f8-b9021bee3039")>.page_source

Inbound/FAQ/Regression/test_FAQ_NRG_SOP_Regression.py:90: AssertionError
======================================= 18 failed, 372 passed in 4038.31 seconds =======================================
(regression) gmnygrios-l1:Regression mreppy.lh$
```
