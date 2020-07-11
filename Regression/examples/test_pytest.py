from __future__ import print_function
import pytest
from selenium import webdriver

try:
    driver = webdriver.PhantomJS()
    driver.implicitly_wait(5)
    driver.set_window_size(1120, 550)
except:
    driver = webdriver.Firefox()

data_array = ['foo', 'bar']


@pytest.fixture(scope='module')
def resource_a_setup(request):
    print('\nresources_a_setup()')

    def resource_a_teardown():
        print('\nresources_a_teardown()')
        if driver:
            print(driver.current_url)
            driver.close()

    request.addfinalizer(resource_a_teardown)


def test_1_that_needs_resource_a(resource_a_setup):
    print('test_1_that_needs_resource_a()')


def test_2_that_does_not():
    print('\ntest_2_that_does_not()')


@pytest.mark.parametrize('stuff', data_array)
def test_3_that_does(resource_a_setup, stuff):
    print('\ntest_3_that_does()', stuff)

    # driver = resource_a_setup()
    driver.get('http://google.com/?{}'.format(stuff))
    print("got url ", driver.current_url)
