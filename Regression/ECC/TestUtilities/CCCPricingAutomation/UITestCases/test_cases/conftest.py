import pytest
from selenium import webdriver
import sys

# Add UtilitySupportModules to the import search path
sys.path.insert(0, '../../../UtilitySupportModules')
# Import the module after the search path is altered
from password_manager import get_username_and_pw_and_setup_if_necessary


@pytest.fixture(scope="session")
def setup(request):
    username, password = get_username_and_pw_and_setup_if_necessary('../credentials.cfg', 'django')
    print("initiating chrome driver")
    with open('../Chromedriver_path.cfg', 'r') as file:
        chromedriver_path = file.read().strip()
    driver = webdriver.Chrome(chromedriver_path)
    session = request.node
    for item in session.items:
        cls = item.getparent(pytest.Class)
        setattr(cls.obj, "driver", driver)
    url = 'https://ccc.pt.nrgpl.us/admin/'
    driver.get(url)
    driver.maximize_window()
    user_name_entry = driver.find_element_by_id('id_username')
    password_entry = driver.find_element_by_id('id_password')
    # No ID provided,Xpath used instead
    login_button = driver.find_element_by_xpath('//*[@id="login-form"]/div[3]/input')

    # Execute the login
    user_name_entry.send_keys(username)
    password_entry.send_keys(password)
    login_button.click()

    yield driver
    driver.quit()
