# Pricing UI Automated Regression Tests

## Requirements:
* Install requirements.txt with ```pip install -r requirments.txt```. 
  The versions listed are not critical, if newer versions are required it should 
  not cause any errors 

* These tests rely on the password_manager module found in
  ```Regression\Regression\ECC\TestUtilities\UtilitySupportModules```
  If the tests scripts are moved, edit the reference to the support modules in conftest.py
 
 ## Setup
 * Run setup_credentials.py from the command line one time before executing tests. It will prompt
   you to enter credentials.
 * Create a file called Chromedriver_path.cfg and enter the path to Chromedriver,
   ex: ```C:/Users/drivers/chromedriver.exe```
 
 ## Running tests
 * Navigate into the test_cases folder and call ```pytest``` to execute all tests, or pass the name of a given test file 
   to pytest
 * Call ```pytest -h``` to get a list of optional arguments
 * Pytest will report how many tests it collects and how many pass at the end of the report.
   If any tests fail, their errors will be displayed. A successful test run will simply list:
   *x passed in y seconds* where *x* is equal to the number of tests collected at the start
   