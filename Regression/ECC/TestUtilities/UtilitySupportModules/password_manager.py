import keyring
import os
from random_word import RandomWords
import configparser

# possible fix:
# 32-bit XP doesn't have Windows Vault. Use an alternative like Win Crypto.
# from keyring.alt.Windows import EncryptedKeyring
# keyring.set_keyring()
# You will need to set the backend file_path member too.


def get_username_and_pw_and_setup_if_necessary(full_file_name_with_location, target_website, ini=False):
    """ This function will read or initialize simple config textfile for storing credentials to webpages. It can also read
    from ".ini" textfile with python's configparser modules if an additional argument specifying sub section of the file is
    passed to it """

    if ini:
        config = configparser.ConfigParser()
        config.read(full_file_name_with_location)
        my_service_id = config[target_website]['username']
        faux_username = config[target_website]['password']
    elif os.path.isfile(full_file_name_with_location):
        service_file = open(full_file_name_with_location, "r")
        my_service_id = service_file.readline().strip()
        faux_username = service_file.readline().strip()
        service_file.close()
    else:
        random_word_source = RandomWords()
        service_file = open(full_file_name_with_location, "w")
        my_service_id = random_word_source.get_random_word()
        service_file.write(my_service_id + "\n")
        faux_username = random_word_source.get_random_word()
        service_file.write(faux_username + "\n")
        service_file.close()

    print("\nThis is myServiceID: " + my_service_id + "\n")
    print("This is fauxUserName: " + faux_username + "\n")
    my_username = keyring.get_password(my_service_id, faux_username)
    my_password = ""
    if my_username is None:
        my_username = input(
            "\nPlease enter your username for " + target_website + ": ").strip()
        my_password = input(
            "\nPlease enter your password for " + target_website + ": ").strip()
        keyring.set_password(my_service_id, faux_username, my_username)
        keyring.set_password(faux_username, my_username, my_password)
    else:
        my_password = keyring.get_password(faux_username, my_username)
    return [my_username, my_password]
