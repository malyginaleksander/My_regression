import sys
sys.path.insert(1, '../../UtilitySupportModules')
from password_manager import get_username_and_pw_and_setup_if_necessary

print("\nIf your credentials.cfg file is not present, you will be prompted to "
      "enter a username and password for django admin access:")
username, password = get_username_and_pw_and_setup_if_necessary('./credentials.cfg', 'django')
if username and password:
    print("Success: credentials stored")
